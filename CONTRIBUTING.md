# 参与贡献

感谢你愿意改进 `zhizhi-bazi-skill`。

## 适合贡献的方向

- 更可靠的排盘测试。
- 更精确的节气历算支持。
- 可靠的农历转阳历能力。
- 能转化为明确判断规则的经典资料摘要。
- 更安全、更自然的中文表达。
- 提示词样例和评测案例。

## 写作风格

- 保持 `SKILL.md` 简洁。
- 详细推理放到 `references/`。
- 确定性计算放到 `scripts/`。
- 不要堆放大段古籍原文，除非已经转化成可执行的判断规则。
- 不要写宿命化、恐吓式、医疗保证、投资保证或婚育保证式断语。

## 校验

运行：

```
python scripts/calc_bazi.py --self-test
python scripts/calc_bazi.py --date 1990-05-15 --time 08:30 --sex 男 --json
```

如果本机有技能校验脚本，也运行：

```
python <skill-creator路径>/scripts/quick_validate.py .
```
