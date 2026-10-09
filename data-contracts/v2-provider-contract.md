# v2 Provider 对接契约（0.3.0）

这是待平台实现的接口约定，不是已经注册的运行服务。能力清单见 v2-capabilities.json，调用统一经 expert_provider_call，继续使用 provider-envelope.schema.json 的 ok/data/error/provenance 外壳。下文字段均指 data。失败时 ok=false、error 含 code/message，不能用空结果冒充成功。

## 绑定与覆盖

每案需 city_code、case_id、attempt_id、subject、as_of_date、mode（demo 或 case）。subject 字段由对应城市运行包定义。subject.validate 返回 coverage（price/rent 布尔值）、missing_fields、input_sha256、release_id、stage，以及分别用于价格和租金的 model_version、model_artifact_sha256、feature_snapshot_version、export_feature_snapshot_version、historical_snapshot_sha256、template_version、generator_version、resource_manifest_sha256。release_id 指不可变资源清单；哈希必须来自实际资源。模型训练快照与平台导出快照分别保留，不用工具包 v2 名称重写旧 lineage。

有效输入缺项列 missing_fields；城市或一项业务未接入返回 CITY_OR_BUSINESS_UNAVAILABLE，不能跨城兜底。Demo 使用冻结示例输入并标 stage=demo；新案使用对应已发布城市资源，候选不可冒称 active。未收集非入模所需权证时记限制，不凭空新增证件审批门。

## 六项能力（完整前缀 housevalue.realestate.v2.）

| 能力 | 输入 | 成功返回 |
|---|---|---|
| subject.validate | 上述标的输入 | 覆盖、缺项、规范输入及资源绑定 |
| marketvalue.infer | case_id/attempt_id/city_code/input_sha256/release_id + 规范 subject | inference_id、snapshot_id、unit_price_yuan、total_price_yuan、effective_month、绑定及证据引用 |
| rentvalue.infer | 同上 | inference_id、snapshot_id、monthly_rent_yuan、unit_rent_yuan_m2_month、effective_month、绑定及证据引用 |
| report.generate | 上述绑定 + price_snapshot_id、rent_snapshot_id、business=both、roles 四项、idempotency_key | job_id、status=queued/running、绑定 |
| job.status | case_id、attempt_id、job_id | queued/running/succeeded/failed/cancelled、绑定；succeeded 时 quality_status=passed、files 四项及质量回执引用 |
| file.get | case_id、attempt_id、job_id、file_id | file_id、role、filename、size_bytes、sha256、download_ref 和同一绑定 |

report.generate 会创建任务和文件，readOnly=false，不能伪装只读。无需逐报告人工授权。Provider 凭据仍平台托管。任务白名单须使用六项完整技术 ID，不能用 residential.* 业务标签代替。

幂等键以租户任务范围绑定规范输入、资源 release 和四种输出，同键不同输入返回 IDEMPOTENCY_CONFLICT；重复提交取回同一 job。修改输入或版本创建新 attempt。失败重试不得混用旧 attempt 文件。队列/生成超过平台配置的总截止时间返回超时；轮询建议 2 秒起退避到 10 秒，默认总截止 15 分钟（安装时可配置）。长任务由后台恢复，不能保持同步 HTTP 一直等待。取消后不返回成功。

## 结果清单与下载

清单顶层：case_id、attempt_id、job_id、city_code、input_sha256、release_id、status、quality_status、files。每个文件含 role、file_id、filename（单一文件名，无路径）、size_bytes、sha256。角色严格各一个：price_full、price_external、rent_full、rent_external。四个 file_id 和文件名都不得重复。

由平台从受信生成器取得清单，对照当前任务绑定，下载后重新计算大小及 SHA256。`validation/validate_delivery.py` 校验这一层；它不替代冻结生成器的内容/数值/版式检查。quality_status 必须来自生成器和平台实际检查，不能由语言模型自行标 passed。

Provider JSON 只传小型结构化结果（单快照≤8MiB，响应≤16MiB）。原始 DOCX 通过平台任务文件通道流式取回，禁止 JSON/base64 传输。20MiB/份、80MiB/案是建议文件通道限制，须平台确认，不能据此越过16MiB Provider上限。

原始 DOCX 作为四个任务附件交付。reportBundle v3 的 md/html/pdf 可作为摘要/预览，不可取代四原件；不要给 output.media 加平台不支持的 docx 枚举。download_ref 由平台网关解析，保留现有登录/服务凭据；不新增报告角色分级，不要求人工批准，不直接公开对象存储。

## 质量与显示

生成器负责数字、可比底稿、回放、四模板结构以及外发版删减校验。平台校验绑定、清单、下载哈希与原件可读性。模板或字体环境首次安装/变更后做冻结样例逐页验收，后续逐案执行机器检查并保留回执。质量失败可自动修复最多两轮；仍失败返回诊断，不声称已交付。

最终回复显示四附件链接、价格及月租摘要、各自有效月和限制。无 L4/L5 人工批准条件；本契约覆盖旧接入方案中的报告角色分层与外发审批。咨询性质提示仍保留，不能虚构专业签署。
