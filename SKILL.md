---
name: zhizhi-bazi-skill
description: Classical Chinese Bazi skill for 四柱八字排盘、命理分析、运势/大运/流年解读、千里命稿风格断事校准, and culturally framed fortune-telling requests. Use when the user asks to 算八字、看八字、批八字、排四柱、分析命盘、看大运流年、用千里命稿分析、or wants a Bazi birth chart interpreted with multiple classical references and cautious uncertainty handling.
created: 2026-06-16T22:50
updated: 2026-07-03T00:00
---

# Zhizhi Bazi Skill

Use this skill for culturally framed Bazi analysis. Treat Bazi as traditional culture and reflective interpretation, not as scientific prediction or professional medical, legal, financial, or psychological advice.

## Operating Principles

- Prefer reliable calculation over mental arithmetic. For Gregorian birth data, run `scripts/calc_bazi.py` before interpreting.
- Do not let any single text, including 《千里命稿》, dominate the reading. Use it mainly for practical event-reading, palace positions, and case-style reasoning.
- Resolve conflicts by this priority: solar-term boundaries and chart facts > season and regulation needs > day-master strength and flow > structure and useful gods > luck-cycle activation > ten-god/palace symbolism > stars and special sayings.
- Mark uncertainty explicitly when the birth time, calendar conversion, solar-term boundary, school convention, or historical calibration is unclear.
- Do not make frightening, absolute, or irreversible claims. Phrase difficult patterns as tendencies, pressures, or topics to handle carefully.

## Reference Routing

Read only the files needed for the task.

### Methodology & Protocol (always available)

- `references/analysis-protocol.md`: full workflow, output structure, calibration loop, and conflict rules.
- `references/classical-lenses.md`: how to assign roles to classical texts and avoid blind quotation.
- `references/qianli-method.md`: how to use 《千里命稿》 as a practical method without becoming mechanical.
- `references/tables.md`: stems, branches, hidden stems, ten gods, branch relations, nobility stars, inauspicious stars (凶煞), twelve growth stages (十二长生), and common lookup tables.
- `references/edge-cases.md`: late Zi hour, solar terms, lunar dates, uncertain birth time, true solar time, and other fragile cases.
- `references/safety-tone.md`: wording boundaries for wealth, relationships, and major life decisions.
- `references/agent-handoff.md`: maintainer-only implementation plan for other agents extending or auditing this skill.

### Classical Source Texts (L0 — read when original text verification is needed)

- `references/source-texts/穷通宝鉴.md`: seasonal regulation by day-master and month
- `references/source-texts/滴天髓阐微.md`: strength, flow, obstruction, and transformation
- `references/source-texts/子平真诠.md`: structure purity, useful gods, success/failure conditions
- `references/source-texts/渊海子平.md`: ten gods, six relations, foundational patterns
- `references/source-texts/千里命稿.md`: practical palace reading and event-style judgments
- `references/source-texts/三命通会.md`: encyclopedia of special structures, stars, and exceptions
- `references/source-texts/神峰通考.md`: disease-and-medicine theory, anti-mechanical review
- `references/source-texts/兰台妙选.md`: nayin and special classical patterns (lowest priority)

### Executable Rule Summaries (L1 — read during the corresponding analysis step)

| Analysis Step | Rule File | Content |
|:---|:---|:---|
| Step 2: Season & Regulation | `references/rules/rules-qiongtong.md` | Day-master × month 调候用神 lookup table |
| Step 3: Strength & Flow | `references/rules/rules-ditian.md` | Strength/weakness judgment, flow, 通关, 寒暖燥湿 |
| Step 4: Structure & Useful Gods | `references/rules/rules-ziping.md` | 用神成败救应, 格局纯杂高低, 相神, 清澈浑浊判断 |
| Step 5: Flow & Circulation | `references/rules/rules-ditian.md` | 通关, 流转, 寒暖燥湿, 气势流通 |
| Step 6: Event Calibration | `references/rules/rules-qianli.md` | Palace positions, 十神事件映射, 历史校准方法 |
| All steps (foundation) | `references/rules/rules-yuanhai.md` | Ten gods table, 六亲配法, 基础格局速查 |
| Error checking | `references/rules/rules-shenfeng.md` | 病药说, 辟谬, 反机械判断清单 |
| Special structures | `references/rules/rules-sanming.md` | 特殊格局 (从格/化气格), 神煞速查, 纳音表 |
| Auxiliary (nayin) | `references/rules/rules-lantai.md` | 纳音特殊格局 (lowest priority) |

