# Analysis Protocol

## Purpose

This file defines the reasoning workflow. It keeps the agent from acting like a quotation engine and forces each conclusion to pass through chart facts, classical lenses, timing, and calibration.

## Minimal Workflow

1. Collect Gregorian birth date, birth time, sex, and birthplace if available.
2. Run `scripts/calc_bazi.py` for chart facts when Gregorian date is available.
3. Read warnings from the script before interpretation.
4. Add five-element count summary after chart facts: count 金/木/水/火/土 across stems + hidden stems, note strongest and weakest/missing.
5. Read `tables.md` when ten-god, hidden-stem, branch relation, twelve growth stages, or nobility-star lookup details are needed.
6. Read `classical-texts.md` before making structure, regulation, or flow judgments. **Each classical citation must be specific enough to affect the judgment — do not quote decoratively.**
7. Read `dayun-rules.md` before calculating or verifying dayun direction and cycles.
8. Read `classical-lenses.md` before selecting useful gods or resolving conflicts.
9. Read `qianli-method.md` before making event-style judgments.
10. Read `safety-tone.md` before discussing wealth, marriage, children, death, or major decisions.

## Reasoning Order

### 1. Chart Facts

Keep facts separate from interpretation:

- Year, month, day, and hour pillars.
- Day master.
- Hidden stems.
- Ten gods by pillar.
- Solar-term warnings.
- Dayun direction and approximate start age.
- Current dayun and current year if requested.

Do not infer personality or fate until this section is complete.

### 1.5 五行个数与强弱统计

在排盘事实之后，统计四柱（含天干+地支本气+中气+余气）中五行出现的次数，作为辅助参考：

- 金（庚、辛、申、酉、丑中辛、戌中辛、巳中庚、辰中辛）：
- 木（甲、乙、寅、卯、亥中甲、辰中乙、未中乙）：
- 水（壬、癸、子、亥、丑中癸、辰中癸、申中壬）：
- 火（丙、丁、巳、午、寅中丙、未中丁、戌中丁）：
- 土（戊、己、辰、戌、丑、未、寅中戊、申中戊、巳中戊）：

统计口径：天干1个 + 地支本气1个 + 中气1个 + 余气1个。不精确计算，只做大致统计。

强弱判断参考：
- 4次以上：明显偏旺
- 3次：偏旺
- 2次：中和
- 1次：偏弱
- 0次：缺失（需特别注意）

此统计仅辅助判断整体五行分布，不作为唯一依据。结合月令、十二长生、生克制化综合判断。

### 2. Season and Regulation

**读取文件：** `references/classical-texts.md` 第一节《穷通宝典》

Ask what the month branch does to the chart:

- Is the season cold, hot, dry, wet, or balanced?
- Is a regulating element needed before ordinary strength balancing?
- Is the regulating element present, rooted, protected, or damaged?

This is where 《穷通宝典》 and related regulation logic are useful. Do not reduce it to a lookup table; confirm the whole chart supports the need. **Cite the specific 穷通宝典 dictum that applies to this day master and month (e.g., "庚金生于六月，先用丁火...").**

**季节判断后必须给出调候得失评级：**

```
- 季节特征：寒/热/燥/湿/平和
- 是否需要调候：是/否
- 调候用神：
- 调候用神在局中的状态：有根/虚透/被克/缺失
- 【调候得失评级】：优/良/中/差 — 理由：...
```

**评级标准：**
- **优**：气候极端但调候用神恰在要位，根深气足，有力调候。如夏木逢水，冬火逢木。
- **良**：需要调候，调候用神有但力量不饱满（虚透、被轻微克制、或位置稍偏）。
- **中**：气候稍偏，调候需求不急；或调候用神有但力弱，仅能部分缓解。
- **差**：气候极端而调候用神缺失、被严重克制、或入墓空亡，无法发挥作用。

### 3. Day-Master Strength

Judge strength by evidence, not by one sign:

- Command: does the day master receive seasonal support?
- Roots: does it have root in branches or hidden stems?
- Twelve growth stages (十二长生): check the day master's stage in year/month/day/hour branches. 长生/沐浴/冠带/临官/帝旺为有力状态；衰/病/死/墓/绝/胎/养为较弱状态。This supports but does not replace the overall strength judgment.
- Support: are resource/peer elements present and useful?
- Drain/control: are output, wealth, and officer-killing forces excessive?
- Flow: does the chart circulate, block, clash, or need a bridge?

