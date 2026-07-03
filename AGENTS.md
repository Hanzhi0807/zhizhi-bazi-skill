# Agent Handoff

This repository contains a Codex skill named `zhizhi-bazi-skill`. If you are another agent continuing the work, first read:

1. `SKILL.md` for the user-facing skill workflow.
2. `references/agent-handoff.md` for architecture, task boundaries, and validation rules.
3. `scripts/calc_bazi.py` before modifying calculation behavior.

## Current Objective

Build and maintain a Bazi skill that improves on single-text, mechanical 《千里命稿》 readings by combining:

- Deterministic chart calculation where possible.
- Multi-classic interpretation lenses.
- Explicit conflict resolution.
- Historical calibration before confident final advice.
- Conservative safety and uncertainty language.

## Development Rules

- Keep `SKILL.md` short and procedural. Move detailed knowledge to `references/`.
- Keep deterministic math in `scripts/`, not prose instructions.
- Do not add broad classical quotations unless they change a concrete decision rule.
- Do not make the skill depend on one book. 《千里命稿》 is a method layer, not the final authority.
- When adding a new rule, state which failure mode it prevents.
- Run `python scripts/calc_bazi.py --self-test` after script changes.
- Run the skill validator before committing.

## File Ownership

- `SKILL.md`: routing, workflow, output rules, boundary triggers.
- `references/analysis-protocol.md`: reasoning sequence and output template.
- `references/classical-lenses.md`: book roles and conflict adjudication.
- `references/qianli-method.md`: practical event-reading and calibration rules.
- `references/tables.md`: stable lookup tables.
- `references/edge-cases.md`: fragile calendar and safety-sensitive scenarios.
- `references/safety-tone.md`: non-fatalistic language constraints.
- `scripts/calc_bazi.py`: chart facts and approximate dayun calculation.

## Before Publishing

Confirm:

- Skill metadata validates.
- Calculation smoke tests pass.
- A sample chart produces readable output.
- `agents/openai.yaml` exists and matches the skill.
- Git history has a clean commit with no unrelated workspace files.
