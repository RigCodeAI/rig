# Four-stage project onboarding

Keep the default rule pack and existing owner rules as background protection.
Custom-rule work starts from applicable application threats. Do not require a
current flaw or a demonstrated default-pack miss before authoring.

| Step | Skill | Saved result |
| --- | --- | --- |
| A | [Application map](../../rig-application-map/SKILL.md) | Components, actors, assets, areas and broad flows |
| B | [Area threat model](../../rig-area-threat-model/SKILL.md) | Applicable threats and required protections |
| C | [Area code flows](../../rig-area-code-flow/SKILL.md) | Actual callers, helpers, paths and source references |
| D | [Threat rules](../../rig-threat-rule-creation/SKILL.md) | Tested rule/test/evidence references and explicit limits |

Normal setup runs [the onboarding coordinator](../../rig-onboarding-coordinator/SKILL.md).
It reads progress first, reuses baseline setup, saves/readbacks the whole requested
map, then the root host agent delegates B–D through native `spawn_agent` or host
delegation, using saved area and protection IDs. Use at most three area workers,
or serial work when native delegation/separate bound MCP sessions are absent.
Rig stores analysis and evidence; the root host agent handles assignments and continuation.
Experiment launchers are test tooling only. Existing private evaluator
workers remain a separate qualification boundary.
One writer owns each area. Only the coordinator replaces the shared map.

Discover the real analysis MCP schemas in the current runtime. Use
one bound project/worktree and external state directory across stages. No SQL,
direct database access, CLI fallback or replacement JSON progress store. Missing
tools retain baseline scans and an explicit incomplete-onboarding result.

Workers read saved areas, preserve earlier records, save partial analysis directly
and read back. The root reads progress after each return or stop and assigns a new
agent to continue missing work. Keep budgets and spent evaluation attempts; saving
analysis grants no rule qualification or activation.

Stage D reviews every area/protection membership; it does not need one rule per
risk. Link canonical requirements across areas, preserving maintenance ownership
and local caller paths/tests/results. Shared-helper success alone never supports
every caller. Read [shared requirements](../../rig-onboarding-coordinator/references/shared-protections.md).
Every applicable threat needs a requirement or an explicit unsupported reason.
Empty analysis is not evidence that no threats apply.

All area saves replace complete bundles: preserve prior-stage records and stable
IDs, filter derived fields/other-owned risks, and read back successful saves.
Reinspect changed source before refreshing references. A database link is not proof
that a rule ran or protects the area. Do not use counts as completion or coverage.

Do not require A/B to certify helper safety. C supplies source-grounded behavior so
D does not blindly exempt misleading helpers. D's independent tests judge detection
and allowed alternatives for a precise threat. Keep unsupported scope visible;
a narrow API-misuse detector is not general authorization proof.

Use existing Rig qualification and activation APIs; development tests alone do not
activate generated checks. Runtime capability/permission failures remain incomplete.
Never claim optional direct-scanner success proves normal Rig behavior with different
options. Preserve finite-scope conclusions and avoid whole-app security claims.

Report saved areas, qualified rules, unqualified candidates, unresolved threats,
source/engine limitations and observed normal-scan results. Reuse the ordinary setup
report where supported, using current saved analysis and actual check outcomes. Query all progress pages
before final reporting and name each unresolved area/protection and exclusion.
Genuine qualification and activation remain separate existing Rig outcomes.