Use labels carefully:

- Strong
- Weak
- Balanced but pressured
- False strong or false weak
- Follow-type possibility

Do not declare a follow structure unless ordinary support/control is truly absent or unusable.

### 4. Structure and Useful Gods

**读取文件：** `references/classical-texts.md` 第七节《子平真诠》

Only after season and strength:

- Identify likely structure from month command and exposed stems.
- Decide whether the structure is clean, mixed, rescued, or damaged.
- Name useful god, assistant god, favorable elements, and unfavorable elements.
- Explain what evidence would change the conclusion.
- **Cite the specific 子平真诠 rule that applies to this structure (e.g., "伤官佩印，随时可用，而夏木见水...").**

When rules conflict, use this priority:

1. Solar-term and chart-fact correctness.
2. Seasonal regulation.
3. Strength and flow.
4. Structure and useful-god integrity.
5. Luck-cycle activation.
6. Ten-god and palace symbolism.
7. Stars, special sayings, and single-line classical dicta.

**结构判断结论必须包含以下两项评级（初评，后续步骤可修正）：**

```
结构判断
- 季节/调候：
- 旺衰/气势：
- 十二长生状态（日主在各宫）：
- 格局/用神：
- 置信度：
- 【格局清纯度初评】：优/良/中/差 — 理由：...
- 【有情有力初评】：优/良/中/差 — 理由：...
- 【成格救应初评】：优/良/中/差 — 理由：...
```

**评级标准：**
- **格局清纯度**：月令所出之格是否单一明确？天干透出的十神与月令格局是否一致？有无混杂、有无破格之神？
- **有情有力**：用神与相神配合是否得当（有情）？是否根深气足（有力）？《子平真诠》："何格无贵？何格无贱？亦在有情、有力无力之间而已。"
- **成格救应**：是否满足成格条件？若败格，是否有救应？《子平真诠》："成中有败，必是带忌；败中有成，全凭救应。"

### 4.5 清澈与浑浊分析（格局纯度）

在确定了格局和用神之后，必须评估格局的"清澈度"。这是《子平真诠》的核心判断：一个命局贵不贵，先看格局纯不纯。

**清澈的标志（满足越多越清）：**

1. **格局单一**：月令所出之格明确，天干透出的十神与月令格局一致。如月令正印、天干透印，为清；月令伤官、天干透财，为格局混杂，为浊。
2. **用神不杂**：有用神，有相神，各司其职。无多余的"第三者"捣乱。如伤官格用印制伤，不要再有财来坏印。
3. **无破格之神**：财不坏印、食不制杀、劫不夺财、枭不夺食。各元素之间不互相拆台。
4. **方向一致**：所有力量的流向是一致的——要么都生日主，要么都泄日主，要么都克日主。不能一边生一边泄一边克，各打各的。
5. **藏干不打架**：地支藏干之间没有严重的刑冲害破。如子午冲、卯酉冲在关键位置，会破坏格局的稳定性。

**浑浊的标志（满足越多越浊）：**

1. **格局混杂**：月令一个格局，天干透出另一个。如月令七杀，天干透正官，官杀混杂；月令食神，天干透伤官，食伤混杂。
2. **用神受伤**：用神被其他元素克制、合化、耗泄。如印为用神，被财破；官为用神，被食伤克。
3. **元素互战**：如金木交战、水火交战、火金交战，且没有通关元素（如水火交战缺木来通关）。
4. **多空亡或墓库不开**：关键元素入墓或被空亡，力量无法发挥。
5. **十神乱透**：天干同时透出多个对立十神，如正官+七杀+伤官+劫财，互相牵制，谁也没法主导。

**重要原则：不要各看各的。看"关系"而不是"元素"。**

例如：
- 表面看"金木水火土都有"是平衡，但如果金克木、木克土、土克水，各元素互战，就是浊。
- 表面看"只有两行"是偏枯，但如果两行相生有情（如木火通明），就是清而偏，仍然可成贵格。
- 判断清浊时，要同时看天干、地支、藏干、大运的**互动关系**，不是静态数个数。

**清澈度的结论格式（必须修正格局清纯度评级）：**

```
清澈度判断：
- 清澈/浑浊/半清半浊
- 关键清澈因素：
- 关键浑浊因素：
- 大运对清澈度的影响：
- 【格局清纯度修正】：优/良/中/差 — 基于清澈/浑浊分析修正后的评级
```

