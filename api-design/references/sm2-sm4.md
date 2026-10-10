# SM2+SM4 Application-Layer Encryption: v1 Implementation Contract

Use only when the project explicitly selects an SM2+SM4 application-layer envelope; first read [Application-Layer Encryption Selection](application-encryption.md). This contract starts from the user-provided "SM2 + SM4 Application-Layer Encryption Scheme", **uses the implemented `v8_picture` stateless wire format as the `X-SM-V: 1` baseline**, and then defines a stateful mode with the same wire format, field-level encryption for multipart, browser public-key caching, and a three-level enablement policy. These extensions are design conventions in this skill, **not claims that `v8_picture` has implemented them**.

The original draft also used `X-SM-V: 1`, but its standard Base64, `C2S`/`S2C` derivation, deterministic IVs, and `X-SM-IV` are **incompatible** with this contract. The version header alone cannot distinguish the two v1 formats at the same entry point. Adopting this contract means defining that entry point's v1 as the implemented format below; callers using the original draft format require a separate migration plan. The original document included no license statement; this document restates only the necessary parameters and flow, without copying its conclusions about the project environment.

**Protection boundary**: TLS remains mandatory. This envelope is intended to protect selected sensitive information; it does not require authentication of the entire URL, multipart content, file bytes, or HTTP response status, nor does it provide independent client identity authentication or forward secrecy. Sensitive content such as names, identity document numbers, phone numbers, **passwords/tokens in the body**, callback credentials, and internal topology must be placed in an encrypted JSON body or allowlisted fields; choose whether to protect business identifiers according to their sensitivity. Existing authentication headers such as `Authorization: Bearer ...` are outside this envelope and remain visible at TLS termination points; encrypting the business body does not protect them. Public pagination/sorting fields, resource identifiers in paths, multipart files, and protocol metadata may remain plaintext. If these plaintext elements themselves require tamper resistance or confidentiality after TLS offload, define another scheme; do not claim this envelope covers them.

## 1. Shared Wire Format and Cryptographic Parameters

| Item | v1 convention |
| --- | --- |
| SM2 | The caller encapsulates a random 16-byte `K_s` using the server's authentic sm2p256v1 public key; the uncompressed point starts with `0x04` and is 65B long; ciphertext order is fixed as **C1C3C2** (16B plaintext yields 113B ciphertext). If a JS library omits `04` from its output, restore it before transmission |
| SM4-GCM | Each value requiring encryption uses a 16B derived key, a **fresh random 12B IV**, and a 16B Tag; never reuse the same key/IV combination across different encryption operations |
| Encoding | `Base64_RawURL(IV(12B) ‖ Ciphertext ‖ Tag(16B))`, URL-safe, **without padding**, consistently used for JSON bodies, query values, and multipart text fields; `X-SM-Key` also encodes SM2 ciphertext in unpadded Base64URL. Decoding may accept padded Base64URL, but not the standard Base64 alphabet as another implicit format |
| Key length and encoding checks | 113B SM2 ciphertext encodes to **151 characters** of unpadded Base64URL (152 characters only with padding); do not rely on a library's default ciphertext segment order |
| Version and IV headers | `X-SM-V: 1`; **no `X-SM-IV`**; the IV travels with each ciphertext value, and a single request may contain multiple distinct IVs |

The caller generates session key `K_s` with a CSPRNG and transmits it only as SM2 ciphertext in `X-SM-Key`, never returning it in plaintext; private keys must not enter source code, images, or logs. Key derivation separating purpose/direction/carrier uses the following byte-level formula; both `info` and `scope` are UTF-8 encoded:

```text
KDF_SM3(Z, info, L):
  T_i = SM3(Z ‖ INT32_BE(i) ‖ info), i = 1, 2, ...
  return (T_1 ‖ T_2 ‖ ...)[0:L]

K_msg = KDF_SM3(K_s, "V8SM1|K|" ‖ direction ‖ "|" ‖ scope, 16)
direction = "C2S" (request) or "S2C" (response)
scope = "body" | "query:<parameter_name>" | "form:<field_name>"
```

