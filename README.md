# 智见住宅咨询测算 Agent 包

本包把房屋价值平台已核验的业务能力组织为三个面向用户的基础 Agent：单套住宅市场价值参考测算、住宅租金参考测算、持有收益与收购价测算。可比案例分析、同小区对比、价格合理性、归因解释和报告生成被纳入相应场景流程，不另设面向用户的 Agent。

## 当前状态

- 包版本：`0.2.0`
- 提交状态：`candidate_for_zhijian_deployment`
- 本地范围：静态结构、引用关系、合规边界及可复现打包可验证
- 平台范围：Provider、Skill 和 Scenario 尚未注册，不能据此声明生产可用
- 发布约束：完成智见平台验收、灰度、GATE 文件、匿名化样本和审批后，方可按正式状态管理

## 目录映射

- 交付源目录：`deliverables/zhijian-residential-advisory`
- 目标平台领域包：`domain-packs/zhijian-residential-advisory`
- Skill 分发副本：`skills/<skill-id>/SKILL.md`
- 目标平台运行时权威入口：`knowledge/skills/<skill-id>/SKILL.md`
- 专家知识说明：`knowledge/experts/<expert-id>/PROFILE-SOURCES.md`

分发包中的 Skill 是提交副本；注册后应以目标平台 `knowledge/skills/` 下的内容为运行时权威版本。能力映射不代表 Provider 已在目标环境注册。

## 三个用户场景

1. `single-home-market-value-reference`：市场价值参考测算、出售可比分析、同小区对比、合理性与归因解释。
2. `single-home-rent-reference`：租金参考测算、租赁可比分析、同小区对比、合理性与归因解释。
3. `single-home-hold-return-acquisition`：基于已验证价值、租金和确定性计算快照，解释持有收益及收购价情景参考线。

## 使用边界

本包生成咨询成果，不自动生成法定或制度要求的资产评估报告、房地产估价报告。AI 不自行计算估值、租金、NOI、DCF、IRR 或敏感性结果；所有数值均须来自结构化数据、确定性代码或已绑定的模型推理结果。

## 本地校验

从项目根目录执行：

```bash
PYTHONPATH=. python -m pytest tests/agent_packs/test_zhijian_residential_advisory_pack.py -q
python scripts/validate_zhijian_residential_advisory_pack.py
```

本地校验通过仅表明候选包满足仓库内的静态约束，不等于目标平台验收完成，也不构成生产可用声明。

