# Automatic behavior-grounded generation

Setup authorization covers discovery, development test execution, independent
qualification and advisory activation of checks meeting policy. The customer does
not prepare verifier programs or cases, review rules, or approve each passing
check. Use existing Rig preview/digest/apply and policy-review/activate controls
under that authorization. Failed or unknown checks remain inactive. Required
rollout, new dependencies, providers and hooks retain their separate scope.

## Defensive fixture context for future authorized requests

State the legitimate purpose and limits plainly: owner-authorized repository
security-rule validation using local disposable fixtures, harmless markers,
in-memory/disposable data and mocks at external-service boundaries. Detection
and allowed-behavior controls must exercise the real source-grounded behavior.
No deployed targets, credentials, exfiltration, persistence or destructive actions
are authorized. Do not disguise the requested operation, weaken expected results
or reveal candidate/answer details to the independent constructor.

This scope clarification changes neither service safety rules nor evaluation
authority, budgets or independence. It does not promise acceptance or fewer refusals.
If a provider refuses a required step, preserve the incomplete inactive outcome and
report it clearly. Do not retry, rephrase, switch models or tune that blocked request
to get around the refusal. Earlier blocked requests, including the existing Ledger
evaluation, remain unresolved; this wording is for future authorized work only.

## Worker execution and permissions

Use the current Rig runtime (`rig` on the caller's trusted PATH, or an explicitly
selected absolute `RIG_EXECUTABLE`). Preflight RPC, the evaluator session and the
controller's oracle rerun all use Rig's shared bounded process capture through
its private `__eval_worker` transport. A stdin lease ties each worker to the
calling controller: EOF, explicit cancellation, SIGINT/SIGTERM, timeout, worker
failure and parent completion terminate only that worker's owned Unix group.
No `ps` or global process inventory is used. Controller SIGKILL closes the lease;
the surviving supervisor cleans up. Native cleanup errors are separate from the
original outcome and always prevent qualification, including after exit zero.

Preflight has a 30-second response deadline and 120-second overall cap; evaluation
uses the supplied session budget (at most 14,400 seconds); the oracle has 120
seconds. Each captured stream is limited to 16MiB. RPC input and response lines
remain limited to 1MiB; native exec event lines share the existing 16MiB total
capture cap because a host command may return 1MiB before JSON escaping. Every
event, including an unterminated final line, is parsed for auth/overage guards;
invalid or truncated event JSON cannot qualify. Native polling is at most 20ms, followed by a two-second
child reap bound; the Python close transport waits three seconds and then allows
three seconds after SIGTERM. These are ordinary scheduler/OS-operation bounds,
not a guarantee during a hung kernel. No unbounded `wait()` is used.

Preserve the caller's configured read-only and never/on-request approval policies;
missing settings use read-only/never. Sandbox-disabling configuration is narrowed
to workspace-write; automatic-review overrides are not enabled. The caller's outer
execution restrictions still apply. If a required execution permission is denied,
explain the affected operation in the calling conversation and use the host's
supported approval path for a separately authorized retry. A decline stops that
work. Never automatically relaunch, disable sandboxing, change authentication or
use API/paid-credit fallback. Permission and worker failures return bounded fixed
messages; keep raw worker logs, requests, private cases and credentials outside
author-visible output. New worker directories are private and single-use.
A valid partial inventory after timeout remains `complete:false` and exits 2;
permission, cancellation and cleanup failures cannot become a successful plan.

The evaluator still supports Codex/macOS with Python 3.11+ and sandbox-exec only.
Shared capture is exercised on Unix; Windows lifecycle work remains DEV-396.
Owned groups cover descendants inheriting that group. Deliberate daemonization
or a new session/group, supervisor SIGKILL, hostile same-user interference and
OS denial of signals are outside this containment boundary; this is not a hostile
process sandbox. The lifecycle tests use fixture hosts without model calls;
they do not qualify native model behavior or same-user filesystem isolation.

## Local fresh-context evaluation through MCP

Submit a saved frozen generated candidate using `rig_evaluate` arguments
{"id":"CHECK"}. CLI equivalent: `rig setup --evaluate CHECK`. This is a local
operation in the current agent loop. It requires no hosted service, server
provisioning, customer infrastructure, new credential flow or per-rule review.
Setup authorization covers the existing worker execution and conditional advisory
adoption. Preserve caller permissions; permission denial is incomplete, never an
invitation to weaken sandboxing or switch providers.