### 5. 流转分析（天干地支五行流转）

**读取文件：** `references/classical-texts.md` 第三节《滴天髓》

判断五行能量在天干和地支中是否顺畅流动。这是《滴天髓》的核心："气有余，宜顺其流；气不足，宜培其源。"

**流转分析必须分三层看，不要混在一起。Cite the specific 滴天髓 principle that explains the flow pattern observed (e.g., "旺极宜泄不宜克").**

---

**第一层：天干流转**

看四个天干之间的五行生克关系，画出"天干能量链"。

| 分析点 | 具体内容 |
|--------|----------|
| 起点 | 月令透干（月干）是起点，因为月令当令 |
| 流向 | 月干→年干→时干→日干，或月干→时干→日干，看实际生克关系 |
| 连续相生 | 如甲（月）→丙（年）→戊（日），木生火→火生土，链条顺畅 |
| 连续相克 | 如庚（月）→甲（年）→戊（日），金克木→木克土，链条阻断 |
| 日主位置 | 日主在链条中是否被生扶？还是被克泄？ |
| 通关 | 天干有两个冲突元素，有没有第三个元素通关？如金克木，中间有水，则金生水→水生木 |

**天干流转结论格式：**
```
天干流转：
- 链条：月干[X]→年干[Y]→时干[Z]→日干[W]
- 顺畅/阻塞：
- 日主被生/被克/被泄：
- 有无通关：
```

---

**第二层：地支流转**

看四个地支之间的五行生克关系，画出"地支能量链"。重点看地支的三合、六合、三会、冲、刑、害、破。

| 分析点 | 具体内容 |
|--------|----------|
| 起点 | 月令地支是起点，当令之气最旺 |
| 流向 | 月令→日支→时支→年支，按实际生克关系画 |
| 连续相生 | 如寅（月）→午（日）→戌（时），寅午戌三合火局，能量聚焦 |
| 连续相克 | 如子（月）→午（日）→酉（时），子午冲、午酉无直接关系，链条断裂 |
| 藏干互动 | 地支藏干之间有没有生克？如寅中甲→生→午中丁 |
| 合会 | 有没有三合、六合、三会？合会后的五行是什么？ |
| 冲刑 | 有没有冲、刑、害、破？冲刑是激活还是破坏？ |
| 通关 | 地支有两个冲突元素，有没有第三个地支通关？如子午冲，有寅木（木生火）或辰土（土克水）调和？ |

**地支流转结论格式：**
```
地支流转：
- 链条：月支[X]→日支[Y]→时支[Z]→年支[W]
- 合会：
- 冲刑：
- 顺畅/阻塞：
- 藏干互动：
- 有无通关：
```

---

**第三层：天地流转（天干与地支的连接）**

看天干和地支之间有没有"天地通气"——天干五行在地支中有没有根？地支五行在天干中有没有透？

| 分析点 | 具体内容 |
|--------|----------|
| 通根 | 每个天干在地支中有没有同类五行？如甲木天干，地支有没有寅卯？ |
| 透干 | 每个地支的五行在天干中有没有透出？如地支寅木，天干有没有甲乙？ |
| 天地呼应 | 天干和地支之间有没有相生关系？如天干甲木，地支有亥水（水生木） |
| 天地悖逆 | 天干和地支之间有没有相克关系？如天干庚金，地支有寅木（金克木但木耗金） |
| 虚实 | 天干有而地支无根 = 虚透；地支有而天干不透 = 暗藏；天干地支都有 = 实 |

**天地流转结论格式：**
```
天地流转：
- 通根情况：
- 透干情况：
- 天地呼应/悖逆：
- 虚实判断：
```

---

**三层结合看**

不要只看某一层。三层都顺畅才是真的好流转。

| 组合 | 含义 |
|------|------|
| 天干顺 + 地支顺 + 天地通 | 上格，能量内外一致，做事顺遂 |
| 天干顺 + 地支阻 | 表面顺但根基不稳，易有内耗 |
| 天干阻 + 地支顺 | 表面阻滞但内在有潜力，需等待时机 |
| 天干阻 + 地支阻 + 天地不通 | 下格，内外皆阻，需大运来救 |

**流转与格局的关系：**

