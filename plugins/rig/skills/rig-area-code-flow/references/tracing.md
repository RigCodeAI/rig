# Source-backed tracing

Literal selected Trail of Bits instructions follow. Apply them to the relevant
paths for the assigned threats, rather than every function in the application.
Here, "adversarial" means unverified outcomes to record, not a finding of harm.
The upstream "next phase" is independent rule qualification. Store concise prose
and pointers in Rig instead of a separate exhaustive audit document. Never submit
source blocks to the analysis database.

## Read the callees

This is the part that distinguishes a real analysis from a plausible one.

A caller's correctness usually rests on something a callee establishes. From the caller alone that dependency
is invisible: a bound looks enforced because the value came back from a function whose name implies a check.

So when the callee's source is available — internal or external, it makes no difference — read it, and record
what the caller depends on it to establish. Walk every path through the callee, not only the one that returns
successfully. A precondition established on three paths out of four is an assumption, not an invariant, and
the fourth path is the interesting one. An output parameter left unwritten on an early return, a check that
sits behind a conditional, a loop that can exit before it validates: these are what you are looking for.

When source is not available, the callee is adversarial. Record what is sent to it, what is assumed about it,
and the outcomes you have not excluded: failure, a hostile return value, an unexpected state change, re-entry
into your caller before its own writes land.

For every assumption, name where it is established. When nothing establishes it, write "nothing found" —
that is a finding for the next phase, and it is the single most valuable thing you produce.

## Grounding

Cite a line for every structural claim. If you cannot point at one, do not assert it — put it in open
questions as "unclear; need to inspect X". Never infer behavior from a name: a function called
`validate_length` may not validate anything. When new evidence contradicts something you wrote earlier,
correct it in place and say what changed.

No hedge words. "Probably", "seems to", and "should be" each resolve to either a cited claim or an open
question.

Depth follows the code. Branches, external calls, and state mutations earn analysis; a three-line block that
copies a value earns three lines. There is no minimum count of invariants or assumptions — a short record
whose claims each cite a line is worth more than a long one padded to fill a template. Returning few
invariants because the function has few is correct. Returning open questions is a complete analysis;
leaving them unwritten is not.


## Conventions

Cite lines as `L45` or `L98-L102`. Label code blocks with the language. For every assumption, say what makes
it true — and write `nothing found` when nothing does.

Spend words where the code earns them. Branches, calls out, and anything that changes stored data deserve
real attention; three lines that copy a value deserve three lines back. There is no minimum number of
anything. Padding a section to hit a count produces text that looks like analysis and isn't.

Leave a section out only when it is genuinely empty, and say so: "No external calls." A missing section could
mean "none" or "never checked", and the reader cannot tell which.

## Before you finish

Check that every claim either cites a line or sits in Open Questions. Check that you followed every path
through each function called, not just the one that succeeds. If something you wrote earlier turns out to be
wrong, fix it where it stands and say what changed.

Cut the hedges. "Probably", "seems to", and "should be" each become either a claim with a line number or an
open question.

Finishing with open questions is a complete analysis. Finishing with open questions you never wrote down is
not.
