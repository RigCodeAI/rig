# Rig map storage

Read [save and progress operations](../../rig-onboarding-coordinator/references/workflow.md).
Read your assigned area, preserve earlier work and save partial analysis directly.
Include the inspected bundle_digest as optional expected_bundle_digest to reject stale edits.
Shared definition changes use exact expected_revision. Read back after saving.
The root host agent handles assignments and continuation.

Inspect live tool schemas first; host prefixes may differ. Use these four native
operations in the same project root and state directory:

Issue Rig MCP calls sequentially, including reads. On “Rig operation busy”, wait
for the outstanding call to finish, then retry the unchanged call. Busy is not
missing data and must never trigger an empty replacement.

| Tool | Arguments | Result in `structuredContent.report` |
| --- | --- | --- |
| `rig_analysis_list_areas` | `{}` | `areas` with stable IDs |
| `rig_analysis_read_area` | `{"id":"AREA"}` | Complete application plus one area bundle |
| `rig_analysis_save_application` | Application object | `saved`, `area_count`, `worktree_id` |
| `rig_analysis_save_area` | Complete area bundle | `saved`, `area_id` |

There is no separate application-read operation. Read any saved area to retrieve
the complete shared application. An empty list does not distinguish an absent map
from an existing map with zero areas. If preserving unknown existing map contents
matters, stop and explain this read limitation instead of assuming an empty map.

The application accepts `summary`, `scope`, `source_revision`, `elements`, `areas`.
Use an inspected commit plus a truthful dirty/scope note for `source_revision`;
it is a description, not a verified fingerprint. Application elements accept
`id`, `kind`, `label`, `description`. Kinds: `actor`, `component`, `asset`,
`external_service`, `data_store`, `trust_boundary`. Areas accept `id`, `name`,
`description`; place area starting paths, source exclusions or unknowns here when
they have no dedicated field. All IDs must follow the live schema's limits.

Area bundles accept `area`, `elements`, `flows`, `risks`,
`protection_requirements`, `protection_links`, `references`, plus current
optional `expected_bundle_digest`. Flows accept `id`, `label`, `description`,
`steps`. Steps have positive distinct `order`, `label`, and optional `transfer`,
`role`, `element_id`, `reference_id`, `explanation`. References accept `id`, `kind`,
`path`, `purpose`, optional `symbol`, `source_range`, `test_name`, `check_id`,
`rule_id`, `protection_id`. For new map evidence use `code` or `documentation`;
paths are existing repository-relative files. A supplied range requires all four
one-based fields: `start_line`, `start_column`, `end_line`, `end_column`.
Rig fingerprints the actual file. Never submit invented fingerprints.

Verify ranges against the actual text, including columns. The selected range must
contain the statements supporting its purpose and linked flow steps. A function's
name or the first character of its final line does not support a broader behavior
claim. For whole-line evidence, read the complete lines and derive the final column
from the actual final line length. Do not use a constant placeholder end column.
Read-back validation checks both pointer validity and support for the mapped fact.

Write short, single-line prose in descriptive fields, not code snippets. The
current runtime conservatively rejects some ordinary punctuation and phrases:
semicolons, backticks, braces, call-like text with parentheses immediately after
a name, assignment/comparison syntax, the substring `import ` even at the end
of an identifier, and prose starting with `select ` or `update ` among others.
Use periods between sentences and place bare symbols and file paths in pointer
fields. Use “Choose” for selection steps and describe file/archive ingestion in
everyday words. Keep the same facts. Do not discard scope or unknowns to get a save
accepted. If a prose-only request
still fails, retain the error, read current state and report the contract blocker.

## Preserve before replacing

Application saves replace the entire shared map and area list. Retained area IDs
keep their details; omitted areas lose theirs. Preserve unrelated areas and all
shared elements needed by saved flows or risks. Do not delete or rename prior
records merely because they are outside today's scope. If removing an element
still used by retained analysis, stop and coordinate instead of bypassing rejection.

Area saves replace the entire owned bundle; omitted arrays become empty. Read
first, then project only writable fields listed in the live schema. In particular:

- Extract writable `application` fields for a map save and rebuild the complete
  `areas` list from list/read results; application reads do not include that list.
  Do not submit the whole read response.
- Map canonical read revision to expected_revision for owned shared
  definitions, using 0 for new ones. Preserve all local protection_links and
  foreign memberships without copying definitions.
- Remove derived `owner_area_id`, `revision`, `fingerprint`, `freshness`, check_snapshot, counts,
  `referenced_evidence`, `evidence_label`, `bundle_digest`, worktree IDs and response envelopes.
- Read responses include shared risks owned by other areas. Submit only risks
  from `owned_risks`; retain each owned risk's complete
  `affected_area_ids` including shared links. Do not take ownership of others' risks.
- Preserve existing local elements, flows, risks, requirements and evidence;
  reuse their IDs. Add/update only map-owned descriptions, flows and pointers.
  If ownership of a flow/reference is unclear, preserve it and use a distinct ID
  for the new broad map flow, or stop if the intended replacement is ambiguous.
- Freshness is derived on reads. Re-saving a reference fingerprints current bytes.
  Never silently make stale downstream analysis look current. If any preserved
  reference is changed/missing, leave that bundle untouched and report an explicit
  refresh blocker. Re-inspect and refresh only records within the authorized stage.

Success requires `isError` false and the documented save report, followed by
list/read reconciliation. A tool call returning text is not enough. On rejection,
retain the error and compare saved state before correcting schema or links. On
timeout/disconnection, reconnect to the same root/state and read before retrying.
The root coordinates one writer per area.
There is no automatic merge of area bundles.

The four tools save descriptions and pointers only. Test/rule links are references,
not verified coverage. This stage does not run scanners or activate policy.
