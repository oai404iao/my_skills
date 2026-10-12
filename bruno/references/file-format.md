# Bruno File Formats

Read this reference before editing. The following primarily covers HTTP `.bru` collections; handle YAML collections as described in the final section. These are independently written format examples, not target-project paths, API contracts, or authorization to execute.

Implementation references: [Bru parser](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/packages/bruno-lang/v2/src/bruToJson.js), [serializer](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/packages/bruno-lang/v2/src/jsonToBru.js). Official documentation: [language](https://docs.usebruno.com/bru-lang/language), [tags](https://docs.usebruno.com/bru-lang/tag-reference).

## Collection File Responsibilities

```text
<collection>/
├── bruno.json
├── collection.bru          # Optional: collection-level auth, variables, scripts, tests, docs
├── environments/
│   └── Local.bru
└── health/
    ├── folder.bru          # Optional: folder-level configuration and inheritance
    └── get-health.bru
```

`<collection>` is a placeholder. Minimal Bru collection root configuration:

```json
{
  "version": "1",
  "name": "Service API",
  "type": "collection"
}
```

Here, `"1"` is the collection file format version, not the Bruno application or CLI version. An existing `bruno.json` may also contain `ignore`, proxy, client certificate, script permission, and other settings; preserve them during targeted edits.

`collection.bru` / `folder.bru` are not ordinary requests. Use blocks supported by the collection parser, such as `headers`, `auth`, `auth:bearer`, `vars:pre-request`, scripts, and `tests`; do not insert complete request blocks into them. For example:

```bru
auth {
  mode: bearer
}

auth:bearer {
  token: {{process.env.BRUNO_API_TOKEN}}
}
```

Both collections and folders can define inherited scripts, authentication, and variables. Changing either file may affect multiple requests; running a single request does not mean skipping inherited logic. See the [collection parser](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/packages/bruno-lang/v2/src/collectionBruToJson.js).

## Basic Bru Syntax

- **Dictionary blocks**: `headers { ... }`, with one `key: value` per line. They are not JSON objects; do not add JSON-style commas. Do not casually quote ordinary values, because the quotes may become part of the value.
- **Text blocks**: `body:json`, scripts, `tests`, `docs`, and similar blocks store multiline raw text. JSON content must separately conform to JSON syntax.
- **Lists**: for example, `tags: [...]` inside `meta`. Request tags are usually written one per line without commas; do not directly apply the array syntax of an environment file's `vars:secret`.
- The `~` prefix disables fields that support disabling (such as headers, params, variables, and asserts); it is not deletion or a general-purpose comment. Preserve existing disabled entries.
- Text blocks end with an unindented `}` line. Keep indentation on `}` inside JSON/JS, or it may prematurely close the outer block. Do not remove indentation globally.
- Do not add guessed comment syntax at the top level; put explanations in `docs` and JavaScript comments inside scripts/tests. Check the target version and nearby examples before using extended syntax such as multiline dictionary values.

## HTTP Request Template

```bru
meta {
  name: Get health
  type: http
  seq: 1
  tags: [
    smoke
  ]
}

get {
  url: {{baseUrl}}/health
  body: none
  auth: inherit
}

headers {
  Accept: application/json
  ~X-Debug: true
}

assert {
  res.status: eq 200
}

tests {
  test("health response is an object", function () {
    expect(res.getBody()).to.be.an("object");
  });
}

docs {
  Read-only health check. Expected response is defined by the service contract.
}
```

- Common method blocks are `get`, `post`, `put`, `patch`, `delete`, `head`, and `options`; keep one method block per HTTP request.
- `meta.name` is the display name; `seq` controls ordering. Do not infer request execution order from filenames. Do not reorder the entire collection just to add one request.
- `auth: inherit` uses parent authentication; `auth: none` means no authentication. Explicit Bearer authentication uses `auth: bearer` in the method block plus `auth:bearer { token: ... }`. Do not also add a conflicting Authorization header.
- `assert` uses Bru assertion expressions, such as `res.status: eq 200` and `res.body.id: isDefined`; do not treat operator display names in the GUI as file syntax.
- The test block is named **`tests`**, not `body:test`; use `test(...)` and Chai `expect(...)` for complex conditions. Base status codes and structures on the actual API contract rather than copying the template.

## Parameters and Request Bodies

### Query and Path

```bru
get {
  url: {{baseUrl}}/users/:userId?include=profile
  body: none
  auth: inherit
}

params:path {
  userId: {{userId}}
}

params:query {
  include: profile
}
```

The query in the URL and `params:query` are two representations; keep them consistent when editing, and adjust the URL accordingly when disabling parameters. Do not assume the CLI automatically synchronizes them like the GUI editor does; `params:path` corresponds to `:userId` in the URL.

### JSON

```bru
post {
  url: {{baseUrl}}/users
  body: json
  auth: inherit
}

headers {
  Content-Type: application/json
}

body:json {
  {
    "name": "Example",
    "teamId": "{{teamId}}"
  }
}
```

The outer `body:json` is a Bru tag; the inner content is valid JSON. Types after interpolation must match the contract; do not hardcode all numbers, booleans, or objects as strings.

| Method block's `body` | Content block |
| --- | --- |
| `none` | No request body |
| `json` | `body:json` |
| `text` / `xml` | `body:text` / `body:xml` |
| `formUrlEncoded` | `body:form-urlencoded` |
| `multipartForm` | `body:multipart-form` |
| `file` | `body:file` |
| `graphql` | `body:graphql`, plus `body:graphql:vars` when needed |

GraphQL requests usually use `meta.type: graphql` and the `post` method; do not write the query as a JSON request body. Older collections may use the compatible `body` text block; do not migrate it as part of a targeted edit.

### Forms and Files

```bru
body:form-urlencoded {
  username: {{username}}
  ~optionalField: unused
}
```

```bru
body:multipart-form {
  description: Example attachment
  attachment: @file(fixtures/sample.txt) @contentType(text/plain)
}
```

Before uploading, verify that the file exists, how its path is resolved, and that the upload is authorized; do not expose local absolute paths or upload private files. Normally, let the runtime generate the multipart boundary rather than setting it manually. Example binary body:

```bru
body:file {
  file: @file(fixtures/sample.txt) @contentType(text/plain)
}
```

These are content block fragments and require the correct `body` mode in the method block; see the [CLI reference](cli.md) for file path details.

## Environments, Interpolation, and Scripts

Example `environments/Local.bru`:

```bru
vars {
  baseUrl: http://localhost:3000
  userId: sample-user
}

vars:secret [
  apiToken
]
```

`--env Local` selects an environment name, not a path with an extension. `vars:secret` stores secret variable names, **not secret values**, and does not retrieve GUI-local secrets for the CLI. See the [environment parser](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/packages/bruno-lang/v2/src/envToJson.js) for the implementation.

- Ordinary interpolation: `{{baseUrl}}`; process environment reference: `{{process.env.BRUNO_API_TOKEN}}`.
- The CLI can use `.env` at the collection root or injected process environment variables. Do not commit the real `.env` or read/output an entire secret file for this purpose. Follow the project's secret injection approach.
- Variables can come from collections, folders, requests, environments, and the runtime. Check same-name overrides and references against actual inheritance; avoid adding a same-name variable that shadows the original value.
- `vars:pre-request` / `vars:post-response` declare variables for request phases; they are not the environment file's `vars`.
- `script:pre-request` prepares for sending; `script:post-response` handles responses; `tests` evaluates outcomes. Use `bru.setVar(...)` for runtime values; do not write temporary tokens back to version-controlled environment files.

```bru
script:post-response {
  const body = res.getBody();
  if (res.getStatus() === 200 && body.token) {
    bru.setVar("sessionToken", body.token);
  }
}
```

In scripts, `bru`, `req`, and `res` are Bruno APIs, not Postman's `pm`. `bru.runRequest()`, `bru.sendRequest()`, and `bru.setNextRequest()` can expand the actual network scope. Parent script order is also affected by the collection's `scripts.flow`; do not present one ordering as a fixed rule for all projects. See the [JavaScript API](https://docs.usebruno.com/testing/script/javascript-reference) and [script order](https://docs.usebruno.com/testing/script/script-flow).

## OpenCollection YAML: Recognize and Preserve

Existing YAML collections use `opencollection.yml`, `folder.yml`, `environments/<name>.yml`, and request `.yml` files. Do not create `bruno.json` or `.bru` to "complete" such a collection; first read the [structure reference](https://docs.usebruno.com/opencollection-yaml/structure-reference) and nearby files.

Minimal HTTP request example:

```yaml
info:
  name: Get health
  type: http
  seq: 1
http:
  method: GET
  url: "{{baseUrl}}/health"
  auth: inherit
runtime:
  scripts:
    - type: tests
      code: |-
        test("health returns 200", function () {
          expect(res.getStatus()).to.equal(200);
        });
```

Common mappings: `meta` → `info`; method block → `http.method/url`; headers/params → lists inside `http`; request body → `http.body.type/data`; scripts/tests → `runtime.scripts` (`before-request`, `after-response`, `tests`). Use block scalars for multiline code/JSON in YAML; preserve quotes and types in variable interpolation.

The official overview and migration pages conflict on whether mixed formats are allowed. This skill's conservative policy is to **keep each collection in its single existing format** rather than rely on mixed-format behavior. Format migration changes paths and script references and may delete original files; it requires separate authorization, a backup, and verification against the actual version. Do not use GUI migration steps as the ordinary AI editing workflow. See [sources](sources.md) for the basis.
