# GrepRules public discovery through Rig

Use rig_setup with these arguments (not customer shell commands):

- ["--rules-search","sql","--language","python"]
- ["--rules-search","sql","--language","python","--cursor","NEXT_CURSOR"]
- ["--rule","PUBLIC_RULE_SLUG"]
- ["--rule-yaml","PUBLIC_RULE_SLUG"]

The fixed service is https://api.greprules.io. Search uses GET /api/rules with q,
language, limit=20 and optional cursor. Use the returned public slug (not opaque rule_ ID) for inspect and fetch.
Live opaque-ID lookup returned 404 while the corresponding slug returned 200.
Inspect uses /api/rules/{id}; YAML uses
/api/rules/{id}.yaml. Rig URL-encodes terms, bounds output/time and returns retrieval
time/digest, full service data and explicit pagination completeness. Public reads
were verified without authentication on 2026-11-02. Do not send code, secrets,
private paths or repository identifiers. Search framework/API/CWE terms via q;
no unverified framework/CWE filter names are documented here.

Follow next_cursor until exhausted or disclose the remaining pages/budget. An empty
page is not proof no rule exists globally. Missing metadata/license/tests/revision
remain unknown; retain the returned digest/time when upstream has no revision.
Inspect actual YAML and tests, including source, sink and sanitizer logic, for the
project's language/framework/API shapes. Rule scores are discovery hints only.

HTTP/network/invalid response and unsuccessful service replies fail explicitly;
rate-limit failures must be reported as incomplete discovery. No documented public
rate quota was found in the inspected API docs; do not invent one or automatically
retry in a loop. The service can change; refresh these facts during maintenance.

Fetched artifacts are returned for reviewed project persistence, not executed or
installed by the transport. Validate selected YAML on Rig's installed OpenGrep.
Preserve existing rules and exclusions, retain the original metadata response and
retrieval provenance, then save via the normal candidate/review/apply flow. Pack
fetch is documented upstream but is not exposed by this thin v1 integration; use
individual rule fetch rather than guessing pack URLs or installing another plugin.

Sources: https://greprules.io/docs/api and
https://github.com/greprules/greprules/blob/main/internal/rules/registry.go.
