---
name: rig-setup
description: Set up the default security scan or update installed Rig components. Application mapping and custom-rule building are paused.
---

# Default scan setup

## Updating Rig

When the user asks to update Rig, use the active standalone CLI from the host's
terminal: `rig update --all --json`. That request supplies update authorization;
reuse it. Read the result for standalone, Codex and Claude independently. Preserve
pins, disabled integrations, host trust and project command approvals. Follow the
reported reload instructions and return after reporting the update outcome.

If the standalone CLI is unavailable, report that component and use the current
host's plugin manager after inspecting its Rig marketplace source. Codex uses
`codex plugin marketplace upgrade rig`. Claude uses
`claude plugin marketplace update rig` followed by
`claude plugin update rig@rig --scope user` for its user installation. Preserve
other sources and scopes and report the owning host command. Codex needs a new
session; Claude supports `/reload-plugins` or a new session. Installing/updating
does not approve hooks or tools. Automatic CLI updates remain an explicit opt-in.

## Default scan preparation

Normal setup is default-pack setup only. Do not map the application, model threats,
trace code flows, delegate area work, build custom rules, start evaluators, or
resume a saved generation worklist. Do not create compiler recipes, application
models, development tests or coverage inventories as part of setup. Report
unsupported files and scanner errors as gaps; do not expand setup to solve them.
The retained [advanced onboarding](advanced-onboarding.md) is paused until the
owner explicitly re-enables it. A request to set up, update or resume Rig alone
never enables advanced onboarding. Existing rules, analysis and outcomes stay intact.

Use the installed Rig MCP tools. Read the sibling [Rig skill](../rig/SKILL.md)
for setup choices, exact configuration consent, finding handling and code changes.
Reuse authorization already given for its actual scope. Host tool and hook trust
still apply. Never change permissions or approval storage to make setup work.

1. Read `rig_setup` with arguments ["--project"] and ["--lifecycle"]. Preserve
   existing configured scanners, rules and owner choices. Resume their status
   rather than replacing configuration. Do not start a new `--begin` pause for
   default-only setup.
2. If preparation_required is true, explain the scanner/rule downloads and obtain
   any missing preparation authorization. Use `rig_manage` command setup with
   arguments [] to prepare the scanner and pack, then refresh --project. The pack
   combines bundled njsscan JS/TS rules with the cached/downloaded Registry
   p/default rules for other languages. Existing scanner selections are reused.
   Missing/broken tools or rules need explicit repair; never replace an owner's
   choice or repeat failed preparation indefinitely.
3. If no security check is configured, preview `rig_setup` with arguments
   ["--candidate", "opengrep-default"], without custom rules, targets or models.
   Show the pack, advisory status, scan scope and .rig/checks.toml configuration.
   Obtain missing consent to save the exact proposal. Apply through `rig_manage`
   command setup with ["--candidate", "opengrep-default", "--apply", "--digest",
   TOKEN]. This freezes the prepared rules locally and preserves existing checks.
   No repository test/lint import, required-policy activation or new hook connection
   is part of normal setup.
4. Choose one existing, representative source file no larger than 64 KiB.
   Avoid generated files, tests and `.rig/` inputs. Run the saved check through
   `rig_manage` command `checks` with arguments ["run", "--id", "ID", "--path", "FILE"].
   This real scan validates scanner launch, output parsing and saved evidence for
   that file only. Report the exact file, findings, diagnostics and coverage limits.
   If no suitable file exists, report validation as unavailable without scanning
   the whole project. Do not repair pre-existing findings to complete setup.
   A whole-project inventory requires a separate explicit request.
   A model-backed scanner cannot run on one file. Report that boundary and use
   `--whole-project` only after an explicit whole-project request.
5. If --lifecycle reports initial_setup from an earlier advanced attempt, finish
   that pause under setup/report authorization. Reuse the existing assessment path
   returned by --report, preserving its gaps and spent attempts. If none exists,
   write .rig/setup-assessment.json containing components, targets, sources and
   sinks as empty arrays, measures.initial as {}, and remaining_gaps with the
   reason "Default-pack setup only; application coverage was not assessed" and
   next_action "Use configured scans; advanced onboarding is paused". Empty arrays
   mean unassessed, never no applicable threats. Preview --profile ASSESSMENT and
   save with the same arguments plus --apply --digest TOKEN through rig_manage.
   Then call rig_manage setup ["--complete"] and confirm initial_setup=false.
   Saving a report alone does not end the pause. Do not restart advanced work.
6. Call `rig_finish` with the same file path when validation ran. Give a short
   result: configuration saved/reused, validation completed or blocked, findings
   and gaps. Setup ends here. Use rig_context,
   rig_check and rig_finish during subsequent code changes, preserving hook-supplied
   task_handle. Installed trusted hooks still provide changed-code checkpoints;
   do not request scanner execution grants or install duplicate hooks. Missing
   host trust/delivery is a stated limitation, not a reason to start custom authoring.

A prepared pack, saved configuration and scoped validation are separate outcomes.
Default rules are background protection, not project-specific or complete security
coverage. Keep prior inactive candidates and reports as history; do not retry them
as part of default setup or routine coding.

Routine `rig_check` calls must supply files (`paths` or `since`) or the existing
`task_handle`. Saved setup settings are reused; missing or unsupported scope
never falls back to a whole-project scan.
