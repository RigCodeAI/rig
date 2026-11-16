---
name: rig-onboarding-coordinator
description: Coordinate application mapping, bounded area analysis and rule work using native host subagents and saved Rig analysis.
---

# Coordinate onboarding

The root coding agent maps the app, assigns bounded areas through native host
subagents, and reads saved analysis to decide what remains. Rig stores analysis
and evidence. The root handles stopped workers and re-delegation.

Read [save and progress operations](references/workflow.md) and
[shared protections](references/shared-protections.md). Discover the actual tool
schemas and confirm the worktree/state binding before writing.

1. Use [application mapping](../rig-application-map/SKILL.md) to inspect the app and
   save its map and named areas. Preserve previous analysis. Read/list it back.
2. Read `rig_analysis_progress` and each scoped area. Give each native host worker
   one area, its worktree/state binding, bounded source scope, allowed writes,
   stage links, time/attempt allowance and evidence/return requirements. The root
   avoids overlapping writers in one area. If native delegation is unavailable,
   process areas serially and disclose that boundary.
3. For each area, use [threat modeling](../rig-area-threat-model/SKILL.md), then
   [code flows](../rig-area-code-flow/SKILL.md), then
   [rule creation](../rig-threat-rule-creation/SKILL.md). Read saved earlier details
   to choose the next step. Empty arrays or record counts never establish completion.
4. Workers read the area, preserve its complete writable bundle, save partial
   analysis directly and read it back. Include the inspected bundle_digest as
   expected_bundle_digest to reject a conflicting edit. Shared definition edits
   use expected_revision. Return actual saved IDs, evidence and remaining gaps.
5. After a result, stop, timeout or lost response, read the saved area and progress.
   Assign another agent to continue the missing work directly. Preserve earlier
   partial findings, failures and spent private-evaluation attempts. The root
   controls worker budgets; independent qualification keeps its existing controls.
   Read the saved canonical report's remaining_gaps and worklist before assigning
   recovery. Carry spent public repair/development counts forward (three total
   per obligation), require a concrete change before retry, and save the new count
   before execution. An unchanged failure or spent allowance is a retained gap,
   never grounds to restart the budget in another worker or session.
6. Review every scoped area and every shared protection pair, following all progress
   pages. Keep source/reference changes, exclusions, unsupported scope, failed tests,
   blocked evaluation and budget deferrals visible. Stop affected writers before
   replacing a shared map. Inspect stale evidence before changing references.

A shared definition has one maintenance area and many area links; those links are
saved data. Each caller needs its own invocation, denial and actual test evidence.
Reuse a rule after own applicability tests, create for different behavior, or
propose a new-ID replacement that preserves original bytes/results. Pending shared
work stays an explicit reason and next action; the root handles its ordering.

Do not duplicate rules to raise counts. Safe-looking code still needs threat-driven
protection. No baseline miss is required. Preserve helper-guarantee tests and their
dependencies. Keep at most three public rule-development runs and the existing
qualification attempt/time limits. Do not reset or reroll spent private evaluation.

Report saved analysis, actual qualified/activated checks and exact remaining gaps.
Progress reads the existing qualification authority; saved references and completed
analysis do not qualify or activate rules or prove general security coverage.
Return to rig-setup for its canonical report and fresh-session check.
