# Applicability and configuration measures

Apply these targets to discovered features, recording evidence and rationale:

- Injection: SQL CWE-89, OS command 78, code 94, LDAP 90, XPath 643.
- XSS 79, path traversal 22, SSRF 918, unsafe deserialization 502, XXE 611.
- Risky cryptography 327, weak hashing 328, insufficient sensitive randomness 330.
- Hardcoded credentials 798, certificate validation 295, signature validation 347.
- Sensitive logging 532, cleartext sensitive transmission 319, redirects 601.
- Sensitive cookies missing Secure 614 or HttpOnly 1004.

Where concrete project contracts permit: authorization 862/863, authentication of
critical functions 306, CSRF 352, dangerous uploads 434, specific input validation 20.
Memory safety, null dereferences, integer errors and races require relevant languages
and demonstrated analyzer support. Do not infer undocumented business policies.

| Measure | Inventory denominator | Verified numerator |
| --- | --- | --- |
| Files | Relevant project files; exclusions separately listed with reasons | Applicable-rule analyzed files established by engine evidence |
| Weaknesses | Applicable targets above | Compatible rules demonstrably loaded and executed for those targets |
| Sources | Distinct discovered input APIs/wrappers | APIs demonstrably recognized by selected models |
| Sinks | Distinct dangerous APIs/wrappers | APIs demonstrably recognized by selected models |

Count API integrations/patterns, not call occurrences. Record each item's evidence,
recognition as verified/inferred/unknown/unsupported, rule mapping and remaining work.
An engine's scanned-file count alone does not prove applicable security rules ran on
each file. Missing telemetry means unknown, never an invented zero or 100 percent.
A relevant weakness with no compatible rule remains applicable and uncovered.

Keep the same inventory when comparing initial/final setup. Parsing failures,
timeouts, incomplete output, unsupported syntax, unrecognized wrappers and skipped
files cannot disappear from denominators. Intentional exclusions remain separately
accounted for, including owner reason. Source/sink completeness is relative to the
discovered inventory, which may itself be incomplete.

Save schema_version, repository revision/fingerprints, component evidence/scope,
target applicability, source/sink items, selected artifacts/provenance/license/pins,
engine/tool versions, scan receipt IDs/runtime, initial/final measures, unknowns,
errors/exclusions and remaining gaps. Refresh on setup/update when dependencies,
source layout, APIs or configuration change. A profile is evidence-backed agent
output, not a new trusted policy or a claim of exhaustive security analysis.

## Finalize after execution

Assessment input is a bounded project-relative JSON file (256 KiB): components,
targets, sources and sinks are arrays of objects; measures.initial records files,
weaknesses, sources and sinks with denominator/numerator (null plus reason when
unknown). Preserve scope, exclusions with owner reasons, provenance/selection and
remaining_gaps. Each target has applicability: applicable, not_applicable, or
unknown/conditional with a reason. Record API names and representative locations;
recognition and compatibility assertions remain agent analysis, not engine proof.

After rig_check, use rig_setup arguments ["--profile","ASSESSMENT"] then authorized
rig_manage command setup with the same arguments plus --apply --digest TOKEN.
The resulting profile and Markdown report are saved together in the existing Rig
project-state JSON envelope; tool returns its absolute profile_path/report_path.
The inventory seed and earlier preparation attempts remain unchanged. Never edit
Rig project-state/approval files directly; use the preview/apply tool contract. No snapshot
exclusion or approval weakening is needed. Immutable history is retained.

Optionally include --evidence with a JSON array of mappings, for example:
`[{"inventory":"sinks","index":0,"findings":[{"result_id":"check-…","rule_id":"exact.rule","path":"src/file.py","line":12}]}]`.
This adds agent-justified API/target mappings outside bound checkout files after
execution. Rig verifies every finding reference against current actual receipts;
wrong IDs/locations, errors, truncated output or stale evidence get no credit.
Explain the matching logic before mapping a finding to an API/target. A structural
warning does not prove taint flow or vulnerability; source recognition needs its
own evidence. Unmapped items stay unknown. Neither scanning a file nor counting
rules proves applicable rules analyzed that file. Verified finding counts are a
lower bound; a zero lower bound does not establish absence or total lack of coverage.

Read/update with rig_setup ["--report"]. It revalidates saved inputs and tool
bindings; a later receipt sets saved_report_current=false until finalized again.
Use the assessment path in the saved envelope; inspect/refine its inventory if
dependencies, APIs, source layout or exclusions changed. Review changed input/tool bindings and scan before saving; configured scanners
need no execution approval or automatic grant. Other commands retain their reviews. The user need not know any internal commands.
Authored/adapted rules require positive/negative tests; unchanged community rules
need matching-logic inspection and installed-engine validation, not exhaustive
security qualification. Missing coverage remains explicit; finalization does not require solving every security family.
