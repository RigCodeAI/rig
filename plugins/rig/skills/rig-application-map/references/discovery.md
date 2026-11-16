# Scoped Cloudflare discovery

Adapted from Cloudflare security-audit-skill, pinned revision
`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, MIT; see [license](../LICENSE).
These are source-reading passes in one session, not subagent assignments.
Return mapping facts with pointers; locate controls without claiming they work.
The omitted full-audit, execution and hunting instructions do not apply.

**Agent 1a: Product, stack, and local operation**

```text
Read the target at <target>. Do not use network access. Return:
1. Product type, users, operators, and ordinary trust-sensitive actions.
2. Languages, frameworks, build system, runtimes, and locally visible deployment models.
3. Repository-relative entry points and subsystem boundaries.
6. Missing local toolchains or runtime facts that limit bounded execution.
Return only source facts with repository-relative file:line references.
```

**Agent 1b: Principals, authority, and controls**

```text
Read all source that establishes identity, authorization, isolation, and privilege. Map:
1. Each lower-trust principal and the actions it has by design.
2. Authentication or peer identity at each entry surface.
3. Per-resource authorization and tenant/owner scope.
4. Process, browser, workload, CI, plugin, model/tool, device, or local-IPC authority.
6. Which controls are source-visible and which depend on an unobserved deployment fact.
Return trust boundaries and control locations with repository-relative file:line references. Do not infer live reachability.
```

Keep authority descriptions broad. Do not trace failures or assess guarantees.

**Agent 1c: Entry surfaces, copies, and sinks**

```text
Inventory every source-visible place external or lower-trust input enters:
- HTTP/browser, RPC/message/protocol, files/archive/document, CLI/env/config, plugins/dependencies/CI, cloud events/IAM selectors, model context/tool arguments, mobile/deep-link/webview, and local IPC.
For each surface, follow major transformations, stored or derived copies, and security-relevant sinks. Record source-visible limits and parallel paths to the same effect.
Return repository-relative paths and line numbers. Be complete, but do not execute or send inputs.
```

Stop at the major entry, transformation, stored/queued hop and operation.
Detailed function tracing belongs to a later stage.

**Agent 1d: Local execution and deployment visibility**

```text
Read tests, build definitions, manifests, packaging, and maintained environment overlays. Return:
3. Commands that would fetch dependencies, publish artifacts, contact paid/provider APIs, or affect shared state; mark them prohibited for this run.
5. The final active source path for each deployment mode only where the repository selects it deterministically.
```

Record missing deployment facts as unknown. No target code runs in this stage.

## Connected summary

Use these selected source slots for the saved map and the short user report:

1. Product, principals, normal authority, and protected resources.
3. Tech stack, source-visible deployment paths, and offline build/test limits.
4. Entry surfaces and the important source-to-sink or lifecycle paths.
6. Repository-relative starting paths.

Locate source-visible controls at trust boundaries without ranking or certifying
them. Store broad paths and source pointers in area bundles, and reconcile each
entry/operation family to a named area or an explicit scope exclusion.
