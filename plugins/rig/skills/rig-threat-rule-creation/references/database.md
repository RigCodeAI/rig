# Preserve the area when adding evidence

Read [save and progress operations](../../rig-onboarding-coordinator/references/workflow.md).
Read your assigned area, preserve earlier work and save partial analysis directly.
Include the inspected bundle_digest as expected_bundle_digest to reject stale edits.
Shared definition changes use exact expected_revision. Read back after saving.
The root host agent handles assignments and continuation.

## Associate the actual registered rule

Select `adopt_existing`, `create_new`, `propose_replacement` or `pending` through
[the shared plan contract](../../rig-onboarding-coordinator/references/shared-protections.md).
Adopt only after this area's own path tests; a different area/owner is no reason for
a duplicate detector. A replacement needs a new ID/path and retains the original
bytes/results. Its expected hashes come from read-area `references[].check_snapshot`,
not invented review fields or arbitrary file hashes. Missing shared work is a durable
dependency/gap. Never overwrite another writer's rule or activate a proposal.

For a new detector evaluated under actual setup authority, or an existing detector,
inspect the current configured generated check through
public `rig_review` using its live schema. Save a `sast_rule` reference to that check's
exact registered package rule file, with its actual `check_id`, `rule_id` and local
`protection_id`. The original author file does not inherit qualification merely
because its contents look equivalent. Rig fingerprints the registered file; do not
invent a hash or copy private evaluation artifacts into evidence.

Run [own caller contrasts](caller-tests.md) and preserve their actual current
receipt separately from detector qualification. A maintained helper receipt cannot
prove newly authored caller tests ran. Record exact rule/applicability and caller
observation fields on this area's canonical protection link.

Inspect changed references and preserve prior records before saving/readback and
recording the rules-stage digest. Progress counts a requirement only from that
current reviewed association and the existing qualification gate. A missing binding
stays unknown; source/rule changes stale evidence. Finite evaluation success does
not establish the whole requirement's meaning or general coverage. Worker failures
and incomplete evaluation remain unknown; rejection/contamination remains distinct.

## Errors: preserve the earlier analysis

All submitted strings share Rig's text filter, including `purpose`, `symbol` and
`test_name`. **Do not include semicolons, backticks or braces.** Code-shaped text,
such as function calls with parentheses, assignment/comparison expressions,
arrows or fenced code, is rejected too. Use short plain words in these fields;
put commands and code in the referenced files. These restrictions apply even to
harmless explanatory prose containing the blocked punctuation.

On the generic bounded-text validation error, keep all unchanged prior-stage
records exactly as read. Inspect the newly added or changed fields first, especially
new reference purposes and test names. Correct those fields after inspection and
retry the full preserved bundle. Do not rephrase earlier threats or code-flow
analysis to hunt the generic error, silently drop records, or refresh stale pointers.
Read back after failure to confirm the prior bundle remains intact.

Issue Rig MCP calls sequentially on each server connection, including reads.
On `Rig operation busy`, wait for the outstanding call to finish, then retry the
unchanged call within its budget. Busy means an outstanding operation, never
missing data. Do not issue overlapping retries or replace an area from a failed read.
