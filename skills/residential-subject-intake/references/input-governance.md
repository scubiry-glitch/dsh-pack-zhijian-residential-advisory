# 标的资料治理清单

## 输入状态

- `verified_fact`：具有结构化来源且已核验；
- `user_input`：用户明确提供但尚未外部核验；
- `structured_fill_pending_confirmation`：接口回填、等待确认；
- `assumption`：用户确认并明确用于情景测算；
- `missing`：缺失或无法核验。

## 执行顺序

1. 标准化城市、区县、小区、楼栋、单元和房号；
2. 调用地址解析能力并保存候选、置信状态和查询引用；
3. 核验城市与住宅类型覆盖；
4. 按业务场景检查必要字段；
5. 输出 `covered`、`needs_confirmation`、`data_insufficient` 或 `not_covered`。

Provider 失败时返回 `provider_unavailable`，不得猜测地址或生成替代数值。
