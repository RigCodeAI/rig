# Advanced onboarding (paused)

Retained for future reintroduction. Normal setup and routine code changes must not
enter this workflow. Use it only after the owner explicitly re-enables advanced
onboarding; a setup request alone does not enable it. Existing rules and saved
analysis remain intact.

Use this for “set up Rig/security scans” and project-specific setup/update offers.
Use the customer's existing agent and installed Rig MCP tools. Users describe the
outcome; the agent handles the supported operations below. The root host agent
creates onboarding area subagents using native `spawn_agent` or delegation, up to
three by default. Rig stores saved analysis and evidence.
Without host delegation, process the saved areas serially. Private evaluator workers
remain separate from these onboarding area subagents. Read the sibling
[rig skill](../rig/SKILL.md) for execution reviews, saved-check reuse and receipts.
The automatic evaluator beta currently requires Codex ChatGPT authentication,
macOS sandbox-exec and Python 3.11+, Bash and available project runtimes. The qualified example is Python
and Bash; other repository/OWASP coverage remains unverified. Unsupported
environments retain baseline scans and explicit inactive generation gaps.
Configuration and report saves need owner authorization. Existing ordinary scanners need
no Rig execution approval or automatic grant; generated application checks must
first satisfy the independent qualification gate in [generation](references/generation.md); host tool trust still applies. Other
repository commands retain their exact execution approvals.
Reuse authorization already supplied for its actual scope; do not ask again while
the same execution binding is current. An authorized setup includes ordinary development tests, independent evaluation,
and automatic advisory activation of generated checks that pass the agreed policy.
Keep human policy review out of that loop; use the existing review/apply APIs
mechanically under that authorization. Required enforcement and hook installation
remain separate choices.

Evaluate a frozen generated rule with `rig_evaluate` and {"id":"CHECK"}.
Rig freezes current candidate/source/tool bytes, launches a separate fresh local
source-only evaluator, freezes its runtime-checked examples, and grades the rule
through native Rig. The CLI owns qualification, saved state and automatic advisory
adoption under setup authorization. No server, infrastructure, new credentials or
per-rule human review is required. Existing caller permissions still apply.
The decision, fixed safe summary and closed diagnostic codes reach author-facing
Rig tools/reports. Read the diagnostic's stage, reason, owner, missing evidence
and next action. A tester/runtime failure leaves the rule ungraded; do not rewrite
it to fix missing infrastructure. For a completed miss or safe alarm, improve the
rule using concrete public development examples before any allowed fresh grade.
Saving, public testing, independent qualification, adoption and normal execution
are separate observations. Exact saved-request retrieval never retries work.
Do not run private verifier scripts as ordinary public checks, inspect hidden
artifacts, or tune a rule from detailed private results. If details were exposed,
call rig_evaluate with {"id":"CHECK","exposed":true}; the collection is retired.

This is fresh-context separation and output filtering, not hostile-user filesystem
isolation. The same OS user or unrestricted file/shell tools can read local worker
artifacts. State this limitation honestly; do not require external isolation or
server provisioning to run this local workflow. Missing runtime/worker evidence
remains incomplete and inactive. Rejected rules are valid outcomes: preserve the
gap and continue rather than rerolling until one passes.

For a per-file preparation, parser, size or timeout failure, retain findings and
completed work and continue unaffected checks/areas. Read input_preparation,
coverage_gaps and execution_limits. Preserve binary assets for behavioral tests;
never remove source, silently narrow scope, raise limits or claim skipped files
were analyzed. Missing required evaluation inputs leave that rule inactive.
Apply supported repairs under the existing setup authorization; ask only when
actual host permissions or additional scope require it. Retry only after recording
a concrete public-input/tool change. Keep at most three public repair/development
runs per affected obligation across sessions and the existing worklist/private
attempt and time budgets. Before each run, persist the operation, input identity,
change, spent count and unresolved gap in the canonical assessment's remaining_gaps
and save the partial report. Resume from that report and read existing worklist,
analysis and evaluation requests first; a new session never resets an allowance.
If unchanged, unsupported or exhausted, save the gap and continue other eligible
work. Retrieve spent evaluation requests without relaunching them.