**Reading priority for L1 rules**: Always read `rules-yuanhai.md` for foundation. Read the rule file matching your current analysis step. Others on demand.

## Information Collection

Collect the minimum data first:

1. Gregorian birth date, preferably `YYYY-MM-DD`.
2. Birth time, preferably `HH:MM`; accept "unknown" or an approximate time range.
3. Sex used by the traditional dayun direction rule: male or female.
4. Birthplace if available; use it for a true-solar-time caveat rather than exact correction unless you have a reliable longitude source.

> ⚠️ **Two date pitfalls to confirm at intake:**
> - **Gregorian vs. lunar:** Many Bazi books and family records give lunar dates without labeling them. If the user's date comes from a命理书 or老黄历, **explicitly confirm whether it is Gregorian or lunar** before running the script. A lunar date fed to `calc_bazi.py` as if Gregorian will produce an entirely wrong chart (wrong day master, wrong structure). If only a lunar date is available, do not convert from memory — ask for a trusted conversion or see `edge-cases.md` "Lunar-Only Dates".
> - **Year range:** `calc_bazi.py` only supports **1900–2100**. Historical figures born before 1900 (common in classical case studies: 朱熹, 王安石, 曾国藩, 左宗棠, 章太炎, 慈禧…) cannot be calculated by the script. For these, ask the user for a pre-computed chart or state that the script cannot verify it.

Optional calibration data:

- Lunar birth date if the Gregorian date is unknown. Do not convert lunar dates from memory; ask for a Gregorian date, a trusted conversion, or state that the chart cannot be reliably calculated.
- 2-4 known past events with approximate years, only after an initial chart is available.
- Name and former names only if the user specifically wants name-related folk interpretation; they are not required for Bazi charting.

## Calculation Workflow

When Gregorian date is available:

```bash
python scripts/calc_bazi.py --date YYYY-MM-DD --time HH:MM --sex male
```

Optional arguments:

```bash
python scripts/calc_bazi.py --date YYYY-MM-DD --time unknown --sex female
python scripts/calc_bazi.py --date YYYY-MM-DD --time 23:30 --sex male --json
python scripts/calc_bazi.py --date YYYY-MM-DD --time 08:15 --sex female --self-test
```

Use the script output as chart facts. If the script emits warnings, carry those warnings into the interpretation. For dates close to a solar term boundary, explain that a high-precision ephemeris or trusted calendar should confirm the pillar.

## Interpretation Workflow

Follow this sequence:

