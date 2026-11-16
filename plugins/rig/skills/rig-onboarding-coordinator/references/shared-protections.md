# Shared requirements, local caller evidence

Read the live analysis schemas before writing. A canonical protection requirement
has one maintenance owner but can apply to several areas. Ownership decides who
edits its statement; it does not decide which callers are protected. Keep one
canonical definition and a separate `protection_links` entry for every applicable
area. One passing helper test never proves all callers invoke and honor that helper.

## Read and preserve

`rig_analysis_read_area` returns local flows/references, `owned_risks`, owned
`protection_requirements`, all `applicable_protection_requirements`, local
`protection_links`, and `bundle_digest`. Applicable definitions have canonical ID,
statement, `owner_area_id` and `revision`. Risks include owner and revision too.

For `rig_analysis_save_area`, preserve the complete writable local bundle and links:

- `risks` contains only owned definitions. Use `owned_risks` to preserve owned risks
  even when they are not locally applicable. Never copy another area's definition.
- `protection_requirements` contains only owned definitions. Preserve each definition
  and its legacy local `risk_ids`/`flow_ids` even when other areas use it.
- On new or shared definitions, set `expected_revision` to 0 for new
  records or the exact read `revision` for existing ones. Strip `revision` and
  `owner_area_id` from inputs. Supplied mismatches always fail. Unchanged semantic
  resaves keep revisions; statement changes advance protection revisions.
- Preserve the full current area's `protection_links`. This array replaces local
  memberships only. An omitted link unlinks that area's obligation, retaining its
  observation history; it does not delete other areas' records. Do not unlink to
  hide a failed caller or to bypass a stale definition.
- Preserve local elements, flows, reference IDs and owned risks' `affected_area_ids`.
  A foreign risk can be linked only if its owner already included this area in
  `affected_area_ids`. Ask that owner to extend applicability when missing.
- Include the latest inspected `bundle_digest` as optional `expected_bundle_digest`. Compare-and-save happens inside
  the transaction. A stale digest/revision fails atomically: read and inspect again,
  reconcile the real change, then rebuild. Never simply substitute a newer digest.

Do not resubmit derived fields or the whole read report. Strip fingerprints,
freshness, caller captured bindings/status projections and result labels. Rig binds
the local digest to relevant canonical semantic revisions and saved file hashes;
another area's membership addition alone does not authorize rewriting its data.
Owner definition deletion or owner-area removal is rejected while consumers remain.
Never take over a shared definition to avoid that failure.

Every supplied reference is fingerprinted again. Inspect changed/missing pointers
and their claims before saving; leave unresolved earlier analysis unchanged. A new
read or replay must not refresh evidence's original captured binding.

## Area-to-requirement link

Each `protection_links` item has:

| Field | Input |
| --- | --- |
| `protection_id` | Existing canonical ID, not a copied definition |
| `definition_revision` | Exact canonical revision, at least 1 |
| `risk_ids` | Local or explicitly applicable risk IDs |
| `flow_ids` | This area's flow IDs |
| `path_reference_ids` | This area's code/evidence reference IDs |
| `rule_plan` | Kind/reason and applicable fields below |
| `caller_observations` | New bounded observations below, append only |

Owned legacy associations and an explicit owned link's risk/flow arrays must agree.
References may use a canonical `protection_id` when this area has that membership.
A stage refines its own paths/evidence, not the shared statement or another area's
results. When preserving a link, rebuild only its writable fields; omit derived
observation projections/bindings and append only new observations. Earlier stored
observations survive omission. Report definition changes to the maintenance owner and coordinator.

## Choose a rule plan without duplicating work

A `rule_plan` requires `kind` and a factual `reason`:

- `pending`: retain the exact missing work. Name any shared analysis still needed in the reason; the root agent decides its order.
- `adopt_existing`: use actual `check_id`, local `rule_reference_id`, and
  `applicability_test` with actual `check_id`, `result_id`, `test_reference_ids`.
  First run this area's own caller/path contrasts through an ordinary Rig check.
  A helper receipt, another area's tests or a qualified detector alone cannot adopt
  it for this caller. Independent detector qualification is still separate.
- `create_new`: explain the different behavior requiring a new detector. Preserve
  caller tests and use genuine qualification. A new area/owner alone is no reason
  for a duplicate rule, and no rule-count quota applies.
- `propose_replacement`: use a new check ID and rule path, distinct from the original.
  Require `rule_plan.rule_reference_id` for the new rule and `applicability_test`
  with actual `check_id`, `result_id`, `test_reference_ids`, backed by an exact
  current satisfied ordinary receipt. Preserve the original captured snapshot
  while refreshing development tests or the reason.
  `replacement_of` names original `check_id`, `expected_check_sha256`,
  `expected_rule_sha256`, and optional `expected_result_id` from its factual public
  snapshot described below. Preserve the captured original snapshot, bytes and results. The candidate
  may be unregistered or a configured inactive generated check; an already active/
  qualified replacement is not a proposal. Never silently supersede or activate it.

Before a replacement proposal, save your own `sast_rule` reference to the original
registered check with a `pending` plan, preserving the area. Read it back:
`references[].check_snapshot` supplies `check_id`, `check_sha256`, `rule_path`,
`rule_sha256`, `result_id`, `result_state`, `result_current`. Copy the actual check/
rule hashes and optional selected original result ID into `replacement_of`. Missing
facts are nullable: retain a gap rather than invent them. This is a closed factual
read, not raw/private output or new qualification. Never submit `check_snapshot`
in saves; it is derived and excluded from bundle/stage digests.

Analysis saves neither evaluate nor change policy. The normal evaluator can adopt
passing checks: do not use it to activate a replacement while merely recording a
proposal. Later promotion needs its separate explicit authority. If original bytes
or the replacement's external activation change, retain the reported conflict.
A later ordinary result alone does not erase the original snapshot or prove a
replacement conflict. Only the assigned writer changes shared rule packages/config;
other areas retain links and local tests, requesting work rather than overwriting.

## Caller observations are separate from helper guarantees

Append a `caller_observations` item with unique `id`, `outcome` and `reason`.
Outcomes are `supported`, `contradicted`, or `unknown`. Use this area's
`invocation_reference_ids`, `denial_reference_ids`, `test_reference_ids`, plus actual
`test_check_id`/`test_result_id` when available. References must support the actual
caller invoking the protection and stopping the sensitive action on denial.

`supported` needs all three reference kinds and a current complete successful
ordinary receipt bound to those exact tests. `contradicted` can use a current
complete successful or violation receipt showing the declared failure; it remains
unresolved. `unknown` can lack a receipt and remains a gap. Use
[the caller-test route](../../rig-threat-rule-creation/references/caller-tests.md).

Rig captures source, definition revision, caller context, references and closed
receipt identity. Repeating the same observation ID/payload preserves its original
binding; it cannot refresh stale evidence. Changed payload with the same ID fails.
Append a new ID for corrections or disagreement; omitting an old observation never
deletes it. Current supported and contradicted observations mean a conflict, not
permission to choose the convenient result. Missing/stale evidence stays unresolved.
Bound saves to 16 new observations per link and 16 IDs per reference kind.
