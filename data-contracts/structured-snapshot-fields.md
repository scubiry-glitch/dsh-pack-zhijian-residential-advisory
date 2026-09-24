# 结构化测算快照字段约定

报告和下游 Agent 只消费结构化快照，不从渲染报告反向取数。

## 通用字段

- `snapshot_schema_version`、`snapshot_id`、`scenario_id`；
- 标的资料、测算基准日和字段核验状态；
- `query_id`、`data_version`；
- `model_version`、`inference_id`；
- `calculation_snapshot_id`、`rule_version`；
- 结果、可比摘要、合理性、归因、警告和限制条件；
- `generated_internal_review_draft`、`ready_for_human_review`、`approved_for_external_delivery` 或 `blocked`。

Agent 只能写入前两种非外发状态。`approved_for_external_delivery` 只能由授权人工流程写入。

## 数值来源

市场价值和租金数值来自已发布模型或结构化可比响应；NOI、收益率、DCF、IRR、收购价和敏感性结果来自确定性计算快照。语言模型只解释，不计算或改写。
