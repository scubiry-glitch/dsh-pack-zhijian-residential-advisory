---
name: residential-rent-reference
description: '住宅租金参考测算工艺。用于租赁可比查询、正式租金模型、同小区租金、单位租金、合理性和归因解释；挂牌、成交和模型来源不清时不得合并表述。Triggers on "月租金", "单位租金", "出租定价", "住宅租金参考".'
version: 0.2.0
user-invocable: true
argument-hint: "[测算/复核] 单套住宅租赁资料"
license: 机构内部
metadata:
  short-description: 住宅租金参考测算
---

# 住宅租金参考测算

> 本文件是分发副本。安装或会话挂载后的运行时权威文件为 `knowledge/skills/residential-rent-reference/SKILL.md`。

## §0 模板引用（先读）

执行前完整阅读 `references/rent-workflow.md`。

## §1 行文逻辑（怎么写）

先陈述结构化月租金和单位租金，再组织租赁可比、同小区对照、模型合理性、归因和限制条件。

## §2 数据要求（怎么用数）

只解释结构化响应已有数值。挂牌租金、租赁成交和模型预测必须标注来源类型；不得将挂牌静默改写为成交，不得自行换算缺失数字。

## §3 质量门禁（怎么过关）

核验城市覆盖、单位、周期、标的一致性、数据版本、模型版本和技术引用。证据不足时保留警告或阻断，不用其他城市结果补缺。
