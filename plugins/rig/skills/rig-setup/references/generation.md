# Automatic behavior-grounded generation

Setup authorization covers discovery, development test execution, independent
qualification and advisory activation of checks meeting policy. The customer does
not prepare verifier programs or cases, review rules, or approve each passing
check. Use existing Rig preview/digest/apply and policy-review/activate controls
under that authorization. Failed or unknown checks remain inactive. Required
rollout, new dependencies, providers and hooks retain their separate scope.

## Bounded worklist, existing protection first

Read `rig setup --worklist` before discovery. A current saved plan keeps completed,
failed and unsupported outcomes and its original attempt/deadline budget; do not
reset it or retry unchanged inputs. For new/changed inputs, invoke evaluate.py
with --inventory and the existing --project/--baseline/--output controls in a fresh
source-only session. Supply only saved obligation metadata with --saved-obligations,
never prior rules, cases or grading forms. Discovery writes an initial unknown
inventory immediately and adds obligations incrementally, reserving time to finish.
A timed-out valid partial plan keeps discovery.complete=false and uninspected
obligations unknown; a failed discovery must still save an all-unknown report
without inventing targets or asking the customer to prepare tests. Its plan records all A01..A10 categories,
observed applicability/reasons and all concrete app-layer obligations (maximum 128).
Use applicable, unknown, not_applicable or outside_app_layer honestly. Missing
runtimes are unsupported/unknown, not evidence that a feature does not apply.

Save a plan request with operation=plan, inventory, gaps, and budget
{max_attempts:8,max_seconds:3600}, using --worklist REQUEST preview then
--apply --digest. The bound may be lower for a declared trial; hard maxima are 32
attempts and 14400 seconds. Budget covers total workflow effort, not eight times
that time. Reserve finalization/reuse time. Each gap has id, statement, gap,
categories, paths, applicability, reason, limitations. Categories are discovery
labels, never a coverage numerator. Paths must cite actual caller source files.
One obligation may span categories; a category can have many obligations.

For each next_gap, save inline {operation:"claim",id:ID} before work. Generate an
independent per-obligation cohort using evaluate.py --focus with only the saved
statement/gap/paths/limitations. No engineer selects helpers or supplies tests.
Use qualify.py purpose=existing with the unchanged complete baseline first. It
needs no candidate: bind rig, engine, private, cohort, baseline_id, frozen_files
and application_inputs as below. Register/review/approve/run this ordinary command
under setup authorization. Only a current approved app_existing_qualification
receipt, exact protective bytes, complete vulnerable/safe contrasts and zero
observed errors/alarms can finish outcome=existing (check=baseline ID,
verifier=command ID). This verifies only tested targets/operations, not the category.
Application-model baselines require their compatible verifier; never omit models.

If existing rules miss the obligation, use the behavior/generation loop below.
Use unique immutable helper/draft/assessment paths and check IDs per generation;
append definitions and preserve older rules/scopes/evidence. Bound public
purpose=development manifests with max_development_runs=3. Freeze at most one
candidate and run its independent qualification once. Save passing evidence then
use normal policy-review/activate automatically under setup authorization.
Finish {operation:"finish",id:ID,outcome:"generated",check:ID,reason:...}; Rig derives
active/rejected status from real qualification/policy, not the requested label.
Failed candidates stay inactive and their actual qualification receipt is retained.
For unavailable evidence/runtime or no candidate, finish unsupported, unknown or
error with an accurate reason. Continue next_gap after every failure; do not retry
for perfect coverage. A prior_check may retain the same saved obligation without
rerolling its failed collection. Changed source/tool/protection context stales the
plan and requires reassessment rather than a cached pass.

Save a current canonical report after the loop. It includes the full worklist and
separate existing_verified, generated_active, rejected, retained_inactive,
unsupported, unknown, not_applicable, outside_app_layer and deferred_budget states.
Only independently checked finite scopes are verified; a completed inventory is
not OWASP coverage. Fresh sessions resume this same ledger, run saved checks with
new receipts and confirm saved_report_current=true, preserving .rig bytes and
attempt counts. Never repeat discovery/evaluation on unchanged finished inputs.