- 清澈的格局 + 三层流畅 = 上格，贵气明显
- 清澈的格局 + 某层阻塞 = 有才华但施展不顺，或早年困顿、晚年通达
- 浑浊的格局 + 三层流畅 = 虽格局不纯，但人生顺遂，能以杂格取贵
- 浑浊的格局 + 三层阻塞 = 下格，人生多波折，需大运来救

**重要原则：流转分析不要脱离格局和用神单独做。流转是"手段"，格局是"目的"。**

例如：
- 正官格身弱，流转应该是"印（天干/地支）→身（日主）→官（正官）"。如果天干流转是"身→食伤→财→官"，这是身弱不任财官，天干流转再顺也是消耗——因为不符合格局需要。
- 伤官格身旺，流转应该是"身→食伤→财"。如果地支流转是"身→食伤→印"，这是伤官佩印，也是好格局，但方向完全不同——说明才华被约束而不是变现。

**流转分析的结论格式（必须包含流转顺畅度评级）：**

```
流转分析：

天干流转：
- 链条：
- 顺畅/阻塞：
- 有无通关：

地支流转：
- 链条：
- 合会/冲刑：
- 顺畅/阻塞：
- 有无通关：

天地流转：
- 通根：
- 透干：
- 虚实：

综合判断：
- 三层流畅度：
- 与格局的匹配度：
- 大运对流转载的影响：
- 【流转顺畅度评级】：优/良/中/差 — 理由：...
```

### 6. 格局综合评价（汇总，非独立打分）

> ⚠️ **重要：这不是一个独立的分析步骤。** 格局综合评价是对前面所有分析结果的汇总——每个维度的评级已经在前面的步骤中给出，此处只做汇总和对应到等级表。

**读取文件：** `references/rules/rules-ziping.md` 第八节"格局综合评价（等级体系）"；`references/classical-texts.md` 第八节《神峰通考》

**汇总操作：**
1. 收集前面步骤已给出的评级：
   - 格局清纯度：来自 Step 4.5 清澈浑浊分析（修正后）
   - 有情有力：来自 Step 4 结构判断
   - 成格救应：来自 Step 4 结构判断
   - 流转顺畅度：来自 Step 5 流转分析
   - 调候得失：来自 Step 2 季节调候
2. 对照等级表，确定综合等级
3. 用《神峰通考》"病药说"给出总结：指出命局之"病"与大运之"药"。

**输出格式（简洁，不重复分析）：**
```
格局综合评价：【等级】（上上/上中/上下/中上/中中/中下/下上/下中/下下）
- 五维汇总（前面已评）：
  - 格局清纯度：优/良/中/差（来源：清澈浑浊分析）
  - 有情有力：优/良/中/差（来源：结构判断）
  - 流转顺畅度：优/良/中/差（来源：流转分析）
  - 调候得失：优/良/中/差（来源：季节调候）
  - 成格救应：优/良/中/差（来源：结构判断）
- 一句话总结（用神峰通考病药说）：此格局之病在XX，大运之药在XX...
- 当前大运影响：提升/维持/拉低
```

**核心原则：**
- 综合评价中**不得出现新的分析内容**。所有判断依据必须在前面的步骤中已经论证过。
- 如果前面的步骤没有给出某维度的评级，综合评价时必须先回退补评，不能直接打分。

### 7. Luck and Timing

**读取文件：** `references/classical-texts.md` 第五节《千里命稿》；`references/dayun-rules.md`

Read dayun as environment and annual years as activation.

- Dayun stem may show surface theme; branch often carries deeper environmental force.
- Some schools split stem/branch into five years each; others read the pair for all ten years. State the convention if it matters.
- Annual year alone should not override original chart and dayun.
- A clash, combination, punishment, or harm needs a target. Explain what it activates.
- **Use 《千里命稿》 palace and ten-god logic to connect dayun to life domains (career, wealth, skill).**

### 7. Qianli-Style Event Calibration

Before final advice, propose 2-4 calibration points:

- Use age ranges, not overly exact dates, unless the chart gives very strong timing.
- Connect each point to chart evidence: palace, ten god, dayun, annual activation.
- Ask the user which points fit, partially fit, or miss.
- Revise useful-god or structure assumptions if feedback contradicts the first reading.

Good format:

```text
Calibration, medium confidence:
- Around age 18-20, study/location/family expectations may have shifted. This is inferred from ...
- Around age 28-30, career pressure or role change may have intensified because ...
```

Avoid:

