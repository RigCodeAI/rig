# Run this area's caller contrasts through Rig

A helper's own tests cannot prove its callers invoke it or stop on denial. Keep
helper-guarantee tests and add finite tests for each area's actual path: allowed
caller proceeds, denied caller cannot reach the sensitive action, and a broken or
ignored guard is detected. Use harmless in-memory substitutes for dangerous actions;
do not contact services, install dependencies or alter application source/manifests.

Write tests under `.rig/caller-tests/<area>.<ext>` using an existing installed runtime.
Read the real caller and helper; test their actual behavior rather than matching
names/strings. Keep the independent private evaluator separate: these are public
development/applicability tests, never independent detector qualification.

## Register through the existing configuration contract

Coordinate one configuration writer with the root agent. Read `.rig/checks.toml`
and append one ordinary candidate/advisory check, preserving all existing entries.
This is the repository-owned CONFIG format, not a new registration MCP API. Do not
invent a discovered candidate ID or replace an existing helper check to run new tests.

The following is the complete required shape for a small Python example. Replace
paths, ID and installed interpreter/PATH with inspected actual values; other
languages use their installed runtime and safe test entry point.

```toml
[[checks]]
id = "area-caller-tests"
source = ".rig/caller-tests/area.py"
statement = "Exercise allowed and denied caller paths"
argv = ["/absolute/installed/python3", "-B", ".rig/caller-tests/area.py"]
authority = "candidate"
mode = "advisory"
owner = "local setup caller tests"
read_only = true
approval_inputs = ["**"]
execution_path = "/absolute/installed/bin:/usr/bin:/bin"
env = {}
timeout_ms = 5000
output_limit_bytes = 65536
paths = ["**"]
inputs = ["**"]
complete_inputs = false
```

Keep existing `schema_version = 1`; a new CONFIG needs it before `[[checks]]`.
Do not add scanner/generated-check fields. The `source` and an argv file argument
must name the exact caller-test file. Use an absolute trusted interpreter, an
absolute execution PATH, empty environment and conservative all-input bindings.
Choose bounded timeout/output sufficient for the safe tests within remaining budget.
Do not set `complete_inputs` or narrow inputs to make stale evidence pass.

## Review, approve, execute, preserve

1. Call public `rig_review` for this actual configured check ID. Inspect executable,
   argv, source, inputs, environment and limits; configuration validity is not test
   execution. If rejected, fix the actual CONFIG without dropping earlier checks.
2. Reuse current command execution authorization when `execution_approved` is true.
   Otherwise, only within the owner's actual safe-test execution authority, use
   `rig_manage` with command `checks` and arguments
   `["approve","--id",CHECK_ID,"--digest",REVIEWED_DIGEST]`. Never invent consent,
   edit approval storage, weaken host permissions or infer approval from a fixture.
3. Use `rig_check` on the selected ID and inspect its actual result. It must execute
   the new tests, complete, and have current bindings; saved helper receipts and
   zero collection are insufficient. Retain named cases, expected outcomes and
   observed behavior in bounded public evidence. Preserve failures too.
4. Recheck receipt freshness after candidate/config/rule changes; rerun these exact
   caller tests and review changed execution bindings when needed. An older helper
   or pre-change caller receipt cannot stand in for a current run.
5. Save this area's exact `test` references and invocation/denial pointers under the
   canonical protection membership. Record actual check/result IDs in the link's
   `applicability_test` and/or appended `caller_observations`. Use
   [the shared contract](../../rig-onboarding-coordinator/references/shared-protections.md)
   for fields and save/readback rules. The closed receipt bridge checks configured
   source/argv, exact bound test files and actual current result; agent-written JSON
   or arbitrary helper receipts cannot substitute.

A current complete successful receipt is needed for adoption/support. A violation
may document a contradicted caller, which stays unresolved. Missing runtime, approval,
collection, receipt or exact file binding is an explicit gap. These finite tests can
still be semantically mistaken; they do not create an infallible safety oracle.
