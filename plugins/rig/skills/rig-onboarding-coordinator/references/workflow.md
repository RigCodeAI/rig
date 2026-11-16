# Save analysis and read progress

Use the same project/worktree and RIG_HOME for every worker. Discover live schemas.

| Tool | Purpose |
| --- | --- |
| rig_analysis_save_application | Save the shared application map and named areas |
| rig_analysis_save_area | Save one area's complete writable bundle |
| rig_analysis_list_areas | List saved areas |
| rig_analysis_read_area | Read one area, its shared definitions and evidence |
| rig_analysis_progress | Read saved detail counts and current finite evidence |

The equivalent CLI is `rig analysis save-application`, `save-area`, `list-areas`,
`read-area` and `progress`; save inputs use --input FILE or --input -.

The root host agent owns assignments, worker limits, stopping and re-delegation.
A worker reads its assigned area, preserves earlier records, saves partial analysis
and reads it back. A new agent can continue the same area directly in a fresh session.
After an uncertain response, read first. Give the next agent saved IDs, inspected
source scope, evidence and explicit remaining work. Do not use a test launcher as
product setup or change global host settings to route workers.

Area saves replace that area's bundle; omitted arrays become empty. Keep shared
protection_links and local tests/rule/evidence references. Filter derived fields.
Use the last inspected bundle_digest as optional expected_bundle_digest to reject
an intervening local edit. Use exact expected_revision for shared definition edits;
these compare data, not worker identity. Never copy a foreign definition.

Progress accepts {} or {"offset":0,"limit":100}. Follow next_offset,
qualification_next_offset and protection_next_offset independently until null.
An area with no details is unexplored; saved means partial descriptions are present.
Read details to decide what remains. Neither state establishes stage completion.

The current source snapshot and reference freshness expose changes. Immutable caller
observations keep their original source/test/context binding; new source or changed
inputs can stale them. Never silently refresh old conclusions. Counts distinguish
saved requirements, explicit area pairs, qualified detector references and supported
caller evidence. The existing generated-check authority alone qualifies/activates.
A helper pass cannot fulfill another caller; failed/incomplete checks and pending
plans/proposals stay unresolved. No count proves general security coverage.