The CLI freezes candidate, source, repository, baseline and tool identity before
launch. It uses the existing __eval_worker supervision and stdin lifetime lease
for the local controller, then the existing native source-only evaluator for a
fresh ephemeral context. Candidate/history are not supplied to that context.
Codex retains the caller sandbox/approval policy; no nested sandbox wrapper or
sandbox bypass is used. Only source, unchanged baseline and caller paths are
supplied. The controller independently reruns the network-denied runtime oracle
and freezes all case/label bytes before
materializing candidate bytes for grading. qualify.py runs actual Rig on unchanged
baseline, candidate-only and combined packs with the same supported engine settings.
Unsafe credit requires the candidate-only and combined scans to detect the intended
operation. All three must complete; combined safe alarms remain disqualifying.
This prevents a baseline rule with a similar ID from earning the candidate credit.
Policy requires complete candidate-owned
attributed vulnerable catches at intended operations and zero observed safe alarms/errors.
A baseline miss is not required: an applicable threat warrants a custom check even
when existing rules detect the test case. Baseline-only warnings cannot qualify an
ineffective candidate. Model-generated semantic oracles can still be mistaken.

The operation retains passed, rejected, failed, cancelled, incomplete, contaminated or
budget_exhausted, with input identities and a fixed safe summary. New results add a
closed `diagnostic`: `schema_version`, `stage`, `reason`, `cleanup_error`, `owner`,
`message`, `missing_evidence`, `next_action`, and `retry_same_request:false`.
An identified authored-pattern error also supplies a bounded `candidate_location`
with rule index, field and JSON pointer, against the outcome's `candidate_rule_path`.
Known construction output limits, permission denial, timeout, authored-rule errors,
scanner/parser failures, missing proof and finite grading failures stay distinct.
Private exceptions and worker text never populate these fields. No cases, expected
labels, oracle, detailed findings, private paths or comparison receipts enter
ordinary check history, MCP responses, error messages, setup reports or worker
status output. Broad `rig_inspect`/project queries use the same safe saved outcome.
Do not register a private evaluator as an ordinary command that prints its proof.
Historical author-visible command proofs no longer qualify generated rules;
--qualification is only an idempotent view/save of a current CLI evaluation seal.

Read `stage`, `reason`, `owner` and `next_action` before changing a rule. Tester
failures leave it ungraded; fix the named runtime/setup/evidence stage. Permission
denial needs the supported caller approval route, never an automatic relaunch.
A complete rejected grade may report unsafe detection/attribution missing, a safe
alarm, or both. Improve public development examples for the declared operation;
do not tune against private syntax or reopen a spent collection. Public examples
may show full code, exact warning lines, expected/actual results and parser errors.
Private feedback stays aggregate and categorical.

The controller checks candidate syntax against public source before construction,
outside the fresh context's source inputs; that temporary rule is removed before
launch. Construction receives source-grounded statement/gap/scope/limitations,
never candidate/history, and must establish those semantics itself. Passing
metadata around is not proof that an oracle tests the right behavior.

Do public syntax and development checks **before** `rig_evaluate`. Use the pinned
engine with the authored rule and a deliberately public caller, for example
`ENGINE scan --config AUTHOR_RULE --strict --json --disable-version-check PUBLIC_CASE`,
or inspect an ordinary public-development Rig scan's parser evidence. Its rule ID,
bad pattern and authored file/JSON pointer identify what to repair. These public
scans do not create an independent request or consume its allowance. Preserve
expected/actual public cases, then register/freeze the repaired candidate.

The extra controller syntax check is defense in depth inside an **already reserved**
private job. An invalid rule first discovered there still spends that slot. Fixing
its syntax does not authorize revised resubmission to the same gap/collection.
Keep that failure and allowance; a later untouched collection needs its separately
authorized budget. No hidden cases are needed to retrieve a public parser error.

Legacy version-1 outcomes remain readable without invented diagnostics. The new
internal response is version 2 with closed codes bound to the same request.
Exact retrieval never reruns a worker or repeats adoption. A later changed binding
adds `freshness_diagnostic` separately from the original evaluation cause; stale
results remain unusable for qualification. Read-only progress carries the same
safe diagnostic without changing support counts or authority.

A current pass automatically adopts advisory policy via the existing policy APIs.
A failed, incomplete, stale, contaminated or spent attempt stays inactive. Required
enforcement remains separate. Source/rule/tool/repository changes invalidate the
seal. Spent or exposed collections cannot qualify revised rules. An identical
submission can read its existing decision without grading again; changing remaining
time or caller-path ordering cannot open a new collection.

