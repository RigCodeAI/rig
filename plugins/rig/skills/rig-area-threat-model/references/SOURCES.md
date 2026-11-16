# Sources and adaptation

Cloudflare security-audit-skill, revision c1c8a8c1471069fb0e188eeaff69b8e8db6564a8,
MIT, copyright 2025–2026 Cloudflare, Inc. Three selected passages are copied
literally into threat-questions.md. Full notice: LICENSE-Cloudflare.txt.

- RECONNAISSANCE.md: principals/authority and input-to-operation questions.
- ATTACK-CLASSES.md: access control, indirect injection and notification URL questions.

Pinned source URLs:
https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md
https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md

Adaptation: Rig selects concrete boundaries in one saved area, describes potential
harm and requirements even for currently safe code, and persists via native MCP.
It does not adopt upstream full-audit orchestration, vulnerability confirmation,
scoring, fixing, execution or exhaustive hunting.

OWASP Threat Modeling and Attack Surface Analysis Cheat Sheets inform the general
boundary-to-threat approach. They are linked only, not copied or adapted text:
https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html
Prior research recorded revision 757270a26306e5edda9957bb7f86cfcde03c30f9.
The twelve-question table and Rig procedure are newly written for this scope.
