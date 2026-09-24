# 市场价值参考测算工作流

1. 读取标的资料核验结果；
2. 并行调用交易可比查询和已发布市场价值模型；
3. 保留候选案例、入选案例、排除案例、原始值和调整值；
4. 形成同小区、同板块和其他候选样本的分层对照；
5. 对照模型预测与调整后可比基准，解释差异方向；
6. 仅在服务返回本地或逐样本归因时解释贡献；
7. 保存 `query_id`、`data_version`、`model_version`、`inference_id` 和 Schema 版本。

`not_covered`、`candidate_release_only`、`subject_consistency_mismatch`、`provenance_incomplete` 均阻断正式结果。Provider 不可用时不生成替代数字。
