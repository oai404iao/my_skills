# Using the Bruno CLI

Read this when running, importing, or writing CI configuration. This reference focuses on common commands checked against official source code; **the installed version's help, project wrappers, and authorization scope take precedence**. Do not assume every documented option is available in the installed version.

Entry points: [CLI documentation](https://docs.usebruno.com/bru-cli/overview), [run options](https://docs.usebruno.com/bru-cli/run/options), [run implementation](https://github.com/usebruno/bruno/blob/8833538ce20548f26b88079ce701095e7b06f682/packages/bruno-cli/src/commands/run.js).

## Installation and Invocation

The package is **`@usebruno/cli`** and the executable is **`bru`**. Installing through a package manager requires Node.js compatible with the selected CLI version; check the project's runtime conventions and that version's requirements rather than inferring Node requirements from the desktop version. First inspect existing project dependencies, the lockfile, and scripts; do not install another copy at a different version:

```sh
# When a global CLI is already installed
bru --version
bru --help
bru run --help

# For an existing project-local dependency, invoke from a project directory that resolves it
pnpm exec bru --version
pnpm exec bru run --help
```

If it is not installed, report the missing dependency first, then choose an installation method according to user authorization and the project's package manager. These are examples, not instructions to execute both:

```sh
# Global installation: changes the local tool environment
pnpm add -g @usebruno/cli

# Project-local installation: changes the manifest and lockfile; pin the project-selected version
pnpm add -D @usebruno/cli@<approved-version>
```

`<approved-version>` is a placeholder. The official documentation also provides `npm install -g @usebruno/cli`; npm projects should retain their own approach rather than migrate package managers. Use the project lockfile to pin the version in CI; do not default to fetching the latest version with `dlx` to run an existing collection.

Replace `bru` with `pnpm exec bru` in the following examples only when the project's dependency resolution path supports it. If a project script already handles changing the working directory, reuse it rather than inventing another invocation.

## Working Directory and Execution Scope

**Run from the collection root**, not the request's subdirectory or an arbitrary Git root. The checked implementation uses `process.cwd()` to read collection root configuration; positional arguments to `run` identify requests/folders within the collection, not arbitrary collection roots.

Below, `path/to/collection`, request names, and folder names are example placeholders. Before executing, replace them with confirmed real paths, an environment, and a safe scope:

```sh
cd path/to/collection

# Single request: prefer the smallest necessary scope
bru run health/get-health.bru --env Local

# Required dependency chain: login and subsequent requests follow project seq/script rules
bru run auth/login.bru users/get-current.bru --env Local --bail

# Requests directly within the specified folder
bru run health --env Local

# Include subfolders of the specified folder
bru run health -r --env Local

# Entire collection: without positional arguments, execution is recursive and requires separate full-scope authorization
bru run --env Local
```

For YAML collections, replace request paths with the actual `.yml` files; folder commands remain the same. An explicit folder path is not recursive by default, unlike `bru run` without a path.

File ordering follows `seq` and collection execution logic, not just command-line positional arguments or filenames; chaining scripts may also jump between requests. Do not substitute rearranging arguments for request order configuration.

Before running, review inherited scripts and `bru.runRequest()` / `bru.sendRequest()` / `bru.setNextRequest()`. Scripts may send additional requests even when you specify only one request, add tags, or use `--tests-only`. `--bail` is not a transaction rollback and cannot undo writes that have already occurred.

## Environments and Secrets

```sh
# environments/Local.bru, or Local.yml in a YAML collection
bru run health/get-health.bru --env Local

# Resolve the path from the collection root; choose a file format supported by the actual version
bru run health/get-health.bru --env-file ./environments/Local.bru

# Non-sensitive variable override; --env-var can be repeated
bru run health/get-health.bru --env Local --env-var baseUrl=http://localhost:3000
```

- Explicitly confirm the target service; omitting `--env` does not guarantee "no environment", because collection configuration may define a default.
- The checked implementation loads `--env-file` first, merges `--env` next (the latter wins for matching names), and finally applies `--env-var` overrides. Normally, choose just one environment loading method; if combining them is necessary, check the target version's merge and inheritance behavior.
- In the current source, `--env-file` does not resolve an environment's `extends` chain; do not assume it is equivalent to `--env`. Check new features against the actual version rather than restructuring environments for this task.
- The current implementation builds variables from the process environment, then loads `.env` at the collection root; same-name `.env` values override process values in that runtime view. If CI-injected values "do not take effect", first check same-name local configuration without outputting secrets.
- Secret values stored by the GUI are not automatically passed to the CLI. Use the project's existing secret injection, process environment references, or an untracked `.env`; do not put real tokens in `--env-var` command-line arguments, to avoid leaks through shell history and process arguments.
- If scripts use persistent variable APIs, running them may write back to environment or collection files. Confirm authorization for those writes before execution, then inspect the diff afterward; do not overwrite or revert user changes without authorization.
- Workspace global environments require `--global-env` and, when necessary, `--workspace-path`; use them only when the collection actually depends on them, and check workspace files and version support.

## Filtering, Failures, and Script Permissions

| Option | Purpose and boundaries |
| --- | --- |
| `--tags smoke,sanity` | According to the official options documentation, includes requests matching any listed tag; the current source also considers tags inherited from folders |
| `--exclude-tags destructive` | Excludes requests with matching tags; not a security boundary that prevents additional requests from scripts |
| `--tests-only` | Selects requests with tests or enabled assertions; **still sends HTTP requests** and omits prerequisites such as login requests without tests |
| `--bail` | Stops subsequent execution after a request error or a test/assertion failure; does not roll back |
| `--delay 100` | Delay between requests, in milliseconds; not a substitute for the service's rate-limit contract |
| `--sandbox safe` | Default sandbox in the current source; check the installed version |
| `--sandbox developer` | Expands script capabilities; use only when explicitly needed and authorized, not as a general fix after failure |

Historical material may use `--test-only` (singular). The checked source registers `--tests-only`; choose according to `run --help` rather than relying on unknown arguments being accepted. The checked `run` command has no `--dry-run`; do not invent an offline execution option.

Use data-file, iteration, parallel, and experimental options only when the current CLI help confirms support. Loops repeat writes, and parallel execution may disrupt shared tokens, variables, ordering, and rate limits; do not enable them unless requested.

Script execution is also affected by the collection's module allowlist and filesystem permissions. First address missing dependencies, variables, or sandbox compatibility; do not grant unrestricted module/filesystem access to "make tests pass".

## TLS, Proxies, and Upload Paths

```sh
bru run health/get-health.bru --env Local --cacert ./certs/internal-ca.pem
```

By default, `--cacert` adds a CA to the existing trust store; combined with `--ignore-truststore`, it uses only the specified CA. Client certificates can be configured through collection settings and `--client-cert-config` where supported by the version.

Do not add `--insecure` by default to disable certificate verification. For proxy issues, first check collection and system proxies; `--noproxy` bypasses both and should be used only when explicitly needed. Do not hide an incorrect target address by bypassing TLS or proxies.

Check upload/binary file paths against the target version's runner: the checked implementation resolves relative paths against the **collection root**, not the request file's directory; absolute paths are used as supplied. Prefer existing portable project paths and confirm the actual files. Do not guess how `@file(...)` resolves based only on the request's directory.

## Reports and CI Results

Generate reports only when actually needed. The paths below are examples; first choose a location where writing is authorized and will not overwrite user files. Report parent directories must already exist; if missing, first create them in an authorized location:

```sh
bru run health -r --env Local --bail \
  --reporter-json ./reports/results.json \
  --reporter-junit ./reports/results.xml \
  --reporter-html ./reports/results.html \
  --reporter-skip-all-headers \
  --reporter-skip-body
```

`--reporter-json` / `--reporter-junit` / `--reporter-html` can be combined. The legacy-compatible form is `--output results.json --format json` (`format` can also be `junit` / `html`); the official documentation marks the old interface as deprecated. Prefer reporter options, while retaining the version-appropriate form for older projects.

Default reports may contain request/response headers and bodies. `--reporter-skip-*` only reduces report fields; it does not guarantee removal of secrets from URLs, queries, script logs, or test messages. Review and redact reports before publishing or uploading them. Do not enable verbose output or print full responses by default for debugging.

- Successful runs usually return `0`; assertion/test failures, request errors, or configuration errors return nonzero. Exact values depend on the actual version.
- The checked runner preserves HTTP responses present in Axios errors and continues with assertions/tests; non-2xx does not automatically mean a transport failure. Use assertions/tests to evaluate the expected status and business contract; negative tests should not require 2xx either.
- `0` does not prove "the expected tests actually ran": check selected request, test, and assertion counts, as well as skipped items. An empty filtered collection or an entirely skipped run is not successful API verification.
- Reuse existing project test scripts in CI and preserve Bruno's nonzero exit code. When piping to `tee`, retain failure status (for example, with Bash's `pipefail`); do not swallow errors with `|| true`.

