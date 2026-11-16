# Read, replace, read back

Read [save and progress operations](../../rig-onboarding-coordinator/references/workflow.md).
Read your assigned area, preserve earlier work and save partial analysis directly.
Include the inspected bundle_digest as expected_bundle_digest to reject stale edits.
Shared definition changes use exact expected_revision. Read back after saving.
The root host agent handles assignments and continuation.


Use the actual tools/list schemas; host prefixes may differ. The native names are
`rig_analysis_read_area`, `rig_analysis_save_area`, `rig_analysis_list_areas` and
`rig_analysis_save_application`. This stage reads/saves its one area. It never
replaces the application map. There is no SQL access or shell save fallback.

Read with arguments `{"id":"AREA_ID"}`. Use `structuredContent.report`; the text
content is only a short summary. A read result is not a save request.

Read [shared requirements](../../rig-onboarding-coordinator/references/shared-protections.md).
Build the complete writable object with preserved `protection_links`, plus current
the inspected `bundle_digest` as optional `expected_bundle_digest`:

```text
area, elements, flows, risks, protection_requirements, protection_links, references
```

Project only writable fields from each record. Retain every prior-stage record
unless you have inspected evidence for a needed refinement. Keep requirement and
risk intent intact; reuse flow IDs. Use `owned_risks` for owned risk definitions,
including ones used only by another area. Map read `revision` to `expected_revision`
for shared definitions (new is 0). Omit derived owner/revision properties. Other
areas' shared risks remain with their owner; do not resubmit or take them over.
Preserve owned risks' `affected_area_ids` so existing shared links survive.

Omit `application`, `worktree_id`, `bundle_digest`, `referenced_evidence`, `evidence_label`, and the
reference properties `fingerprint`, `freshness` and `check_snapshot`. Rig computes fingerprints.
References contain ID, kind, relative path, purpose and optional symbol/range,
test_name, check_id, rule_id or protection_id. Test/rule references must retain a
valid canonical protection_id with current area membership. A range uses start_line, start_column, end_line and
end_column, all one-based. Point at existing regular files only.

Flows have ID, label, description and ordered steps. Steps have a unique positive
order and label; optional transfer, role, element_id, reference_id and explanation.
Owned requirements retain legacy local risk/flow links. `protection_links` names
canonical definition/revision and this area's risks, flows and path references. A
foreign risk must already apply here. Do not copy or edit a foreign definition.
Preserve rule plans and caller observation history; append corrections under new
observation IDs. Record own invocation/denial paths, never inherit helper support. IDs are unique per kind in
the project, so prefix new IDs with the area ID. Shared application elements can
be referenced without copying them into local elements. Do not add invented fields.

Save the entire bundle, not a patch: omitted arrays become empty. Each text field
is single-line prose at most 2,048 UTF-8 bytes, without source snippets or secrets.
The runtime also rejects semicolons, backticks, call syntax and source-like text
such as the substring import followed by a space, including at the end of a
longer symbol. Text beginning with select, update, insert into, delete from or
create table followed by a space is rejected too, even in ordinary labels.
Use plain factual prose, bare symbols and structured ranges. Rephrase descriptive
labels when necessary. A prose rejection does not justify changing the schema.
Keep within the actual schema bounds (32 flows, 256 total steps, 128 references).
Use descriptions for conditional paths and unknowns; do not invent progress or
coverage states. If detail exceeds limits, report the unfinished scope to the
coordinator instead of silently discarding threats.

A save rebinds all references to current file bytes. First read and inspect every
changed/missing pointer, including retained test/rule references. Never save old
analysis simply to refresh stale fingerprints. If a referenced file is missing,
report the unresolved pointer and leave the prior bundle intact until the owner
resolves it; do not create a placeholder or silently drop the reference.

Issue all Rig MCP calls sequentially, including reads. On an operation-busy error,
wait for the outstanding call to finish, then retry the unchanged call. Busy is
not missing data and is not a failed save receipt. There is no
automatic merge for one area.
After success read the area again, compare IDs/links and retained metadata, and
inspect any unexpected change. On a lost response, read before retrying. Unknown
area, schema error or missing MCP stays incomplete. Correct a rejected request
using the actual schema; never reset state, substitute SQL or claim success.