- "You definitely had a disaster in year X."
- "Your marriage must fail."
- "This illness will happen."

### 6.5 神煞分析（吉神与凶煞）

根据用户需要，在排盘事实之后、结构判断之前，加入神煞查表。神煞传统上仅作辅助参考，不可越级使用，不可单断。

**分析原则：**
- 吉神与凶煞要"同宫同看"——不要只看吉神不看凶煞，也不要只看凶煞不看吉神。
- 吉神多则凶煞之力减，凶煞多而吉神少则压力增。
- 神煞与十神、宫位结合看，不要单独论断。例如：桃花在正官宫 vs 桃花在七杀宫，含义完全不同。
- 大运流年填实或冲动神煞时，神煞之力才明显。

**吉神部分（原局自带 vs 大运补）：**

| 贵人类型 | 原局出现 | 大运补入 | 宫位/影响 |
|----------|----------|----------|-----------|
| 天乙贵人 | | | |
| 太极贵人 | | | |
| 天德/月德 | | | |
| 文昌 | | | |
| 国印 | | | |
| 福星 | | | |
| 将星 | | | |
| 驿马 | | | |
| 华盖 | | | |
| 金舆 | | | |
| 学堂 | | | |
| 词馆 | | | |

**凶煞部分（原局自带 vs 大运引动）：**

| 凶煞类型 | 原局出现 | 大运引动 | 宫位/影响 |
|----------|----------|----------|-----------|
| 羊刃 | | | |
| 劫煞 | | | |
| 灾煞 | | | |
| 桃花 | | | |
| 红艳 | | | |
| 孤辰/寡宿 | | | |
| 亡神 | | | |
| 元辰 | | | |
| 空亡 | | | |
| 阴差阳错 | | | |
| 十恶大败 | | | |

**神煞综合判断：**
- 吉神集中度：
- 凶煞集中度：
- 吉凶平衡：
- 大运流年对神煞的填实/冲克：

### 7. Final Advice

Offer advice by domain only when requested or naturally relevant:

- Work and learning: roles, environments, decision style.
- Money: habits, risk posture, timing pressure.
- Relationships: communication patterns, timing sensitivity.

Keep advice practical and non-fatalistic.

## Output Template

Use this template when a full reading is requested:

```text
说明：以下按传统八字文化方法分析，供参考和自我观察，不作确定性预测。

排盘事实
- 四柱：
- 日主：
- 大运：
- 关键不确定性：

五行个数与强弱
- 金：
- 木：
- 水：
- 火：
- 土：
- 最旺五行：
- 最弱/缺失五行：

神煞分析
- 天乙贵人：
- 太极/天德/月德/文昌/国印/福星/将星/驿马/华盖/金舆/学堂/词馆：
- 羊刃/劫煞/灾煞/桃花/红艳/孤辰/寡宿/亡神/元辰/空亡/阴差阳错/十恶大败：
- 吉神集中度：
- 凶煞集中度：
- 原局自带 vs 大运补：

结构判断（含三维度初评）
- 季节/调候：
- 旺衰/气势：
- 十二长生状态（日主在各宫）：
- 格局/用神：
- 置信度：
- 【格局清纯度初评】：优/良/中/差 — ...
- 【有情有力初评】：优/良/中/差 — ...
- 【成格救应初评】：优/良/中/差 — ...

清澈与浑浊（修正清纯度）
- 清澈度：
- 关键清澈因素：
- 关键浑浊因素：
- 大运对清澈度的影响：
- 【格局清纯度修正】：优/良/中/差 — ...

流转分析（含顺畅度评级）
- 天干流转：
  - 链条：
  - 顺畅/阻塞：
  - 有无通关：
- 地支流转：
  - 链条：
  - 合会/冲刑：
  - 顺畅/阻塞：
  - 有无通关：
- 天地流转：
  - 通根：
  - 透干：
  - 虚实：
- 综合判断：
  - 三层流畅度：
  - 与格局匹配度：
  - 大运影响：
  - 【流转顺畅度评级】：优/良/中/差 — ...

格局综合评价（汇总，非独立分析）
- 等级：（上上/上中/上下/中上/中中/中下/下上/下中/下下）
- 五维汇总（前面各步骤已评）：
  - 格局清纯度：优/良/中/差（来源：清澈浑浊分析）
  - 有情有力：优/良/中/差（来源：结构判断）
  - 流转顺畅度：优/良/中/差（来源：流转分析）
  - 调候得失：优/良/中/差（来源：季节调候）
  - 成格救应：优/良/中/差（来源：结构判断）
- 一句话总结：
- 当前大运影响：提升/维持/拉低

大运与流年
- 当前大运：
- 近年主题：

历史校准
- ...

综合建议
- ...
```