Retain the existing worklist budget (default eight attempts/3600 seconds), three
public development runs and one private candidate grading pass per gap/input
context. Claim the current gap before work. The local controller preserves a
finite ledger and a single-use gap/caller-scope slot, honoring the current worklist
limits up to the existing hard maxima (32 attempts/14400 seconds). Interrupted work
remains incomplete. Finish rejected/unsupported entries and continue the queue;
never retry unchanged failed obligations for a better score.
To retire known exposure, use `rig_evaluate` with {"id":"CHECK","exposed":true},
or `rig setup --evaluate CHECK --exposed`, before revising the candidate.

## Request identity and reconnects

The CLI persists an author-safe request record before launching a worker. Its
`request_id` derives from the existing frozen evaluator identity and setup binding:
repository/worktree, source fingerprint, candidate, baseline, gap/scope, package and
tools. `request_sha256` retains the submitted transport-byte digest. Remaining time
is not a new candidate identity. Synchronous responses retain the normal call
association; the record is the recovery handle, not a credential or chat router.

Retrieve exactly one job using `rig_evaluate` with
{"id":"CHECK","request_id":"REQUEST"}, or
`rig setup --evaluation-result REQUEST --check-id CHECK` (CLI check ID is optional).
`rig_setup` can read the same `--evaluation-result` path. Unknown/mismatched IDs fail;
historical results report `current:false` after input changes and never select the
latest candidate. Retrieval executes no worker and activates no policy. Submit with
optional `origin_host`/`origin_session` (CLI `--origin-host`/`--origin-session`) only
when the actual host supplies bounded identifiers. Unknown references stay null;
Rig never uses the latest active conversation as an origin.

Lifecycle is `running`, `completed`, `failed`, `cancelled`, `incomplete`, or
`interrupted`. Rejection is a completed evaluation, not worker failure. Permission,
runtime or evidence gaps stay incomplete. A request lease identifies live work;
a missing controller lease converts unfinished state to interrupted/incomplete.
The existing worker stdin lease handles owned cleanup; recovery does not keep a
worker alive, relaunch it, reset budgets or repeat adoption. Interrupted adoption
cannot authorize execution. Identical submissions return their original record;
older qualification outcomes archive before fresh submission validation, without
re-evaluation, as explicitly stale history with unknown origin.
Terminal decisions are saved before the serialized short adoption transaction.
A policy-adoption error preserves the pass with activated=false, and retrieval
does not retry adoption. Exposure retirement records its marker even while the
worker lease is held; completion cannot activate a retired collection.
Different requests can overlap; short shared ledger transactions reserve attempts
before work and merge completion without overwriting another job's result.

Normal `setup --generated` and saved `setup --report` include `evaluation_requests`.
Fresh sessions reuse repository-scoped configuration, outcomes and finite budgets.
Only the fixed safe result enters these records; a known request ID provides no
private evidence endpoint. Exposing a collection retires the existing request and
preserves its origin; it does not create another grading attempt.

## Same-user limitation

Fresh context and MCP output filtering do not make local files inaccessible to the
same OS user. Unrestricted file/shell tools may read evaluator artifacts despite
ordinary private directory permissions. Neither role is isolated from all same-user
reads. The constructor is given only the fresh source context; the separate runtime
oracle retains its network/write/candidate/history sandbox. Do not claim
hostile-author isolation or that prompts, unadvertised directories or managed
workers enforce secrecy. Never deliberately
inspect hidden data during authoring. If exposure occurs, retire that collection
and leave its candidate inactive. Stronger external OS/service isolation is outside
DEV-413's owner-revised local scope and is not a prerequisite for this workflow.

## Normal bounded setup loop

1. Resume `rig setup --worklist`; keep existing outcomes, applicability/unknowns,
   attempts and deadline. For new source, preview `rig_setup ["--inventory"]` and
   execute the exact proposal with `rig_manage` setup arguments
   `["--inventory","--apply","--digest",TOKEN]`. The CLI runs the existing
   source-only native discovery worker within 600 seconds. It returns only the
   public passive plan; model captures and worker files are not public receipts.
   Save it through ordinary `--worklist @inventory` preview/apply and claim
   next_gap before effort. Do not supply a substitute engineer-written plan or
   call private Python protocols yourself. Terminal replay does not start another
   discovery worker, and changed input requires a fresh proposal. A timed-out
   valid partial plan remains incomplete with unknowns; interrupted or unavailable
   workers provide no plan or coverage.
   OWASP inventory/tags and zero findings never establish coverage.
