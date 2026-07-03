# Agent Handoff and Implementation Plan

## Mission

Create a publishable Codex skill for Bazi analysis that is more robust than a mechanical 《千里命稿》 skill.

The target behavior:

- Calculate chart facts instead of relying on memory.
- Interpret through several classical lenses.
- Use 《千里命稿》 for practical event-reading and calibration, not for deterministic copying.
- Make uncertainty visible.
- Keep culturally framed advice reflective and non-fatalistic.

## Design Thesis

The main failure mode in a single-book skill is overfitting:

```text
classical phrase -> direct modern conclusion
```

This skill should instead force:

```text
birth data -> chart facts -> season/strength/structure -> timing activation -> Qianli-style calibration -> revised advice
```

The user should feel the agent is reasoning from a chart, not reciting a book.

## Repository Architecture

```text
zhizhi-bazi-skill/
  SKILL.md
  AGENTS.md
  agents/
    openai.yaml
  references/
    analysis-protocol.md
    classical-lenses.md
    qianli-method.md
    tables.md
    edge-cases.md
    safety-tone.md
    agent-handoff.md
  scripts/
    calc_bazi.py
```

### `SKILL.md`

Role: runtime entrypoint.

It should answer:

- When should the skill trigger?
- What data should the agent collect?
- Which file should the agent read for which need?
- What is the high-level workflow?
- What output rules and safety boundaries apply?

It should not contain long tables or long classical discussions.

### `references/analysis-protocol.md`

Role: reasoning engine in prose.

It defines the ordered workflow:

1. Chart facts.
2. Season and regulation.
3. Day-master strength.
4. Structure and useful gods.
5. Luck and timing.
6. Qianli-style event calibration.
7. Final advice.

When extending this file, preserve the order. The order is the anti-mechanical guardrail.

### `references/classical-lenses.md`

Role: book-role map and conflict resolver.

Each book has a job:

- 《渊海子平》: foundations and ten gods.
- 《子平真诠》: structure and useful-god integrity.
- 《滴天髓》: strength, flow, and obstruction.
- 《穷通宝鉴》/《造化元钥》: regulation and seasonal need.
- 《三命通会》: broad lookup and special patterns.
- 《千里命稿》: practical reading and case analogy.
- 《神峰通考》: anti-mechanical review.
- 《命理约言》: conservative adjudication.
- 《五行精纪》, 《星平会海》, 《兰台妙选》: auxiliary or extended methods.

If you add books, assign them a job. Do not add them as decorative authority.

### `references/qianli-method.md`

Role: use 《千里命稿》 safely.

This file should remain practical:

- Palace reading.
- Event reading.
- Case analogy.
- Calibration style.
- Revision rules.

Do not paste long passages. Convert useful ideas into operational checks.

### `references/tables.md`

Role: stable lookup data.

Tables belong here when they are short and stable:

- Stems and branches.
- Hidden stems.
- Ten-god derivation.
- Branch relations.

If a table becomes large or contested, split it into a separate reference and mention the convention.

### `references/edge-cases.md`

Role: fragile inputs and school disputes.

Keep adding cases here when real use reveals calculation pitfalls:

- Late Zi hour.
- Solar-term boundary.
- Lunar-only date.
- Unknown birth time.
- True solar time.
- Deceased subject.
- Children.
- Health, fertility, marriage, finance.

### `references/safety-tone.md`

Role: output language policy.

This file is part of the product, not legal boilerplate. It prevents the skill from becoming scary, fatalistic, or overconfident.

### `scripts/calc_bazi.py`

Role: deterministic chart fact helper.

Current scope:

- Gregorian date input from 1900 to 2100.
- Approximate solar-term boundaries.
- Year/month/day/hour pillars.
- Late Zi convention.
- Hidden stems and ten gods.
- Dayun direction and approximate start age.
- JSON or text output.

Known limitation:

- Solar terms use compact date approximations. Birthdays within one day of a solar term must be verified with a trusted calendar.
- Lunar conversion is intentionally not implemented.
- True solar time correction is intentionally not implemented.

Do not expand this script with interpretation prose. Keep it focused on facts.

## Multi-Agent Task Split

If several agents are working in parallel, split work this way:

### Agent A: Calculation

Owns:

- `scripts/calc_bazi.py`
- calculation tests
- calendar warnings

Acceptance criteria:

- `--self-test` passes.
- Sample charts produce stable JSON.
- Boundary warnings are emitted near solar terms and late Zi hour.

### Agent B: Reasoning Protocol

Owns:

- `references/analysis-protocol.md`
- `references/classical-lenses.md`

Acceptance criteria:

- No single book can dominate the output.
- Conflict priority is explicit.
- Full reading template is clear.

### Agent C: Qianli and Calibration

Owns:

- `references/qianli-method.md`

Acceptance criteria:

- Event calibration uses chart evidence.
- Palace reading is practical but not deterministic.
- Revision rules are explicit.

### Agent D: Safety and User Experience

Owns:

- `references/safety-tone.md`
- boundary sections in `SKILL.md`

Acceptance criteria:

- No frightening fixed claims.
- Health, money, marriage, death, and children have clear guardrails.
- Output remains warm and useful, not legalistic.

### Agent E: Packaging and Release

Owns:

- `agents/openai.yaml`
- validation
- git commit and GitHub publish

Acceptance criteria:

- Skill validator passes.
- Git status contains only intended files.
- Remote repository is public unless the user asks otherwise.

## Validation Checklist

Run from the skill root:

```bash
python scripts/calc_bazi.py --self-test
python scripts/calc_bazi.py --date 1990-05-15 --time 08:30 --sex male --json
python <skill-creator-path>/scripts/quick_validate.py .
```

Expected:

- Self-test prints `self-test passed`.
- Sample JSON includes four pillars, day master, dayun direction, and warnings if applicable.
- Validator reports success.

## Definition of Done

The skill is ready to publish when:

- `SKILL.md` is concise and complete.
- All referenced files exist.
- Calculation script passes smoke tests.
- `agents/openai.yaml` is generated.
- `AGENTS.md` tells future agents where to start.
- Git has a clean initial commit.
- GitHub remote exists and push succeeds.

## Future Improvements

Good next steps:

- Add verified ephemeris-based solar terms.
- Add optional lunar-to-Gregorian conversion with tests.
- Add fixture charts from trusted calendars.
- Add a scoring helper for element balance that reports evidence rather than final fate.
- Add example prompts as test cases for forward evaluation.

Avoid:

- Adding long public-domain text dumps without operational summaries.
- Making the script issue fate judgments.
- Expanding special stars before core chart mechanics are reliable.