1. Inspect languages, frameworks, dependencies, actual helpers and callers, existing
   rules/exclusions and a real baseline scan. Inventory OWASP concerns from observed
   features; unresolved applicability and policy stay unknown. Establish helper
   semantics through contrasting executable tests before generating rules. Create
   ordinary development tests under .rig using available project runtimes; register,
   review, approve and run them through normal Rig commands under setup authority.
   Record a behavior table for actual transformations: input constraints, value
   lineage, execution context, ordinary result and security effect. Distinguish
   known unsafe operations, tested safe transformations and unknown behavior.
   Unknown transformations are not evidence of vulnerability. Probe the analyzer
   against that table, including safe custom helpers and alternative encodings;
   matching an API name or knowing one escaping primitive is insufficient. Let
   observed semantics determine the sources/sinks/sanitizers and conservative scope,
   rather than adding patterns solely to fit the visible fixture forms.
2. Keep evaluation separate from authoring. The current Codex/macOS beta helper
   scripts/evaluate.py launches a fresh ephemeral native evaluator with a source-only
   repository copy, existing baseline pack, no author rules/conversation/history and
   no API-key route. Invoke it with --project ROOT --baseline LOCAL_RULES --output
   NEW_EXTERNAL_DIRECTORY. Read its source before execution if needed. It inspects
   the application and generates its own public/private full-source variants plus
   a runtime behavior oracle. The controller separately reruns that oracle without
   network, joins every label and ordinary-behavior observation to case bytes, and
   freezes the generation. No engineer-written repository code or labels are inputs.
   Run this before authoring. Only public/ observations/cases reach the author;
   private/ and oracle files must stay outside author tool read access. The emitted
   location.json identifies the frozen external evaluation directory. Load hash/path
   fields programmatically for manifests; never print the full freeze inventory,
   private cases, oracle or runtime-results to the rule-author model.
   During the separate author session, use id-scoped reviews/runs only. Broad
   project/status inspection can expose private comparison receipts before freeze;
   it is not an author-safe inventory path after evaluation commands have run.
   Retire an exposed collection without rule tuning or a qualification score. The
   existing unopened-generation guard permits transport-only replay only while
   source/pack/evidence bytes match and the collection has not been spent/retired.
3. Use the normal generic scripts/qualify.py command runner for both splits. It
   disables scanner background version/metrics calls in isolated execution and
   retains a bounded startup budget. The public catalog opengrep-native variant
   supports the same local-rule path without Python CLI startup; preserve the exact
   selected engine/pack identities across both arms. Use
   separate manifests/purpose=development or qualification. Manifests contain rig,
   engine, private (output directory), cohort, generated_id, baseline_id (the
   existing complete local-rule scanner; defaults to opengrep-default), frozen_files (absolute
   path to SHA256), application_inputs (repository-relative source to SHA256 from
   the evaluator freeze), and development_report. Bind the source_root files from
   that freeze in frozen_files as well; changed context needs a new generation. Development also selects rules_path
   .rig/draft-rules.json. The independent manifest binds evaluator oracle/runtime
   observations, cohort/case/tool bytes and uses default installed generated rules.
   Register the ordinary read-only commands with normal execution review/approval
   under setup authorization; keep the independent command approved in policy.
   Do not require the customer to construct these manifests or commands.
