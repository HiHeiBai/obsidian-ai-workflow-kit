---
type: example
status: active
---

# AI 接手演示

## 场景

用户只给 AI 一句话：

```text
你是知识库维护 Agent，请阅读当前 vault 的 00-AI/START-HERE.md，并按里面的开工流程执行。
```

## AI 应该读到

1. `00-AI/START-HERE.md`
2. `index.md`
3. `10-Projects/01-example-project/BRIDGE-example.md`
4. `10-Projects/01-example-project/current-state.md`

## AI 应该输出

- 当前任务类型。
- 已读取的入口。
- 建议下一步。
- 结果写回位置。

## 结束写回

项目事实变化时，先更新项目事实文档，再替换桥接卡当前摘要。无变化不写。只有确实需要另一个窗口或 Agent 接手时，才在 `01-Inbox/agent-handoffs/` 写临时交接卡。

完整过程见 [任务接手与经验复用示例](walkthrough.md)（含中文和 English）。
