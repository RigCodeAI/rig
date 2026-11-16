# Actual analysis-tool update contract

Read [save and progress operations](../../rig-onboarding-coordinator/references/workflow.md).
Read your assigned area, preserve earlier work and save partial analysis directly.
Include the inspected bundle_digest as expected_bundle_digest to reject stale edits.
Shared definition changes use exact expected_revision. Read back after saving.
The root host agent handles assignments and continuation.


Verified against src/analysis/interface.rs and docs/database-mcp.md in this checkout.
Discover live schemas before use; host prefixes can differ. Issue Rig MCP calls
sequentially on each server connection. On an operation-busy response, wait for
the outstanding call to finish, then retry the unchanged call. Busy never means
missing data. Operations are
rig_analysis_save_application, rig_analysis_save_area, rig_analysis_list_areas and
rig_analysis_read_area. Step B uses read/list/save-area; only the coordinator saves
the application map. Use the same project root and RIG_HOME across sessions.

Read: `rig_analysis_read_area` with `{"id":"download"}`.
Read [shared requirements](../../rig-onboarding-coordinator/references/shared-protections.md)
for canonical ownership, memberships and revision rules. Build the complete writable
replacement, including preserved `protection_links`, the inspected `bundle_digest` as optional `expected_bundle_digest`:

- area: id, name, description.
- elements: local elements, id, kind, label, description.
- flows: id, label, description, steps. Preserve step order and optional transfer,
  role, element_id, reference_id, explanation.
- risks: use owned_risks for owned definitions only. Retain id, description, harm,
  priority, assumptions, asset_ids, affected_area_ids. Map read revision to
  expected_revision, using 0 for new shared definitions, and omit derived
  owner_area_id/revision. Do not copy foreign risks.
- protection_requirements: owned id, statement, legacy local risk_ids/flow_ids and
  expected_revision as above. Preserve owned definitions consumed elsewhere.
- protection_links: canonical protection_id/definition_revision and local
  risk_ids/flow_ids/path_reference_ids, rule_plan and append-only caller_observations.
  Keep owned legacy risk/flow associations consistent with an explicit owned link.
- references: id, kind, path, purpose, symbol, source_range, test_name, check_id,
  rule_id, protection_id. Omit fingerprint, freshness and check_snapshot.

Do not submit application, worktree_id, bundle_digest, referenced_evidence or evidence_label.
Other-owned definitions remain with their maintenance owner. A foreign risk may be
linked only when its canonical applicability already includes this area; request
an owner update otherwise. Link a shared protection with its exact definition
revision and this area's own associations, without copying its statement. Keep all
local memberships and prior caller results. Stale expected digests/revisions fail
atomically; inspect/reconcile the actual change before rebuilding a request.

Risk has no flow_id or reference_id field: explain its broad path in description
and link the requirement using risk_ids and flow_ids. Requirement has no basis
field: include the basis in statement. Reference purpose explains the observation
or basis, and protection_id links it to the requirement. File pointers are relative
regular files. Reference source_range uses one-based start_line, start_column,
end_line, end_column. Never invent hashes. Rig computes saved fingerprints.

Save tool arguments are that complete replacement,
not a report wrapper.
Success requires isError false and structuredContent.report.saved true, followed
by a successful read. An error has no structured success payload. A disconnected
or missing tool, missing reference, invalid input or uncertain save stays incomplete.

Descriptions are single-line prose, at most 2048 UTF-8 bytes each, with no source
or secrets. This runtime also rejects semicolons, braces, backticks, code fences,
assignment/comparison markers and function-call syntax in text. Use periods and
commas in descriptions. Avoid credential-shaped labels such as authorization
followed immediately by a colon. Plain identifier names belong in pointer fields. IDs use 1–80 ASCII letters, digits, dot, dash or
underscore. Prefix new local IDs with the area ID. Tool schemas give record bounds.
Do not invent analysis statuses, coverage fields or fingerprints.

Changes in references affect earlier analysis too. Do not refresh stale unrelated
records merely to add a threat. Inspect and reconcile the affected earlier claims
or stop and identify the records requiring their owning stage's review.