Read-only discovery, candidate previews and GrepRules calls use `rig_setup` with
an arguments array. It cannot apply configuration or grant execution. Saving uses
`rig_manage` command setup with the same selection plus --apply --digest. The host
may independently review writes; never change tool annotations or permissions to
avoid review. Preserve the caller's execution policy, including never/read-only.
If the host denies required work, explain that operation in the calling conversation
and stop it; retry only after supported caller approval. Do not switch to automatic
review, weaken sandboxing, or repeatedly launch a denied worker. See generation.md
for the shared native worker lifecycle and its platform limits.

Before preparation or writes, read [the coordinator](../rig-onboarding-coordinator/SKILL.md)
and query saved analysis progress through MCP. Read existing details and preserve
spent evaluation attempts before continuing missing work.
After the user authorizes initial setup, call rig_manage command setup with
arguments ["--begin"] before saving configuration. Read ["--lifecycle"] through
rig_setup on resume. Only a new project without established policy/report can
enter this one-time initial phase. Automatic application enforcement waits during
it; manual scans and development tests remain usable. Existing/completed projects
never reenter this pause when a rule is updated. The entire root .rig directory is
Rig authoring output, excluded from application source; specific explicitly loaded
rule/test bytes still keep their own identity and trust requirements.

Use steps 1–5 below only for missing or explicitly updated baseline setup, then
return to the coordinator. Missing analysis tools leave project onboarding incomplete.

1. Inspect the repository before selecting rules. Use rig_setup with
   arguments ["--project"] for saved checks and metadata inventory. Inspect manifests,
   lockfiles, imports, source roots and representative code with the agent's normal
   file tools. Inventory component languages/frameworks/versions, database APIs,
   request/input APIs, custom wrappers, sanitizers and other security features.
   Read discovery.frontend for React/Next.js, Angular and Vue package evidence.
   Report every discovery.frontend.template_gaps entry with its family, file count
   and example paths. Rig excludes those unsupported templates from saved OpenGrep
   checks and direct OpenGrep scans. Setup continues with the other source files.
   When a connected setup or scan reports a template gap, continue the agent recipe
   workflow in this session. Treat the gap as pending until qualification succeeds
   or the available toolchain and host permissions prevent further progress.
   If Rig splits a large scan into bounded passes, report its cross-file analysis gap.
   Direct-source and
   compiler-required labels are routing evidence, not qualified coverage.
   For React or Next.js, select applicable JSX/TSX OpenGrep rules. Run the
   selected rules on independently expected unsafe and escaped-source controls
   before saving the normal opengrep-default check. Verify the unsafe original
   path and line and the absent safe finding. Save through the usual candidate
   preview/apply flow, then run the saved check in a fresh agent session.
   React and Next.js use their original JSX/TSX source; do not compile them
   merely to obtain a template result. Report missing validated rules as gaps.
   For Angular or Vue, call rig_setup with ["--frontend", "angular" or "vue",
   "--project-root", "RELATIVE_ROOT"] for read-only compiler diagnosis.
   Inspect the installed version and lockfile before proposing any package command.
   Use the connected agent's configured host permissions for installation.
   If the host permits the install, continue without another Rig approval prompt.
   If the host requires approval, use its normal permission flow.
   Rig itself never installs dependencies. After a concrete repair, use an explicit whole-project check
   tool on the configured frontend check. Limit unsuccessful repair attempts to
   three. Rig stops repeated failed qualification of the same reviewed source
   after three attempts. Inspect its structured stage and diagnostics. Ask the
   user for help when the limit is reached. A changed command or toolchain needs
   a new preview and review. If no agent is connected, report the CLI gap.
   After selecting a generated-code rule and independently expected controls,
   preview qualification with rig_setup arguments ["--frontend", FAMILY,
   "--project-root", ROOT, "--check-id", NEW_ID, "--rule", RULE_FILE,
   "--unsafe", UNSAFE_FILE, "--safe", SAFE_FILE, "--expected-rule",
   RULE_ID, "--expected-line", LINE, "--runtime", NODE_PATH].
   Add ["--strategy", "build"] only when direct compilation is unsuitable.
   The preview names the compiler command, source scope, controls and digest.
   After the owner approves that command and policy addition, call rig_manage
   setup with the same arguments plus ["--apply", "--digest", DIGEST].
   Rig compiles the whole selected frontend, runs OpenGrep and checks the
   independently expected unsafe and safe locations before saving one advisory
   check in .rig/checks.toml. A successful qualification does not itself prove
   that a fresh normal scan has run. Review the saved compiler recipe with
   rig checks review --id ID, then obtain owner approval for its current digest
   with rig checks approve --id ID --digest DIGEST. This local execution approval
   applies to direct compilers and project builds. Use rig_manage checks run --id ID --whole-project for a current full-check receipt.
   For an unsupported template family, inspect its package declaration, source
   syntax, installed compiler and build scripts. Use host permissions when
   installing tooling. Propose an exact JSON recipe with argv, template_paths and
   metadata_inputs. argv must name an installed executable, avoid a shell and
   contain {rig_output} once as a separate argument. A project-specific wrapper
   may compile templates when the installed tool lacks a direct output option.
   Show the wrapper source and exact command to the owner before execution.
   The compiler must emit fresh JavaScript and adjacent source maps that point
   to every listed original template. Select independent unsafe and safe
   templates with a rule that distinguishes them. Preview with rig_setup using
   the Angular/Vue qualification arguments, replacing --runtime NODE_PATH with
   ["--strategy", "agent", "--recipe", RECIPE_PATH]. Rig rejects a recipe
   that selects paths outside the detected unsupported family. Obtain explicit
   owner approval of the proposal before rig_manage setup --apply --digest.
   The owner's reviewed proposal approval also approves the saved agent recipe.
   Reuse that approval after template edits while the command, toolchain, rule,
   policy and declared metadata stay unchanged.
   Obtain a separate owner host grant before automatic hook execution. Run the saved
   check and a direct OpenGrep scan. If qualification fails, leave the gap visible, inspect
   Rig's stage and diagnostics, and ask the owner after three failed attempts.
   Read existing .rig/checks.toml, .semgrepignore, local rules and intentional
   exclusions. Preserve user choices. Do not execute project configuration to infer
   facts. Mark dynamic or unresolved facts unknown with evidence locations.