Construct SM4-GCM AAD separately for **each encrypted value**. Strings are UTF-8, and `\n` is an actual newline byte:

```text
AAD = "V8SM1\n" ‖ METHOD ‖ "\n" ‖ PATH ‖ "\n" ‖ sid ‖
      "\n" ‖ seq ‖ "\n" ‖ ts ‖ "\n" ‖ scope
```

- `METHOD` is uppercase; `PATH` is the request path agreed by both sides, **excluding the query** (URL pathname on the frontend, `URL.Path` in Go middleware). Reverse-proxy rewrites or path escaping may cause mismatches; during integration, fix the actual paths the caller and receiver use for AAD.
- `seq` is a decimal integer, and `ts` is a decimal Unix timestamp in milliseconds; stateless requests use an empty string for `sid`. Response AAD reuses **that request's** method/path/sid/seq/ts; response bodies use `scope=body` and `direction=S2C`. AAD does not include HTTP status or unencrypted fields, so their application-layer integrity is not guaranteed.
- `query:<name>` binds an encrypted query value to its parameter name; `form:<name>` binds an encrypted multipart text value to its part name. `form:` is this contract's multipart extension; the `v8_picture` BFF itself does not implement multipart.

| Request header | Rule |
| --- | --- |
| `X-SM-V` | Required for encrypted requests, value `1`; whether encryption is **mandatory** is determined by the server level, not declared unilaterally by the client |
| `X-SM-Seq` | Required for encrypted requests; stateless callers set `1`, stateful callers increment from `1`; **sequence numbers are not used for replay deduplication** |
| `X-SM-Ts` | Required for encrypted requests, Unix timestamp in milliseconds; the server checks both ends of the time window |
| `X-SM-Key` | Required for stateless requests and stateful session-establishment requests; carries SM2-encapsulated `K_s` |
| `X-SM-Sid` | Required for subsequent stateful requests; omitted from stateless requests |

Encrypted JSON request and response bodies are **single-field** envelopes with `Content-Type: application/json`; business JSON semantics remain unchanged before and after encapsulation:

```json
{"d":"<Base64_RawURL(IV || Ciphertext || Tag)>"}
```

When a JSON body exists and requires encryption, the entire business object goes into `d`, rather than encrypting only selected nested fields. For protected endpoints **expected to receive a JSON body**, reject requests that declare encryption but carry a nonempty body of a type other than `application/json`, have missing/invalid `d`, or cannot be decrypted. Never pass an undecrypted body through to the handler; bodyless requests and defined partially encrypted multipart are exceptions. The existing `v8_picture` middleware skips decryption for non-JSON types, so adopting this constraint requires additional entry-point validation. When a response has a nonempty JSON body and the request envelope has been opened, encrypt the entire response body and include `X-SM-V: 1` and the echoed `X-SM-Seq`; do **not** return `X-SM-IV`. Errors that cannot be unwrapped before session establishment return minimal plaintext responses without `X-SM-V`; JSON errors after successful unwrapping are also encrypted. Successful empty responses use 204 (304 only where applicable), without `X-SM-V`; **200 with an empty body is not covered by this exception**. `OPTIONS` preflight and public-key discovery endpoints are plaintext. When handling successful JSON responses to encrypted requests, callers must validate the envelope rather than silently treating missing headers as successful plaintext; plaintext errors before unwrapping and agreed empty responses are exceptions.

## 2. Stateless Mode: A New Key for Each Request

Suitable for browsers that do not retain sessions and for service-to-service calls; this section's wire format follows the implemented Go/browser stateless protocol in `v8_picture`:

