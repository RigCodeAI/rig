---
name: rig-threat-rule-creation
description: Create and independently test threat-specific source rules for one saved Rig analysis area, then save rule and evidence references through Rig MCP. Use after an area's threats and code flows exist, including currently safe code needing regression protection.
license: CC-BY-SA-4.0
---

Create useful candidate rules because a threat applies, even when current code is safe.
A current vulnerability, default-pack miss or baseline scan is not an entry condition.
The default pack remains background protection. Do not fix application code or silently
activate checks in the customer's project.

For future owner-authorized work, state the purpose accurately: defensive validation
of repository security rules in local disposable fixtures, checking unsafe detection
and allowed-behavior controls. Use harmless markers, in-memory or disposable local
data, and mocks only at external-service boundaries while preserving real helper
semantics. No deployed targets, credentials, exfiltration, persistence or destructive
actions are authorized. Describe the actual source-grounded behavior and limits;
do not conceal the requested operation or supply candidate/answer details to the
independent builder.

A defensive label does not override safety rules or mean that a service permits
the request. If a provider refuses, preserve and clearly report the incomplete
outcome. Do not retry, rephrase, switch models or tune the blocked request to get
around the refusal. Keep it separate from a failed rule test; leave the candidate
inactive and continue only unaffected work within existing authorization and budget.

Read the assigned area using the host-exposed `rig_analysis_read_area` tool and
`{"id":"AREA"}`. Use the coordinator's bound project/worktree and state directory.
Discover the live schemas; tool prefixes vary. If the four analysis tools are absent,
report the missing capability. Do not substitute SQL, database files or CLI saves.

Read [database updates](references/database.md) before saving. Read the literal pinned
Trail of Bits [skill](references/upstream/skill.txt),
[workflow](references/upstream/workflow.txt) and
[quick reference](references/upstream/quick-reference.txt) before authoring.
These are source reuse, not a claim that Semgrep-only features work in OpenGrep.
Read [host adaptations](references/adaptations.md) and its seven documentation snapshots.

Keep author-generated rule packages, development fixtures, understanding notes and
logs under `.rig/` by default, with one rule-ID subdirectory per rule. The private
constructor excludes `.rig/`; leaving candidate bodies or answer notes among ordinary
application files can expose them as source inputs. Keep these artifacts out of the
fresh evaluator context and inspect submitted scope before qualification.

Follow the upstream sequence:

1. **Explain the intended detection.** Select an existing protection ID and its risks,
   flow and code pointers. Inspect current helpers, failure paths and caller behavior.
   State the input, sensitive operation, safe behavior, supported scope and unknowns.
   A helpful name is not proof that a helper protects the actual output context.
   Save this understanding before rule creation; retain later corrections separately.
   Before investing in a full rule package, choose a capability route for each
   helper that matters to the detection. Save a small `.rig/helper-capabilities.json`
   note naming the helper, the behavior the rule needs, and one of:
   - automatic tracing, demonstrated on the installed engine in normal Rig mode;
   - explicit helper modeling, backed by inspected source and expressible with
     verified engine features in normal Rig mode; or
   - unsupported scope, retaining the original protection requirement and its gap.
   Inspect installed help and the actual Rig argument contract first. Use a small
   disposable, tests-first capability probe through normal Rig scanning before
   building a dependent rule. Record the invoked options, expected versus observed
   behavior and the chosen route. Optional direct-engine flags are a separate
   comparison, never evidence that normal Rig supports that behavior. If the probe
   fails, revise the route or report unsupported scope before investing further.
   Names alone cannot justify a modeled helper. Preserve the original unsafe and
   allowed obligations when a route is unsupported; do not turn the missing scope
   into an unannounced exclusion.
   When a caller rule or model relies on a helper, pair it with checks of that
   helper's actual guarantee. Record the canonical source and symbol, the exact
   identities and denial behavior the caller relies on, and the dependent rule and
   test paths in a small dependency note under `.rig/`. Write executable pure
   behavior tests for allowed and denied identities before trusting that guarantee.
   Where supported, add a narrowly scoped native rule and annotated tests that catch
   a broken guarantee without warning on unrelated helpers with the same name.
   Test the pair through normal Rig as well as native rule tests. If a source, rule
   or test dependency changes or disappears, inspect it and mark the old dependent
   evidence unusable until its meaning is rechecked. Save source, rule, test and
   dependency-evidence references under the same protection ID through MCP, then
   read them back without dropping earlier records or refreshing stale pointers.
   Reference freshness alone neither checks helper behavior nor disables a rule.
   State any missing enforcement or unsupported semantic scope explicitly.