2. Keep the prepared/default pack as background protection. Do not audit its coverage
   or prove a default-pack miss before creating project-specific rules. Optional
   community-rule discovery uses [discovery API](references/greprules.md) only when
   useful or requested; inspect actual compatibility and preserve provenance.
3. Preserve existing protective rules, profiles and owner choices. Add project rules
   without silently replacing or narrowing the configured selection. Conflicting IDs
   and changes to existing policy use the supported review/apply path.
4. Preview through rig_setup arguments ["--candidate","opengrep-default",
   "--rules","RELATIVE_LOCAL_RULE_FILE"]. This explicit local selection uses the
   prepared OpenGrep executable and does not borrow a globally registered model.
   For an existing reviewed compatible profile, append ["--application-model",
   "RELATIVE_PROFILE_JSON"]. Alternatively, omit both overrides to import the
   prepared scanner's full selection. Never silently strip its application model
   to make setup pass. Profiles are optional, API/layout-specific capabilities;
   SQL usage or TypeScript alone does not make a project compatible. The current
   juice-shop-search-v1 profile models only the reviewed search contract and needs
   pinned owner-provided Node/TypeScript. Its verifier and base rule ship in Rig.
   Inspect compatibility first; missing supporting tools require explicit preparation.
   No hardcoded application checkout paths or universal SQL model assumptions.
   Optional repeated --target RELATIVE_PATH restricts scanner targets; omit it for
   the full project. Carry deliberate scope/exclusions into the profile/report.
   Do not narrow targets to hide failures; retain full-scan errors as uncovered areas.
5. Show the exact proposal and obtain any missing save authorization, then repeat
   the same selection with --apply --digest TOKEN. If a host restart changes only
   transient PATH entries, preserve the execution_path already reviewed by
   supplying --execution-path with that proposed configuration value on preview
   and apply. Do not invent this value, remove tool/security wrappers or silently
   substitute the new ambient PATH. Changed reviewed settings need owner consent. Rig freezes rule/profile bytes,
   writes configuration last and refuses changed inputs or conflicts. It preserves
   existing checks/settings. For already configured checks, resume review/status
   without rewriting policy. Updates requiring replacement need owner review; do not
   remove policy or rename checks to bypass it. Use rig_review and rig_check through the rig skill. Do not call rig_approve or
   ask for scanner execution permission; only other repository commands need
   owner-approved execution digests. Supporting tool
   changes require repair/review. Never manually edit approval storage.