1. State chart facts: four pillars, hidden stems, ten gods, dayun direction, approximate start age, and current luck cycle. **Read `dayun-rules.md` to verify direction and cycles.**
2. Add five-element count and strength summary after chart facts: count 金/木/水/火/土 occurrences across stems + branch hidden stems, note the strongest and weakest/missing element.
3. Add nobility and star analysis (神煞分析) if relevant or requested: look up both auspicious stars (吉神: 天乙贵人, 太极贵人, 天德/月德, 文昌, 国印, 福星, 将星, 驿马, 华盖, 金舆, 学堂, 词馆) and inauspicious stars (凶煞: 羊刃, 劫煞, 灾煞, 桃花, 红艳, 孤辰, 寡宿, 亡神, 元辰, 空亡, 阴差阳错, 十恶大败) in `tables.md`. Mark which appear in the original chart vs which need dayun to supplement. Assess the balance between auspicious and inauspicious stars.
4. Assess season and climate needs before choosing a useful god. Read `rules-qiongtong.md` and **`classical-texts.md` (穷通宝典 section)** for seasonal regulation logic. **Give a 调候得失评级 (优/良/中/差) and cite the specific 穷通宝典 dictum.**
5. Assess day-master strength using command, roots, twelve growth stages (十二长生), support, drain, control, and flow. Read `rules-ditian.md` for strength/flow rules. Read `tables.md` for the twelve growth stage lookup tables.
6. Identify structure only after strength and season are understood. Read **`classical-texts.md` (子平真诠 section)** for structure rules. Assess clarity vs turbidity (清澈与浑浊): is the structure clean or mixed? Is the useful god protected or damaged? Are there conflicting elements? Read `rules-ziping.md` for structure purity and rescue logic — **判断格局前必须执行 `analysis-protocol.md` Step 4.0 "格局判断三段式校验"**（候选枚举 → 透干信号扫描 → 对立假设检验 + Anti-Pattern 回查），并查 `rules-ziping.md` "二·补：透干变格速查表"确认月令本气不透时透干十神能否另起格局。**Cite the specific 子平真诠 rule for the identified structure. Give three ratings in the conclusion: 格局清纯度初评, 有情有力初评, 成格救应初评 (each 优/良/中/差). The first will be revised after step 7.**
7. Assess flow and circulation (流转分析): analyze on three layers — **heavenly stem flow** (天干流转: chain of stem interactions), **earthly branch flow** (地支流转: chain of branch interactions including hidden stems, combinations, clashes), and **heaven-earth connection** (天地流转: roots, exposed stems,虚实). Read `rules-ditian.md` and **`classical-texts.md` (滴天髓 section)** for flow and obstruction logic. **Cite the specific 滴天髓 principle. Give a 流转顺畅度评级 (优/良/中/差) in the conclusion, based on whether the flow direction matches the structure's needs.**
8. **Assess image/formation (形象分析) — the fourth analytical lens**, alongside strength/regulation/structure. First scan whether the chart's qi is concentrated in one or two elements. If yes (two-line mutual generation like 木火通明/金水相生, or one-line dominance like 曲直/炎上), apply the image lens: the image must not be broken (象不可破) — elements that would normally be useful may become harmful if they break the image. Read `rules-ditian.md` section 七"形象与成象". If the chart's elements are dispersed (3+ lines with normal generation/control), skip this step. **Give a 形象得失评级 (优/良/中/差/不适用).**
9. **Summarize the comprehensive structure grade (格局综合评价):** collect the five ratings already given in steps 4, 6, and 7 (plus the image rating from step 8 if applicable); map them to the 九等等级表 in `rules-ziping.md`. Use **《神峰通考》病药说** to summarize: what is the chart's "病" and what does the current dayun provide as "药"? This is a **summary, not a new analysis** — all evidence must have been stated in previous steps.
10. Read dayun and annual activation as timing, not as isolated fate. Use **《千里命稿》 palace and ten-god logic** to connect dayun to life domains.
11. Use 《千里命稿》-style palace and event logic to propose 2-4 historical calibration points.
12. After user feedback, revise strength/useful-god/flow assumptions before giving final advice.

For the detailed sequence and output format, read `references/analysis-protocol.md`.

## Output Rules

- Include a short cultural-reference disclaimer near the start or end.
- Separate chart facts from interpretation.
- Use confidence labels: high, medium, low.
- Where two schools differ, name the convention used and give the alternative if it materially changes the result.
- Avoid over-quoting classics. Cite a text only when that text's rule actually affects the judgment.
- End with practical, non-fatalistic suggestions framed as choices and habits.

## Boundary Handling

Before interpreting, read `references/edge-cases.md` if any of these appear:

- Birth near 23:00, midnight, a solar-term boundary, or Li Chun.
- Unknown or approximate birth time.
- Lunar-only date, leap month, or calendar conversion uncertainty.
- Birthplace far from the time-zone meridian.
- Deceased person, child chart, or request about wealth, marriage, pregnancy, death, lawsuits, or investment.

If the chart cannot be calculated reliably, say what information is missing and offer a partial reading only when the uncertainty is contained.
