---
type: template
created: 2026-05-14
updated: 2026-09-05
status: active
aliases: ["TPL-Codex项目桥接卡", "项目桥接卡模板", "Project Bridge Card Template"]
---

# TPL｜项目桥接卡

复制下列字段和章节建立卡片。规则见 `00-AI/governance/write-back-rules.md`；本卡保存当前摘要，逐项替换，不按日期追加。无状态、决策、边界、证据或下一步变化时不写。

```yaml
---
type: project-bridge
record_format: compact-v1
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active # active / waiting / paused / blocked / done / archived
project:
pillar: general
project_entry: true
priority: p1 # p0 / p1 / p2 / p3
stage: discovery
local_root:
kb_project:
startup_files: []
kb_bridge_status: kb-only # kb-only / project-linked / paused
last_verified: # 实际核验后填写；创建或改写文档不等于核验
next_action: # 必须与正文“首要动作”一致，只是该动作的字段镜像
next_review:
---
```

# 项目桥接卡｜<项目名>

## 一句话定位

<项目做什么，为什么需要 AI 接手。>

## 开工入口

- 本地项目：`<local_root>`；规则：`<local_root>/AGENTS.md`（如存在）。
- 知识库项目页：<项目页链接>。
- 事实来源：<当前状态文档>、<决策文档>；与摘要矛盾时先复核事实源。
- 当前任务需要的其它入口：<至多列必要文件，不复制文档目录>。

## 当前状态

- <最多 5 点；只写当前结果、限制及核验来源，不累计每次进度。>

## 有效决策

- <最多 5 点；只保留仍约束行动的决策及原因，细节链接到决策文档。>

## 下一步

- 首要动作：<一个可执行动作，与 next_action 完全一致>
- 必要依赖：<最多 2 项；没有则删除此行>

## 阻塞与操作边界

- <未解决阻塞、授权范围及禁止动作；没有则写“无”。不得为压缩删除这些信息。>

## 证据与经验入口

- <影响接手的关键验证结论及可定位证据；完整测试输出留在项目记录。>
- <已沉淀经验链接；有复用经验写入 `20-SharedAssets/01-user-assets/`，不要写进 managed `02-modules/`。没有则删除。>

## 维护约定

- 正文不超过 3000 个 Unicode 字符且不超过 120 个非空行，移除文件开头 YAML frontmatter 后计量；不是字数或 Token。
- 超限先把详细过程保存在既有项目日志、验收文档或可追溯历史，再在本卡引用；不得丢失未解决阻塞、操作授权边界或关键证据。仍不可压缩时，写明例外原因和复核条件。
- 只替换当前段落；已失效内容保存在可追溯历史后移出摘要。正文只设一个“下一步”，不另加“下次开工”“当前下一步”或逐次“验证记录”。
- 重要实现 / 验收写入项目 docs 或 PR；只有确实需要其它窗口或 Agent 接手时才写交接卡。
- 更新后执行只读检查：`python3 00-AI/scripts/kb.py check-record <本卡路径>`。
