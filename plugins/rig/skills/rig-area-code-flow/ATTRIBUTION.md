# Attribution and adaptation

This skill adapts Trail of Bits, **audit-context-building**, from
[trailofbits/skills](https://github.com/trailofbits/skills/tree/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/audit-context-building),
revision `e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff`, under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The full license is in `LICENSE`. This adaptation is distributed under the same license.

`references/tracing.md` literally copies the function analyzer's **Read the callees**
and **Grounding** sections and ANALYSIS_FORMAT's **Conventions** and **Before you finish**.
No wording inside those selected sections was changed.

Adaptation: bound tracing to existing area threats; replace separate exhaustive
per-function documents and source blocks with ordered MCP flow records and file
pointers. Treat unavailable source as unknown outcomes, not proof of a defect.
Add real language failure order, transformation counterexamples, safe-code rule
motivation, full-bundle preservation, source freshness and readback. No upstream
exhaustive-audit orchestration or vulnerability hunting is included.

The experiment's `adaptation.json` records original paths, hashes and copied ranges.
