---
name: residential-market-value-reference
description: '单套住宅市场价值参考测算工艺。用于交易可比查询、正式模型推理、同小区对比、预测合理性、价格归因和咨询报告证据组织；城市未覆盖、正式版本缺失或要求法定评估结论时不得生成正式结果。Triggers on "二手房价值", "成交价参考", "市场价值参考", "同小区价格对比".'
version: 0.3.0
user-invocable: true
argument-hint: "[测算/复核] 单套住宅资料"
license: 机构内部
metadata:
  short-description: 单套住宅市场价值参考测算
---

# 单套住宅市场价值参考测算

> 本文件是分发副本。安装或会话挂载后的运行时权威文件为 `knowledge/skills/residential-market-value-reference/SKILL.md`。

## §0 模板引用（先读）

执行前完整阅读 `references/market-value-workflow.md`。

## §1 行文逻辑（怎么写）

先陈述结构化测算结果，再组织交易可比、同小区对照、预测合理性、价格归因和限制条件。

## §2 数据要求（怎么用数）

只解释 Provider 响应和结构化快照已有事实与数值。模型预测、可比原始值和调整值分层保留；不得编造可比案例，不得用全局重要度冒充单套本地归因。

## §3 质量门禁（怎么过关）

城市、标的、数据版本、模型版本和技术引用通过硬门后，才生成结构化市场价值参考快照。报告金额只能称为市场价值参考测算、咨询测算结果或建议区间。