For shorter user requests, answer only the relevant section.

## Anti-Patterns / 常见错误清单

以下是从实际分析中总结的高频错误，每次分析前必须自检：

### 1. 各看各的（元素孤立主义）

**错误表现：** 看到"金3个、木2个"就下结论，不看它们之间是相生还是相克；看到"有天乙贵人"就说有贵人，不看贵人被什么克制或合化。

**正确做法：** 永远看"关系"而不是"元素"。金3个如果是3个庚金天干，那是比肩夺财；如果是1个庚金+2个酉金，那是金局成势。同样是"3个金"，含义完全不同。

**自检问题：**
- 我有没有画出能量流向图？
- 我有没有检查每个元素被谁生、被谁克、合谁、冲谁？
- 我有没有把天干和地支、藏干一起考虑？

### 2. 一叶障目（只看月令主气）

**错误表现：** 月令未土，主气己土，就断"正印格"，完全忽略天干透出的伤官癸水。癸未月柱，伤官透干+印在地支，是伤官佩印，不是正印格。

**正确做法：** 月令主气是参考，但透干和藏干的组合才是真正的格局。看格局要看"月令+透干+藏干"的整体互动。

**自检问题：**
- 我有没有检查天干透出什么十神？
- 月令藏干的中气和余气有没有参与格局？
- 有没有出现"月令一个格局，天干透出另一个"的混杂情况？

### 3. 查表漏查（神煞不全）

**错误表现：** 查驿马只看日支，不看年支；查国印按年支查而不是日干查；查将星搞错三合局。

**正确做法：**
- 驿马：日支查一次，年支查一次，两个角度都要看
- 国印：严格按日干查地支，不是按年支
- 将星：按日支三合局的帝旺位查，不是按其他规则
- 所有神煞查完后，对照 `tables.md` 复核一遍

**自检问题：**
- 我是不是凭印象写的，而不是严格查表？
- 我有没有漏查年支角度的神煞？
- 我有没有把不同神煞的查法搞混（如国印 vs 福星 vs 金舆）？

### 4. 十二长生记错

**错误表现：** 庚在未月是冠带，记成衰；壬在卯月是死，记成病。

**正确做法：** 不要凭记忆，每次都查 `tables.md` 的十二长生表。阳干顺行、阴干逆行，必须严格对应。

**自检问题：**
- 我有没有查表确认日主在各宫的长生状态？
- 我有没有搞错阳干/阴干的顺逆方向？

### 5. 格局→用神→大运 连锁错误

**错误表现：** 格局判断错了（如伤官佩印错成正印格），导致用神错了（该用财却用印），导致大运分析全错。

**正确做法：** 格局判断是最关键的节点。如果格局不确定，宁可标"置信度：低"，也不要硬套一个格局。格局判断错了，后面所有分析都要重来。

**自检问题：**
- 我对格局判断的置信度是多少？
- 如果格局判断错了，后面的用神、大运、校准是否全错？
- 我有没有因为"格局不确定"而主动标出不确定性？

### 6. 清澈浑浊与流转分析的"各看各的"

**错误表现：** 清澈分析只看格局纯不纯，流转分析只看五行生不生，两者完全不结合。

**正确做法：** 清澈与流转必须结合格局和用神一起看。例如：
- 正官格身弱，流转应该是"印→身→官"（印生身，身任官）。如果流转是"身→食伤→财→官"，这是身弱不任财官，流转再顺也是消耗——这就是"清澈但流转方向错误"。
- 伤官格身旺，流转应该是"身→食伤→财"（才华变现）。如果流转是"身→食伤→印"（才华被印约束），这是伤官佩印，也是好格局，但方向完全不同——这就是"清澈但流转方向不同"。

**自检问题：**
- 我有没有把清澈分析、流转分析、格局判断三者孤立起来看？
- 流转的方向是否符合格局的需求？
- 如果流转阻塞，阻塞点是否正好在用神或格局的关键位置？

---

*错误清单更新日期：2026-06-21 | 基于实际分析错误总结*