2. **Write development tests first.** Include unsafe variants and allowed alternatives,
   aliases/wrappers, stored input, failure/unreachable paths and unrelated code as relevant.
   Explain whether an `ok` case is safe for this threat or outside a deliberately narrow
   warning. Never relabel a missed requirement as safe. Keep one rule and its annotated
   test file in a directory named after the rule ID. Only `ruleid` and `ok` annotations.
3. **Inspect the parsed code.** Probe the actual trusted engine version and supported
   options. Use its syntax-tree inspection on representative source. Explicitly check
   malformed input: files listed as scanned and exit zero alone do not prove parsing.
4. **Write and test the rule.** Prefer data-flow matching when caller data reaches a
   dangerous operation. Run native annotated tests, inspect exact finding lines, errors
   and analyzed targets. Use only features supported by this engine and Rig's normal
   path. Record required engine arguments with the rule. Do not assume unknown helper
   outputs safe or use a generic helper-name allowlist.
5. **Correct, then simplify and retest.** Preserve first-pass failures. Run final native
   tests and source scan after optimization. Do not execute dangerous fixture operations.
   Passing author tests are development evidence, never independent qualification.
6. **Freeze and independently qualify.** Read [candidate registration and evaluation](references/qualification.md) to obtain a real generated check ID. Use the supported `rig_evaluate` tool with the
   actual saved generated check ID; discover its current schema. Rig's private fresh
   evaluator must construct/freeze its own expectations without the candidate and return
   a safe decision and closed stage/reason/owner/next-action feedback. A tester
   failure is ungraded: preserve it and repair the named runtime/evidence stage.
   For a completed unsafe miss or safe alarm, add public source-grounded examples
   with expected and actual warning locations, repair and retest within the public
   development allowance before freezing. A saved rule is not tested or active.
   Do not call private scripts directly, inspect private cases,
   supply a self-written passing proof or tune against disclosed withheld cases.
   Honor budgets and existing authorization. Missing candidate registration, obsolete
   baseline-miss gates, unsupported runtime/options or permission denial mean incomplete,
   not permission to fabricate a miss or bypass evaluation. An independent public fixture
   review can assess finite behavior but cannot replace this production gate.
7. **Exercise the normal path and save references.** In an authorized isolated profile,
   verify exact rule bytes and required engine options survive normal Rig scanning.
   A direct-engine pass with extra flags does not qualify a different Rig mode. Preserve
   current source/configuration and prior evidence. Save actual rule, development test
   and bounded evidence report paths against the exact protection ID, even when their
   honest result is unqualified. Do not attach a rule to another requirement merely to
   raise a count. Read the area back through MCP to confirm preservation and fingerprints.

If a broad requirement is unsupported, preserve it and explain the missing scope.
An ignored-result warning cannot establish that every sensitive operation checks the
right identity; a warning on unreachable code is not a reachable exploit. Keep rejected,
errored and unsupported candidates visible. Independent failure must not disappear when
narrowing a detector. Changed/missing references require inspection, not blind re-saving.

Finish with a short outcome: created candidates; tested scope and failures; independent
qualification decision; normal Rig result; database save/readback; remaining gaps.
Link detailed evidence. Distinguish controlled fixtures, real-project source slices,
packaged tests and live installed-host behavior. A reference is not test success,
whole-area coverage, security assurance or activation authority.
