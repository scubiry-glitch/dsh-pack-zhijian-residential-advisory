---
name: residential-hold-return-acquisition
description: '单套住宅持有收益与收购价测算工艺。用于经营参数核验、NOI、收益率、DCF、IRR、收购价参考线和敏感性情景解释；缺少确定性计算快照时阻断数值结论。Triggers on "持有收益", "NOI", "IRR", "DCF", "收购价", "敏感性".'
version: 0.3.0
user-invocable: true
argument-hint: "[测算/复核] 价值快照、租金快照和经营参数"
license: 机构内部
metadata:
  short-description: 持有收益与收购价测算
---

# 持有收益与收购价测算

> 本文件是分发副本。安装或会话挂载后的运行时权威文件为 `knowledge/skills/residential-hold-return-acquisition/SKILL.md`。

## §0 模板引用（先读）

执行前完整阅读 `references/deterministic-calculation-boundary.md`。

## §1 行文逻辑（怎么写）

先列市场价值快照、租金快照、经营参数和情景，再解释确定性代码返回的 NOI、收益率、DCF、IRR、收购价参考线和敏感性结果。

## §2 数据要求（怎么用数）

AI 不得自行计算、补算或改写任何数值。计算输入只来自结构化快照，不得从渲染报告正文提取。参数必须保留来源、单位、基准日和确认状态。

## §3 质量门禁（怎么过关）

缺少有效价值快照、租金快照、关键经营参数或 `calculation_snapshot_id` 时阻断数值结论。Agent 只解释已经生成的确定性结果，不作投资审批或融资承诺。