1. Generate a fresh 16B `K_s` for every request (including retries of reads), encapsulate it with the server's SM2 public key as `X-SM-Key`, and send `X-SM-V: 1`, `X-SM-Seq: 1`, and `X-SM-Ts`; **do not send `X-SM-Sid`**.
2. For requests with a JSON body, derive the key with `direction=C2S, scope=body`, generate a fresh IV, and transmit `{"d":...}`; do not create empty envelopes for bodyless GET/DELETE requests. Encrypt each sensitive query value with `query:<name>`; query parameters not configured as sensitive remain plaintext. The caller and server must agree on the allowlist; one side must not encrypt while the other reads plaintext.
3. The server parses headers, checks the timestamp, unwraps `K_s` with SM2, and authenticates/decrypts each field using its scope/AAD before business processing. If there is a JSON response, encrypt it with the same `K_s`, `direction=S2C, scope=body`, and a **fresh random IV**. Discard `K_s` at the end of the request; do not allocate a `sid`.

```http
POST /api/v1/items:search HTTP/1.1
Content-Type: application/json
X-SM-V: 1
X-SM-Seq: 1
X-SM-Ts: 1730000000000
X-SM-Key: <Base64_RawURL(SM2_C1C3C2(PK_enc, K_s))>

{"d":"<Base64_RawURL(IV || Ciphertext || Tag)>"}
```

In this mode, `seq=1` and the timestamp are not replay prevention: the same request **can execute repeatedly** within the permitted time window; replaying the same ciphertext repeats decryption, not encryption. The server still uses a **fresh IV** whenever it generates a response, avoiding reuse of `(K_s, IV)` for different responses to replayed requests. Define separate duplicate-submission policies such as idempotency keys or unique business IDs for business-write side effects; idempotency does not change the fact that messages can be replayed within the window. Frequent encryption of many values in one request also requires controlling IV collision risk under each derived key.

## 3. Stateful Mode: The Same Wire Format with Reusable Keys

**This is a design extension to the stateless wire format, not an existing `v8_picture` feature.** SM2/SM4 parameters, Base64URL, `scope`, AAD, and random IVs are **identical to stateless mode**; do not restore the original draft's deterministic IVs, standard Base64, or old KDF.

1. **Session establishment**: the caller generates `K_s` and sends an encrypted establishment request without `X-SM-Sid` but with `X-SM-Key` (the project may select a dedicated session endpoint), encrypting with an empty `sid` in request AAD. After unwrapping, the server generates an unpredictable `sid` and stores `sid → {K_s, authenticated principal/permission boundary, idle/absolute expiry, encryption count}`, with a TTL and no plaintext-key logging. The establishment response must return JSON containing `sid` in that request's `S2C/body` envelope. The caller **obtains `sid` only from a validated ciphertext body**, not plaintext response headers. An endpoint without a response body cannot serve as a successful establishment response.
2. **Subsequent requests**: carry `X-SM-Sid`, `X-SM-Seq`, `X-SM-Ts`, and `X-SM-V`, **no longer carrying `X-SM-Key`**. The server first looks up the session for the authenticated caller and validates `sid` ownership and TTL, then retrieves `K_s` to validate ciphertext/AAD. Responses reuse the request's `sid` and other AAD metadata, with the separate `S2C/body` key and a fresh random IV.
3. **Expiry and rotation**: suggested idle timeout is 30 minutes and absolute timeout is 8 hours. Revoke the old `sid` on logout, authenticated-principal changes, or token refresh, and generate a new `K_s`/`sid` through a new establishment request. Random IVs are **not** derived from `seq`. End sessions early and rotate keys for long sessions or excessive encryptions under one derived key; set limits according to project message volume, rather than treating the original document's 2³²-message limit as a safety guarantee for random IVs.

Clients still increment `seq` and send valid timestamps for normal requests, but the server **does not maintain a set of used sequence numbers or reject repeated `seq` values within the window**. Stateful mode only reuses keys to reduce per-request SM2 operations; it does not imply replay protection. Session-establishment requests themselves can also be replayed within the window, so rate-limit establishment attempts. Concurrent requests may arrive out of order; identical requests can take effect repeatedly during their validity period, and writes still rely on business idempotency. `sid` is not a login token and cannot replace authentication or authorization.

