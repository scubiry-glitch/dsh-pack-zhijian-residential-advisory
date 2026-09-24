---
name: residential-advisory-report-quality
description: '住宅估值咨询报告组织与门禁工艺。用于市场价值、租金、持有收益与收购价咨询报告的数字一致性、来源、版本、措辞、限制条件和 DOCX 渲染复核。Triggers on "生成咨询报告", "报告复核", "质量门禁", "DOCX 交付".'
version: 0.2.0
user-invocable: true
argument-hint: "[生成/复核] 结构化测算快照"
license: 机构内部
metadata:
  short-description: 住宅估值咨询报告质量门禁
---

# 住宅估值咨询报告质量门禁

> 本文件是分发副本。安装或会话挂载后的运行时权威文件为 `knowledge/skills/residential-advisory-report-quality/SKILL.md`。

## §0 模板引用（先读）

执行前完整阅读 `references/report-gates.md`。

## §1 行文逻辑（怎么写）

从结构化快照生成报告：结果先行，随后呈现证据、合理性与归因，最后披露技术引用和限制条件。

## §2 数据要求（怎么用数）

润色不得修改数字、日期、条件、程度词或限制性声明。允许结果名称包括市场价值参考测算、咨询测算结果、建议区间和情景参考线。

## §3 质量门禁（怎么过关）

依次执行内容、计算、视觉和合规检查，并完成 DOCX 逐页渲染复核。Agent 只能形成内部草稿或待人工复核状态，对外交付必须由授权人工批准。