2. Inspect actual helpers/callers, preserve selected baseline rules/profiles and
   execute ordinary development tests and baseline scans through normal Rig APIs.
   Missing dependencies are recoverable setup work, not by themselves an unsupported
   outcome. Inspect declared versions and use normal host permissions to prepare
   needed test tooling in `.rig/generated` without editing application manifests or
   lockfiles. Continue after permitted installation. Report unsupported only when
   tooling cannot be prepared, execution is denied, or semantics remain unknown.
   When no existing project command exercises the helper, author an ordinary test
   in `.rig/development/` and a small JSON definition with `id`, `statement`,
   `script` (relative path), `runtime` (absolute external executable), optional
   `arguments` and `approval_inputs` (script/supporting source patterns). Preview
   `rig_setup ["--test",DEFINITION]`, save its exact digest with `rig_manage` setup
   plus `--apply --digest TOKEN`, then use `rig_review`, `rig_approve` and `rig_check`
   under the setup test authorization. Saving grants no execution approval or
   automatic permission. These are public development observations, not independent
   qualification. Do not invent `checks add`, edit approval storage or hand-edit
   project policy to create the helper check. Use `rig_setup ["--help","checks"]`
   for the actual public command contract.
   Establish observable unsafe/neutralized/ordinary behavior; unknowns remain gaps.
   Do not substitute a growing list of guard spellings for a semantic model.
3. Anchor current helper tests/baseline with rig_setup ["--behavior","TEST_CHECK",
   "--baseline","SCANNER_CHECK"], then save through rig_manage setup --apply
   --digest. Author bounded local rules and public development controls. For taint
   the supported precision option remains taint_assume_safe_functions=true with
   verified propagators. Keep opaque or unsupported flows explicit. Public
   development fixtures are visible and never count as independent qualification.
   A captured current baseline with analysis diagnostics can anchor development,
   retaining `baseline_verification=incomplete` and its original errors. Preserve
   the full baseline check and report; never narrow it to hide diagnostics. The
   anchor contains a bounded receipt reference and summary; use normal Rig receipt
   inspection for its retained full findings/errors. Unreadable legacy packages
   remain inactive history and cannot be evaluated or activated. This
   reference establishes no protection. The fresh evaluator must still execute
   complete baseline/candidate contrasts with zero errors before qualification.
4. Save --generate REQUEST using preview/apply. Fields id, behavior_check,
   statement, gap and limitations are strings (join multiple limitations in that
   string). With a worklist, gap is the exact claimed obligation ID; an exact
   unique legacy description is also accepted. Rig canonicalizes both before job
   identity/reservation. Unknown or ambiguous references fail without execution;
   Rig never chooses the latest/running obligation on the caller's behalf. Paths
   is an array of strings, and rules is {"rules":[...]}. Unknown
   fields are rejected.
   No private qualification_check command or engineer-prepared oracle is needed.
   After at most three public development runs, freeze ONE candidate and submit
   it with rig_evaluate. Do not launch private scripts yourself or inspect private
   worker results. The evaluator constructs cases automatically in its fresh context.
5. Use the safe decision. A pass is adopted automatically under setup authorization;
   rejection/incomplete/exposure needs no customer rule review. Finish the queue row
   from actual gate state or an honest unsupported/unknown reason; preserve budget
   deferrals. Do not claim independent existing coverage from visible command output.
6. Save the canonical assessment/report from current ordinary scan receipts and
   safe generated-check outcomes. Verify unchanged-input reuse in a fresh session.
   New executions and actual freshness matter; do not repair result IDs or approvals.
   Inactive generated checks, unsupported cases and incomplete whole-project scans
   remain explicit gaps. A current executed baseline failure plus inactive
   candidates can be saved as a partial report; it adds no verified coverage.
   Refresh stale active receipts through Rig; do not add a passing scoped scan
   merely to make a report save. Mention the same-user file-access limitation when reporting
   this local evaluation boundary. Finite case success is not repository-wide or
   OWASP-wide coverage.

The existing evaluator beta still requires macOS sandbox-exec, Python 3.11+, Bash,
Codex ChatGPT authentication and available project runtimes. No API-key fallback,
provider installation or automatic permission escalation is added. Unsupported
platforms/runtimes remain incomplete; no customer infrastructure solves that here.
