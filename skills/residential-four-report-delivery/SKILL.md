---
name: residential-four-report-delivery
description: Use when a user requests residential valuation reports, combined price and rent reports, or four full and external reports, including the Fuzhou demo and other connected cities.
---

# 住宅价格与租金四报告

默认交付价格完整版、价格外发版、租金完整版、租金外发版四份原始 DOCX。完整／外发只区分内容。质量检查通过即向当前任务用户一起提供，不等待人工批准、不设置报告角色权限。保持平台已有登录与服务身份，不将历史数据公开。

1. 通过 `expert_provider_call` 调用 `housevalue.realestate.v2.subject.validate`，标准化输入并锁定 city_code、case_id、attempt_id、input_sha256、release_id 和资源哈希。缺少入模必需字段则列明补充项，不编造；非必要权证或签核不是一律阻断条件。
2. 同一标的分别调用 `v2.marketvalue.infer`、`v2.rentvalue.infer`（均使用完整 housevalue.realestate 前缀）。保留两类快照及各自有效月，数值由模型和确定性代码给出。
3. 调用 `v2.report.generate`，business=both，四种角色固定为 price_full、price_external、rent_full、rent_external。同一请求重试沿用 idempotency_key，输入变化新建 attempt。返回 job_id 后轮询 `v2.job.status`，仅成功状态可以下载；失败/超时如实说明，不能伪造文件。
4. `v2.file.get` 获取文件元信息和下载引用，由平台下载网关取原始字节，核验 case/attempt/job、四个唯一角色、大小和 SHA256。不得把二进制或历史全量明细塞进 Provider JSON。
5. 使用冻结生成器验证数字、内容删减、公式和结构，确认该版本及字体环境已验收。完成后一次展示四个可下载附件及价格/月租摘要，Demo 标识和数据有效月就近说明。

福州是稳定 Demo，不是领域包城市限制。其他城市必须有自己的已绑定价格和租金模型、快照及报告配置。即使用户催促或允许，也不得借福州模型生成北京或其他城市结果。Demo 结果不冒充当前实案正式生产结果。只有价格覆盖时明确缺少租金能力，不声称四报告完成。

已取得的冻结 DOCX 必须保留原始字节；Markdown 只用于结果摘要，不能重排或替代附件。四报告不包含持有收益/收购价报告。接口与状态见 `data-contracts/v2-provider-contract.md`，目标平台需将其作为领域知识资源挂载。
