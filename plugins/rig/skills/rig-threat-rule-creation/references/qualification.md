# Register a candidate and use Rig's private evaluator

Use live MCP schemas and the coordinator's project/state binding. This is the
supported setup-generation route, not a second verifier protocol. The sibling
`rig-setup/references/generation.md` contains the full worker and recovery contract.

Evaluation currently adopts a passing advisory check automatically. Run this in an
authorized isolated profile unless the owner's existing setup authorization covers
advisory activation in the actual project. Creating files and evidence links alone
does not grant that authority. Required enforcement remains separate.

Before creating another candidate, read [shared requirements](../../rig-onboarding-coordinator/references/shared-protections.md)
and [this area's caller tests](caller-tests.md). `adopt_existing` reuses a detector
only after own path tests; `create_new` needs different behavior. A proposed
replacement preserves original bytes/results under a new ID and stays inactive;
do not run the auto-adopting evaluator merely to record a replacement proposal.
Detector qualification, caller applicability and caller invocation/denial evidence
remain separate. An old helper receipt does not prove new caller contrasts ran.

## Obtain an actual generated check ID

1. Discover existing configuration using `rig_setup` with
   `{"arguments":["--project"]}`. Preserve configured scanners and policy. If the
   scanner/rules are unavailable, report that prerequisite; do not install tools
   automatically. Where missing preparation is already authorized, `rig_manage`
   with `{"command":"setup","arguments":[]}` prepares it and may download files.
2. Reuse a current frozen local baseline check. If it needs configuration, preview
   with `rig_setup` arguments `["--candidate","opengrep-default"]` (or select the
   already reviewed local `--rules` file). Read the proposed configuration, then
   apply the same selection through `rig_manage`, command `setup`, adding
   `"--apply","--digest",TOKEN` under the existing setup authorization. Run it
   using `rig_check` with its actual ID. The runtime requires a completed current
   scan with analyzed files and no diagnostics as provenance. **Do not assess its
   effectiveness or require a missed finding.** A clean scan does not remove the
   threat or the need for regression protection.
3. Reuse an ordinary read-only project test check that exercises relevant helper
   behavior. Separately run this area's exact caller contrasts through
   [the supported caller-test CONFIG route](caller-tests.md); do not substitute a
   maintained helper receipt for those new tests. If none exists, write development contrasts and inspect the project's
   actual test entry point. `rig_setup ["--project"]` discovers repository command
   candidates; preview the actual discovered ID with `--candidate ID --read-only`
   and apply its exact reviewed digest through `rig_manage`. Do not invent a
   candidate ID. Read its executable, arguments and full scripts before using it.
   Use `rig_review {"id":ID}`. If `execution_approved` is true, run `rig_check`
   directly. Otherwise use `rig_approve` with the reviewed execution digest only
   under explicit owner authorization for that command. Ordinary shell output or
   author-written JSON claiming success cannot replace a Rig test receipt.
   When new development/caller tests have no discovered entry point, append an
   ordinary CONFIG check as documented in caller-tests.md, then review/approve/run
   its actual ID. No arbitrary-argv registration API or invented discovery ID exists.
   Missing runtime/permission remains an explicit gap; never forge a receipt.
4. Anchor the two current receipts using `rig_setup` with
   `{"arguments":["--behavior",TEST_ID,"--baseline",BASELINE_ID]}`. Preview returns
   `proposal_digest`. Save the same arguments through `rig_manage`, command `setup`,
   adding `"--apply","--digest",TOKEN`. After source changes rerun/re-anchor the
   helper evidence; stale anchors cannot authorize a new rule.
5. Write the request under `.rig/`, for example `.rig/threat-rule-request.json`,
   so saving the request does not change the source fingerprint just anchored.
   An application-source edit or a new request outside `.rig/` needs a fresh helper
   run and anchor before generation. The supported fields are:

   ```json
   {
     "id": "area-threat-check",
     "behavior_check": "ACTUAL_SAVED_TEST_ID",
     "statement": "The selected protection requirement",
     "gap": "An applicable threat needs project-specific regression protection",
     "limitations": "The inspected detector scope and unsupported cases",
     "paths": ["src/relevant.py"],
     "rules": {"rules": []}
   }
   ```

   Replace `rules.rules` with the actual nonempty parsed rule objects; one rule
   per authored YAML file remains the development layout. The `gap` field is a
   required legacy description, **not a demand to prove a default miss**. Omit
   `qualification_check`; no engineer-written qualification command is needed.
   The ID must be new; preserve earlier candidates/results.
6. Preview with `rig_setup` arguments `["--generate",REQUEST_PATH]`. Inspect the
   generated files, rule/check identity, scope and inactive state. Apply that exact
   preview via `rig_manage`, command `setup`, with the same arguments plus
   `"--apply","--digest",TOKEN`. This saves an inactive generated candidate.
   Use its returned/configured ID for evaluation, never a guessed filename/ID.

## Freeze, evaluate and retrieve

After development testing of an authorized new detector, submit `rig_evaluate {"id":CHECK_ID}`. Preserve the safe
`request_id` and decision. Retrieve the exact request with
`rig_evaluate {"id":CHECK_ID,"request_id":REQUEST_ID}`; retrieval runs no worker.
Private fresh construction freezes cases before grading and keeps them out of
ordinary Rig outputs. Do not register private scripts as public commands or
provide a self-written pass proof. If private cases are exposed, retire with
`{"id":CHECK_ID,"exposed":true}` before any revision. Do not reroll unchanged
rejections; preserve finite budgets, errors and unsupported requirements.

A baseline miss is not required for an applicable threat. Qualification still
requires candidate-owned unsafe findings, safe contrasts, exact bytes, current
provenance and actual Rig execution.
A baseline-only finding must never qualify a useless candidate.

The tested OpenGrep supports `--taint-intrafile`, but the current generated-check
argument contract does not carry that flag. Record this required option explicitly
and leave that integration incomplete. Do not disguise it as a YAML option or
inject it into an otherwise unsupported check. The permitted conservative YAML
option is `taint_assume_safe_functions: true` in taint mode; verified propagators
are still needed and unknown outputs are unsupported, not proven safe.

The evaluator requires its actual supported host/runtime and permissions. Safe
outcomes are passed/rejected/failed/cancelled/incomplete/contaminated/budget_exhausted;
only a current qualifying pass can adopt. Same-user filesystem access is not
hostile-author isolation. Missing capability leaves the candidate inactive.

## Use feedback to repair a public example

Read `diagnostic.stage`, `reason`, `owner`, `missing_evidence` and `next_action`.
For invalid syntax, use `candidate_rule_path` and the bounded candidate JSON
pointer, then run the pinned engine on that authored rule and a public caller.
Its public parser error identifies the bad pattern. Do this before `rig_evaluate`:
ordinary public scans spend no independent allowance. The controller's later
syntax check occurs after reservation and still spends its slot on error; repair
does not permit revised resubmission to that same private collection.
Output limits, denied permission, timeout, invalid case construction, scanner/parser
failure and missing proof leave the rule ungraded. Preserve that result; repair
the named stage rather than treating it as a missed detection. Use supported caller
approval only when actually needed. Retrieval never restarts a spent request.

For a concrete public SQL example, an unsafe string-built query should warn;
`db.execute("SELECT secret FROM notes WHERE name = ?", (name,))` should not warn
merely because `name` is caller data. A broad `execute(...)` rule alarms on both.
Return the author-owned reproducer, expected silence, actual warning/line and
pinned engine command. Track data into SQL text and verify allowed bound values
and fixed queries remain quiet. Check actual behavior with a disposable in-memory
database, then test the exact rule through normal Rig.

Freeze the repaired candidate before its first independent grade. Fresh construction
must not see the candidate, public case variations, conversation or previous grades.
A final private result may say unsafe detection/attribution missing, safe alarm or
both, without private case code, IDs, paths or syntax. Do not refine rules against
that collection or reset its allowance. Report finite pass, policy adoption and
selected normal execution separately; all retain current-source requirements.
