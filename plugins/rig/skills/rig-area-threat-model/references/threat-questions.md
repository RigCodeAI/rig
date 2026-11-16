# Select questions from observed boundaries

Use this as a prompt, not a category quota. One concrete boundary may support
several risks. A fixed public health response need not acquire private-data or
owner checks. Missing external implementation stays unknown.

| Observed operation | What could go wrong / what must hold? |
| --- | --- |
| Input handling | Which fields, keys, headers or stored values can callers control? Require bounds, accepted shapes and context-appropriate handling. |
| Login/session | Could identity be forged, confused or reused after expiry? Bind identity to the intended session and operation. |
| Explicit permissions | Can a different route, bulk action or fallback bypass resource permission? Require the intended caller/action/resource decision. |
| Customer separation | Can an ID, cache key or saved context select another customer's data? Preserve owner/customer scope at every access path. |
| Database queries | Which input reaches which query operation? Keep values separate from query instructions and scope reads/writes to authorized data. |
| Browser output | Does caller or stored content reach HTML, script or browser navigation? Require handling appropriate to that output context. |
| Files | Can callers choose paths, names, archives or links? Keep access within intended roots and allowed files. |
| Outbound requests | Can input select a destination now or after storage? Require allowed destinations, including redirects and resolved addresses where applicable. |
| Parsing | Can untrusted documents/objects trigger unintended interpretation or disproportionate work? Restrict accepted formats and size/depth. |
| Secrets | Could credentials/private data reach logs, errors, URLs or responses? Restrict exposure and protect security-sensitive randomness/keys. |
| Security configuration | Does missing configuration, dependency failure or fallback remove the intended boundary? Require an explicit safe failure outcome. |
| Failure/resource limits | Can input consume shared workers, memory, connections or repeated jobs? Bound work, retries and sensitive error details. |

## Selected upstream text reused literally

Cloudflare, RECONNAISSANCE.md, principals section:

> Per-resource authorization and tenant/owner scope.

Cloudflare, ATTACK-CLASSES.md, indirect injection:

> Do not stop at the obvious direct paths. Look for indirect injection: data stored safely, then retrieved and used in a dangerous context by different code.

Cloudflare, ATTACK-CLASSES.md, feature abuse:

> Can a user set a notification URL, webhook URL, or callback URL that the server fetches?

Apply those questions to threat hypotheses and required protections. The upstream
full-audit instructions to hunt, prove, fix, score and delegate are not adopted.
See [source and license record](SOURCES.md).

## Specificity examples

Useful: A customer supplies an invoice ID to the download flow. Another customer's
invoice could be returned if ownership scope is lost. Requirement: private invoices
must only reach permitted customers. Basis: documented owner policy. Current owner
check is observed, effectiveness remains for the next stage.

Too vague: Injection may happen. Better: user-supplied search text reaches the
invoice query. Its values must remain separate from query instructions. Whether
the current query builder does that is unverified here.

A refund amount may need standard numeric bounds and caller authority. Eligibility,
refund windows and discount combinations require owner policy and stay deferred.
