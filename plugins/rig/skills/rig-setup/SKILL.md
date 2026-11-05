---
name: rig-setup
description: Configure or update Rig SAST for a repository by inspecting its stack and APIs, discovering compatible GrepRules community rules, saving reusable checks, and reporting evidence-backed configuration gaps.
---

Use this for “set up Rig/security scans” and project-specific setup/update offers.
Use the customer's existing agent and installed Rig MCP tools. Users describe the
outcome; the agent handles the internal APIs and tokens below. Read the sibling
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

When acting as the separate rule author after independent comparisons exist,
skip broad project/status inspections. `rig_inspect` project views and broad status
responses include ordinary command receipts, including private-comparison output.
Use the supplied obligation/public facts and repository files, then id-scoped
`rig_review` and `rig_check` for your own helper tests, baseline and development
runner. Do not inspect the existing/private verifier IDs or their histories.
Broad report/status inspection belongs after the candidate is frozen or the attempt
has closed. This is trusted-role separation, not hostile-agent isolation. If
independence or capability evidence fails, preserve it, leave the check inactive
and continue; no engineer approval or hand-written qualification program is needed.

Read-only discovery, candidate previews and GrepRules calls use `rig_setup` with
an arguments array. It cannot apply configuration or grant execution. Saving uses
`rig_manage` command setup with the same selection plus --apply --digest. The host
may independently review writes; never change tool annotations or permissions to
avoid review. The agent uses supported on-request host approval, not a never policy
that rejects required approvals.

1. Inspect the repository before selecting rules. Use rig_setup with
   arguments ["--project"] for saved checks and metadata inventory. Inspect manifests,
   lockfiles, imports, source roots and representative code with the agent's normal
   file tools. Inventory component languages/frameworks/versions, database APIs,
   request/input APIs, custom wrappers, sanitizers and other security features.
   Read discovery.frontend for React/Next.js, Angular and Vue package evidence.
   Report its EJS, Handlebars and Pug template gaps. Direct-source and
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
   Show the exact install command, changed project files and script behavior, then
   obtain explicit user approval before installing. This consent does not approve
   a project build command. After a concrete repair, use the existing rig_check
   tool on the configured frontend check. Limit unsuccessful repair attempts to
   three. Rig stops repeated failed qualification of the same reviewed source
   after three attempts. Inspect its structured stage and diagnostics. Ask the
   user for help when the limit is reached. A changed source or command needs
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
   applies to direct compilers and project builds. Use rig_check for a current receipt.
   Read existing .rig/checks.toml, .semgrepignore, local rules and intentional
   exclusions. Preserve user choices. Do not execute project configuration to infer
   facts. Mark dynamic or unresolved facts unknown with evidence locations.
2. Read [targets and measures](references/coverage.md). Decide target applicability
   from actual features. Search current GrepRules using public language/framework/API
   and CWE terms only. Read [discovery API](references/greprules.md), then search,
   inspect actual matching logic/metadata and fetch suitable artifacts through Rig.
   CWE tags, quality scores, pack membership and zero findings establish no coverage.
   Keep missing rules, empty/incomplete results and service errors explicit. Do not
   fall back silently to another online provider or build a local discovery catalog.
3. Select compatible community rules first; retain existing protective rules and
   local owner rules even if they have no current findings. Inspect the prepared
   selection before overriding it: if its rules/profile apply, retain all protective
   rule definitions and the compatible profile when adding community rules. A small
   new selection must not silently replace the applicable prepared pack. Replacing
   protection needs a concrete separate owner decision. Rig-reported prepared rule,
   profile and supporting-tool paths are legitimate setup inputs; inspecting them
   is distinct from reading earlier scan reports, grading oracles or conversations.
   Pin selected bytes and
   preserve provenance, license, retrieval time, upstream identity/revision/digest,
   rationale and source/sink recognition evidence. Save fetched YAML using the agent's
   normal file tools in a new project-owned file after configuration authorization.
   Combine rules without dropping existing definitions; conflicting IDs need review.
   Validate with the installed engine and representative positive/negative cases.
   Missing tests or metadata remain gaps; a scan alone is not rule qualification.
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
6. Work through ALL identified applicable app-layer OWASP Top 10 2025 gaps,
   using [behavior-grounded generation](references/generation.md). Begin with a
   source-only --inventory discovery and persist its full inventory/obligations
   through --worklist. Inventory accounts for all ten categories; it is not verified
   coverage. Group overlapping obligations; never force one rule per category.
   Resume saved current work first. Claim each next_gap before spending effort.
   Independently test compatible existing rules first; generate only where they
   fall short. Establish actual helper behavior, develop a bounded candidate and
   independently qualify frozen bytes through real Rig. Setup authorization covers
   automatic advisory activation of passing checks. Failed checks stay inactive:
   preserve results, finish their queue entry, then continue the next gap. Never
   tune on withheld cases or retry unchanged failed obligations for perfection.
   Default ceiling: eight gap attempts, 3600 total seconds, three public development
   runs and one private candidate pass per gap/input generation. Reserve effort for
   report finalization and fresh reuse. Report every budget-deferred gap explicitly.
   Changes require a new source-bound generation, retaining earlier evidence.
7. Prepare a bounded assessment JSON before scanning, e.g.
   .rig/setup-assessment.json. Read [report finalization](references/coverage.md#finalize-after-execution)
   for the small input shape and supported tool flow. This is an inventory seed,
   not a finalized scan profile. Preserve original/default measures, evidence,
   exclusions, rule provenance and unknowns. Existing historical profile/report
   files may remain as historical assessment inputs; do not present them as current.
8. Review/run through normal Rig tools, inspect actual receipts, then finalize.
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
9. Verify in a fresh native session without earlier conversation. It must discover
   saved checks/report with normal Rig tools, preserve settings and any command
   approvals, perform a new
   scan, and finalize the updated customer report using its new receipt. Rebind any
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
