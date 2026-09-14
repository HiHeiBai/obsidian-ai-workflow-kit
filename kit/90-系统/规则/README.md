---
type: governance-index
status: active
---

# Agent Governance

按正在发生的操作读取对应规则；本页是导航，不是每次开工的必读清单。

| 文件 | 作用 |
|---|---|
| `startup-contract.md` | 明确目标与授权，按缺口加载上下文 |
| `write-back-rules.md` | 决定写回位置，维护桥接与交接摘要 |
| `review-gates.md` | 控制改动范围、去重与验证长期写入 |
| `maintenance-loop.md` | 维护知识库健康 |

外部资料的分析、私人收藏和知识提炼见 `20-资料/处理流程/资料转知识流程.md`。只有项目状态变化或确实需要接手时，才更新相应入口。

共享规则在公开源码维护一次，经受管同步导入。本地扩展只记录路径、字段、工具约束和用户偏好等差异，并引用共享规则；不复制其正文。

## English

Read the rule for the operation being performed; this index is not a mandatory startup checklist.

| File | Use |
|---|---|
| `startup-contract.md` | Establish the goal and authorization; load context as needed |
| `write-back-rules.md` | Route durable changes and maintain bridge or handoff summaries |
| `review-gates.md` | Control scope, deduplicate, and validate durable changes |
| `maintenance-loop.md` | Maintain vault health |

Use `20-资料/处理流程/资料转知识流程.md` for analysis, private collection, and knowledge promotion. Update an entry point when project state changes or an actual handoff is needed.

Maintain shared rules once in public source and import them through managed sync. Local extensions reference shared rules and record only differences such as paths, fields, tool constraints, and user preferences.