## 4. Special Carriers and Partial Encryption

| Carrier/field | Application-layer handling | Plaintext boundary |
| --- | --- | --- |
| Bodyless GET/DELETE | Encrypt each allowlisted sensitive query value with `query:<name>` as Base64_RawURL; the server decrypts by name and restores values for the business layer | Paths, parameter names, and nonsensitive query values remain plaintext; suggested encrypted query limit is 4 KiB |
| JSON requests/responses | Encrypt the entire nonempty business JSON body as `{"d":...}` | HTTP methods, paths, statuses, and other headers remain visible |
| multipart text fields | Separately encrypt only sensitive allowlisted part values using `form:<name>`, such as `items` JSON text or `callback` configuration; parse using the original media type after decryption | Nonsensitive text fields outside the allowlist may remain plaintext |
| multipart file parts | v1 provides no application-layer encryption or authentication | File bytes, part names, `filename`, `Content-Type`, and so on remain visible; rely on TLS, authentication, and file validation |

The request as a whole remains `multipart/form-data`; encrypted text-value parts may still use `text/plain`, with values of `<Base64_RawURL(IV ‖ Ciphertext ‖ Tag)>`. **An `X-SM-V: 1` request may leave some text fields and files unencrypted**; `force` only mandates use of the envelope and protection of the specified sensitive fields, not protection of file bytes. Do not misreport plaintext fields as "GCM-authenticated." Each endpoint specifies its field allowlist and requiredness. By default, **reject duplicate query values or multipart text parts with the same allowlisted name**, rather than decrypting only the first and silently dropping the rest. If an endpoint genuinely needs repeated values, separately agree on handling and ordering for every value. Existing `v8_picture` query processing uses `get/set`; implementing this rejection rule requires changes to the caller and server. Filenames and client media types are untrusted; continue validating file size/type, temporary storage, and access control under the upload contract.

Public file downloads may use TLS, authentication, or short-lived signed URLs; this does not constitute file-byte encryption by this envelope. SM4-CTR + an unkeyed `SM3(plaintext)` digest is **not** a defined authenticated streaming-file protocol and is not enabled in this v1; it cannot establish file integrity.

## 5. Public-Key Delivery and a 5-Minute Browser Cache

Under `on`/`force`, the server provides a plaintext public-key discovery endpoint requiring no authentication (path follows the API prefix, for example `GET /api/v1/sm/public-key`), with a response such as:

```json
{"version":"1","public_key":"04<128 hex>"}
```

The browser **fetches the public key dynamically** from this endpoint and validates the version, encoding, and curve public-key format. Cache successful results only in memory for the current page execution, keyed by **the full public-key endpoint URL + version**, and reuse them **for 5 minutes from successful retrieval**; fetch again after expiry. HTTP retrieval may still use `cache: no-store`/`Cache-Control: no-store`; these 5 minutes refer to an application memory cache, not a proxy cache. On retrieval failure, version mismatch, or malformed data, do not send business requests that should be encrypted. After cache expiry, do not reuse old values or automatically fall back to plaintext.

This differs from the current `v8_picture` browser implementation, which **fetches the public key anew for every request**, and is a new requirement in this contract. Runtime retrieval is not public-key fingerprint pinning: public-key authenticity depends on HTTPS and the endpoint delivery chain; a party that can actively replace the public-key response can substitute a key, and the 5-minute cache does not solve this. Leakage of the long-term SM2 private key still permits unwrapping historical recorded `K_s` values. During key rotation, the server should account for browsers caching old public keys for up to 5 minutes and for in-flight requests: retain the old private key briefly for unwrapping, or explicitly accept failures during the transition; never silently downgrade to plaintext after failure. Service-to-service calls may preconfigure public keys under the project contract and need not use the browser caching policy.

## 6. Levels, Errors, and Verification