6. Run [the onboarding coordinator](../rig-onboarding-coordinator/SKILL.md) using
   [the four-stage flow](references/onboarding.md). Installing defaults is preparation.
   Save/read back the whole requested map, then use the durable area/protection queue
   for threats, code paths and independently tested rules. Resume existing work first,
   The root host agent delegates the area work through its native tools, then
   reviews saved outcomes after each worker and continues ready work within budget.
   Link shared canonical requirements without copying definitions; every applicable
   area keeps its own caller tests/results and adopt/create/replacement decision.
   Shared-helper success alone cannot cover every caller. Retain pending shared work,
   conflicts, unsupported threats, failed candidates and exact exclusions as gaps.
7. Prepare a bounded assessment JSON before scanning, e.g.
   .rig/setup-assessment.json. Read [report finalization](references/coverage.md#finalize-after-execution)
   for the small input shape and supported tool flow. This is an inventory seed,
   not a finalized scan profile. Preserve original/default measures, evidence,
   exclusions, rule provenance and unknowns. Existing historical profile/report
   files may remain as historical assessment inputs; do not present them as current.
8. Review/run supported checks through normal Rig tools, inspect actual receipts,
   then save the report. Partial progress is useful: save even with zero scans or
   failed, stale or inactive checks; keep the partial/unverified state and exact
   gaps/next actions. Missing evidence never becomes a pass.
   rig_setup arguments ["--profile","ASSESSMENT"] previews a canonical customer
   profile and readable report from actual current receipts, runtime and diagnostics.
   Save with rig_manage command setup and those arguments plus --apply --digest TOKEN
   under the user's setup/report authorization. Reports use Rig's existing external
   worktree state, so finalization changes no scan inputs or approvals. Return the
   reported saved paths and concise actual outcomes, metrics and actionable gaps.
   rig_setup ["--report"] discovers saved setup and revalidates freshness. Stale
   inputs/tools, parser failures, timeouts and unknown recognition never become
   coverage. Refresh assessment facts after source/API/dependency/layout changes,
   review changed bindings, re-run, and finalize again. Never manually repair approvals.
   Saving a partial report does not finish initial setup. When the bounded setup
   attempt is finished, explicitly call rig_manage command setup with arguments
   ["--complete"]. Declared gaps and inactive rules are allowed; completion enables
   normal app-change enforcement without qualifying or activating any rule. Do not
   wait for every custom detector to pass before finishing this initial phase.
9. Verify in a fresh native session without earlier conversation. It must discover
   saved checks/report with normal Rig tools, preserve settings and any command
   approvals, perform a new
   scan when supported, and save the updated customer report using its new receipt.
   If unavailable, preserve the partial report and exact next action; fresh-session
   readback is useful progress and does not authorize evaluator retries. Rebind any
   finding mappings only after checking matching rule/location evidence in that new
   receipt; old result IDs cannot verify a new observation. Saving a report enables
   automatic receipt refresh for unchanged inventory. After new scans, confirm
   --report returns saved_report_current=true; changed source still requires
   automatic reassessment and a normal updated profile save. End with
   rig_finish. Historical reports/receipts do not count as new execution. Report
   unavailable fresh-session verification explicitly. Configuration coverage is
   not vulnerability recall or a security guarantee.

Small rule adaptations require maintained vulnerable/safe examples on the installed
engine and declared limits. Route supported authoring through the existing rig skill.
Behavior-grounded generation reuses existing authoring and scan machinery; it
creates development tests and independently generated runtime-checked qualification
data automatically. Unsupported semantics and unqualified candidates remain gaps;
never substitute an engineer-preparation requirement for this automatic workflow.

Application profiles may execute only the reviewed external Node/TypeScript runtime registered in user scanner configuration. Repository-owned profile JSON is not helper trust. A missing or mismatched user registration fails clearly; use the normal explicit scanner registration flow after reviewing the runtime rather than changing state by hand.

Application-model checks do not support task-differential attribution. Run the complete saved check without a task handle; Rig explicitly fails the differential path rather than silently omitting the model. Report that limitation when task-scoped feedback is requested.

Setup-wide scanning must use `rig_manage` command `checks` with arguments
`["run", "--id", "ID", "--whole-project"]`. Routine `rig_check` requests
require explicit files or the existing task handle; unsupported narrow adapters
return unverified without broadening execution.