4. Build from positive semantic evidence, not absence of a recognized guard. Record
   a transfer table for actual helpers and operations: preserved unsafe input,
   tested neutralization/validation, ordinary behavior and unknowns. Probe these
   transfers independently through the installed analyzer before rule authoring.
   Opaque calls must not be assumed unsafe simply because a sanitizer name/form is
   unrecognized. For taint rules, the supported conservative option is
   options: {taint_assume_safe_functions: true}; explicitly propagate through
   runtime-verified unsafe-preserving operations. This does not prove opaque
   calls safe: keep their unsupported scope explicit. Other engine options remain
   rejected. See the [upstream taint semantics](https://github.com/semgrep/semgrep-docs/blob/main/docs/writing-rules/data-flow/taint-mode/advanced.mdx).
   Prefer the existing scripts/qualify.py native() fixture path for analyzer
   capability controls, registered as an ordinary Rig command under setup authority.
   It initializes an isolated Git root and checks current complete execution,
   analyzed-file counts and attribution while retaining raw evidence. Every
   additional direct probe must retain raw JSON and assert the exact analyzed
   target set before interpreting absent findings. Use a known positive primitive
   control first; skipped inputs or a failed probe are not semantic analyzer limits.
   Challenge the draft with new behavior-checked equivalents derived from the
   semantic contract, not the visible fixture spellings. A growing list of guard
   spellings is not a semantic model. If the analyzer cannot represent the
   obligation conservatively, leave it unsupported rather than flagging unknowns.
   Test equivalent control flow for proven validation, including branch-local
   conditions and early exits, with actual runtime outcomes and native findings.
   Do not stop at a perfect public-suite score. The independent all-vulnerable,
   zero-observed-safe-alarm and zero-error requirements stay unchanged.
   Develop on public cases and separate native capability probes, including aliases,
   propagation, overwrites, unused values and useful legitimate alternatives. The
   runner evaluates actual Rig checks and normalized findings, preserving baseline
   protection. It supports local-rule baselines; application-model baselines must
   retain their existing compatible verification path, never silently strip them.
5. Use baseline_check from the actual public-development proof as the baseline,
   and compare its baseline_rules_sha256 with the behavior preview before saving.
   Historical scoped checks may contain older rule bytes; never substitute them
   because a display preview was shortened. Structured raw JSON/SARIF preserve full
   scanner evidence; display_truncated alone does not invalidate that evidence.
   Anchor current helper tests and baseline using rig_setup arguments
   ["--behavior","TEST_CHECK","--baseline","SCANNER_CHECK"], then save via rig_manage
   setup with --apply --digest. Generate a request JSON with id, behavior_check,
   qualification_check, statement, gap, limitations, paths and rules:{"rules":[...]}.
   Preview --generate REQUEST and save its digest. Save ONE frozen candidate per
   independent collection, after all public cases pass. Run the independent
   qualification command once through Rig. Never repair or tune against spent
   cases; preserve them and automatically create a new generation when needed.
6. Save --qualification ID only if every vulnerable case is detected at the right
   operation, every safe case has zero new alarms, no errors/unknowns occur, and
   existing rules demonstrably missed the obligation. Automatically run normal
   policy-review and activate for this exact qualified advisory check under setup
   authorization. This is an automatic conditional policy decision, not a request
   for human review. Failed checks remain inactive with explicit remaining gaps.
7. Save the assessment/report using current normal scan receipts. This enables
   automatic receipt refresh for unchanged inventory; a fresh reuse scan must leave
   --report saved_report_current=true. Old finding IDs never become new evidence;
   absent current mappings remain unknown. Code changes still require reassessment. Fresh sessions
   discover --generated and reuse current saved checks with NEW executions and no
   configuration changes. Test reuse with unchanged code separately from staleness.
   Source/rule/tool/grader changes invalidate evidence. Automatically re-inspect,
   generate new independent cases, test and qualify a new version using the same
   loop; preserve old evidence and unrelated policy. Never repair approval storage
   or reuse a cached qualification for changed context. If new evidence fails,
   keep the changed check inactive and record why; do not require manual repair.

The native evaluator currently requires Codex ChatGPT authentication, macOS
sandbox-exec and Python 3.11+, Bash and available project runtimes. Model-generated runtime oracles
are independent of rule authoring but can still share model errors; byte bindings
are integrity, not semantic proof. One finite successful example does not establish
arbitrary-repository or OWASP-wide effectiveness. Missing runtimes, failed oracle
construction, unsupported analyzer semantics and scan errors remain explicit beta
gaps; do not ask engineers to supply repository-specific tests to paper over them.