Configure levels for the protected endpoint/caller scope; the meanings of `off/on/force` are **not** negotiated through untrusted request headers:

| Level | Requests without `X-SM-V` | Requests with `X-SM-V: 1` |
| --- | --- | --- |
| `off` | Plaintext processing only | Reject; do not pass ciphertext through to the business layer |
| `on` | Process under the published plaintext/legacy contract | Decrypt with this envelope; handle responses as specified |
| `force` | Reject (for example `sm_required`) | Validate and decrypt; some nonsensitive multipart fields and files may remain plaintext |

Public-key discovery, `OPTIONS`, and explicitly listed health probes may be exempt from `force`, but **business routes must not fall back to plaintext on their own because encryption headers are missing**. Protected JSON routes must validate both media type and the body envelope, not treat a plaintext body as an encrypted request merely because some `X-SM-*` headers exist. A bodyless request with no sensitive fields has no business ciphertext to validate, even if it carries envelope headers; in this case `force` constrains only the enablement marker and defined fields, not cryptographic authentication of the whole request. A client under `on` that has selected encryption must not automatically fall back because it cannot obtain a public key or receives an unexpected successful plaintext response. `off` requires an explicit **plaintext client mode**, with no public-key retrieval or encryption headers. The existing `v8_picture` browser always retrieves the public key before business requests, so switching to this contract's `off` requires client changes as well as server configuration changes. Reject other `X-SM-V` values rather than processing them as plaintext. For legacy-client migrations, assess the duration and transition conditions of `on`; do not retire old envelopes without authorization.

The server validates `|now - ts| ≤ 300 seconds` (checking both past and future), but **allows duplicate submissions within this window**; `sm_replay` is not an error in this scheme. Externally collapse ciphertext/SM2 format/Tag errors into `sm_invalid`, without leaking detailed causes. Timestamp expiry may use `sm_expired`, invalid stateful `sid` may use `sm_session_expired`, and encrypted query/request-body size violations may map to the project's existing `request_too_large`. Reject both encrypted requests under `off` and plaintext requests under `force`; specify HTTP statuses/error bodies under the project's published contract. The original draft's `408`/`426` status mappings do not become universal HTTP requirements because of this document.

Verification must at least cover: SM3/SM4 known vectors, SM2 C1C3C2 and the `0x04` prefix, and Base64URL round trips; two encryptions of the same plaintext with the same `K_s`/direction/`scope` must use different IVs; ciphertext must not decrypt across directions, scopes, or methods/paths. For `K_s="0123456789abcdef"`, `KDF_SM3(K_s, "V8SM1|K|C2S|body", 16)` should be `837cd670f33501d83a7dc35107621524`. An AAD interoperability vector can use `METHOD=POST, PATH=/api/v1/images:search, sid=sess-1, seq=1, ts=1730000000000, scope=body`, with expected UTF-8 text `V8SM1\nPOST\n/api/v1/images:search\nsess-1\n1\n1730000000000\nbody`; actual stateless requests should use an empty `sid`. Also cover 5-minute public-key caching/expiry and rotation, the three levels, empty bodies, encrypted errors, partially plaintext multipart, within-window replay in both modes, and write idempotency. **Test vectors and the implemented stateless flow do not establish that the new stateful mode, caching, or enforcement policy is implemented in the target project.**

Do not log `K_s`, private keys, the SM2 ciphertext header `X-SM-Key`, `d`, decrypted sensitive fields, or files to logs/APM. Public-key discovery, allowed within-window replay, partially plaintext fields, and browser dynamic public-key boundaries should all be explicitly disclosed in target endpoint contracts. Neither this envelope's algorithm names nor passing tests are equivalent to security review or compliance certification. [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html#section-3.1) requires unique AEAD nonces under the same key, and its AEAD interface itself provides no replay-prevention service; [RFC 8998](https://www.rfc-editor.org/rfc/rfc8998.html#section-3.5.1) describes SM4-GCM usage in TLS 1.3, not a standard for this HTTP envelope.
