# 智见住宅估值与租金四报告领域包

版本 **0.3.0**。住宅估值默认生成价格完整版、价格外发版、租金完整版、租金外发版四份 DOCX；质量检查通过后一次直接给出全部文件，不设置报告角色分层或人工批准环节。

面向已接入的城市。福州提供冻结运行包及历史数据快照，作为稳定 Demo；其他城市绑定各自模型、快照与报告配置。没有城市覆盖时说明缺少的资源，不能套用福州模型。

## 使用入口

“住宅估值”“估值和租金报告”“四份报告”“福州估值”进入 `single-home-four-reports`。组合请求优先于单业务关键词；明确只要价格/租金时仍可使用原两个场景。持有收益/收购价保留独立场景，不计入四报告。

冻结生成器输出原始文件；Markdown 仅是简短摘要，不重排 DOCX。完整／外发是内容版本：外发版删减底稿等细节，四份均返回当前任务用户。数值来自模型和确定性代码，附数据有效月与咨询性质，不虚构专业签署。

## 安装与状态

本包为 `candidate_for_zhijian_deployment`，含领域编排、能力契约、Skill、质量规则和本地校验工具。**更新 Git 不等于六项新能力已经在智见注册，也不包含私有运行程序与历史数据。**

- [智见接入步骤与反馈处理](docs/INTEGRATION.md)
- [六项 Provider 契约](data-contracts/v2-provider-contract.md)
- [能力与直接交付策略](data-contracts/v2-capabilities.json)
- [福州私有 Demo 运行包校验引用](demo/fuzhou-runtime-reference.json)
- [提交验收清单](SUBMISSION-CHECKLIST.md)

领域包安装到 `domain-packs/zhijian-residential-advisory`。`skills/` 分发文件及 references 一起挂载到 `knowledge/skills/`，登记 skill-catalog；领域知识和 data-contracts 也须可检索。平台凭据、模型、历史逐笔数据不进入公共 Git。训练保留本地。

## 本地验证

无需项目仓库之外的测试脚本，Python 3.11+：

```sh
python3 -m unittest discover -s validation/tests -v
python3 validation/check_pack.py
```

修改后重建完整性清单：`python3 validation/check_pack.py --build`，再执行上述只读验证。四报告下载完整性校验：`python3 validation/validate_delivery.py manifest.json expected-current-task.json downloaded-files/`。清单校验不代替真实 DOCX 内容、数值或渲染验收。