See the [report documentation](https://docs.usebruno.com/bru-cli/run/reports). Commands, report generation, and CI network execution must fall within the current authorization scope; adding documentation does not authorize executing them.

## Importing OpenAPI

Importing generates files; it is not API testing and does not automatically provide complete authentication, scenario chains, or valid assertions.

First read `bru import --help` and confirm the output location, whether it already exists, and the format. Using a local specification file avoids extra network downloads. Run this example from the directory containing `api.yaml`; `./generated` should be an approved new output location:

```sh
# Explicitly select bru when matching an existing Bru collection's format
bru import openapi \
  --source ./api.yaml \
  --output ./generated \
  --collection-name "Service API" \
  --collection-format bru
```

The current source defaults to the `opencollection` import format; you can explicitly specify `--collection-format opencollection` when YAML is needed. If an older CLI lacks this option, follow its help and actual output rather than copying the example blindly.

The output argument may serve as the generated collection's parent directory; after import, identify the actual collection root containing `bruno.json` / `opencollection.yml` before running. First review the generated files in a separate new directory, checking URLs, authentication, bodies, variables, `seq`, and tests; then selectively incorporate them into the target collection rather than overwriting a manually maintained collection.

A URL passed to `--source` triggers a download; WSDL import and external references may also read related files or network resources. Remote retrieval, bulk generation, and overwrites must be within the authorization scope. For other formats such as Postman/Insomnia, do not invent `bru import` subcommands; instead, check the actual version's help and the [official converters](https://docs.usebruno.com/converters/overview).
