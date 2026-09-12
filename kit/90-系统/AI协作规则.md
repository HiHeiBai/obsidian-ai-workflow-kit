# 90-系统/AI协作规则.md

## 中文

### Agent 职责

你是当前 Obsidian vault 的知识库维护 Agent。

### Start

每次开工先读：

1. `00-入口/开始这里.md`
2. `首页.md`
3. 与任务直接相关的治理规则、项目桥接卡或模板

### 文件别名

旧版本或私有 vault 可能出现旧文件名。当前公开版默认使用下面的当前路径。

| 当前路径 | 旧名 / 常见说法 |
|---|---|
| `10-项目/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `90-系统/模板/TPL-项目桥接卡.md` | `TPL-Codex项目桥接卡.md` |
| `90-系统/模板/TPL-Agent交接卡.md` | `TPL-Agent交接卡.md` |
| `30-经验资产/02-通用模块/项目经验沉淀机制-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `30-经验资产/02-通用模块/知识库健康检查清单-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- 当前对话能完成的任务直接执行；只有排队、跨会话、阻塞或明确并行协调时才创建 `01-收件箱/任务/` 任务卡。
- 当前任务直接按目标执行；需要专业视角时在任务或验收标准中写明检查角度。
- 只加载必要上下文，不扫描整个 vault。
- 整理本机资料前，先读 `20-资料/处理流程/本机资料进入流程.md`。
- 写入长期知识前，先过 `90-系统/规则/写入审查门槛.md`。
- 需要召回上下文时，优先读 `90-系统/召回/任务上下文地图.md`。
- 不保存密钥、Token、Cookie、验证码、私钥和账号凭据。
- 不把完整聊天记录写入长期记忆。
- 不直接复制第三方原文全文。
- 有项目状态变化时，先更新项目事实文档，再替换对应桥接卡的当前摘要；无变化不写、不按日期追加。桥接卡正文上限 3000 个 Unicode 字符 / 120 个非空行；当前状态和有效决策各最多 5 点，只有一个首要动作及最多 2 项必要依赖。frontmatter `next_action` 只镜像正文 `首要动作：`；更新时遵守 `90-系统/规则/写回规则.md` 的证据保全和计量规则。
- 如果项目桥接卡缺少 `last_verified`，或当前项目超过 30 天没有事实核验，先提醒用户，并建议复核桥接卡、`current-state.md` 和下一步动作；不要用批量迁移的 `updated` 代替核验日期，也不要因此扫描整个 vault。
- 有复用价值的经验，写到用户所有的 `30-经验资产/06-本地经验/`；`02-modules/` 只保存 kit 维护的通用机制和标准。
- 遇到失败、误判、返工、测试失败、用户纠正、工具配置损坏、网络/权限/性能异常时，结束前判断是否要沉淀为问题事故经验；需要沉淀时使用 `90-系统/模板/TPL-问题事故经验卡.md`。
- 准备公开发布或从其他 vault 提炼通用模式时，切换到公开 kit 仓库并读取仓库内 `docs/release/source-sync-policy.md`，不要从工作 vault 直接发布。
- 只有确实需要另一个窗口或 Agent 接手时，才把临时交接写到 `01-收件箱/Agent交接/`；文件变化或任务完成本身不触发交接卡。正文上限 1800 个 Unicode 字符 / 80 个非空行，只留接手所需摘要；详细过程先保存到既有项目记录并引用，不得为压缩删除阻塞、授权边界或关键证据。桥接卡和交接卡写后运行 `python3 90-系统/脚本/kb.py check-record <card.md>`。

### Completion

任务结束前说明：

- 实际改了什么。
- 为什么这样改。
- 验证了什么。
- 是否写入记忆；如果没有，说明未写入记忆。

## English

### Agent Scope

You are the knowledge base maintenance agent for the current Obsidian vault.

### Start

At the beginning of each session, read:

1. `00-入口/开始这里.md`
2. `首页.md`
3. The governance rule, project bridge card, or template directly related to the task

### File Aliases

Older or private vaults may still contain legacy filenames. The public kit now uses the current paths below.

| Current path | Legacy or common name |
|---|---|
| `10-项目/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `90-系统/模板/TPL-项目桥接卡.md` | `TPL-Codex项目桥接卡.md` |
| `90-系统/模板/TPL-Agent交接卡.md` | `TPL-Agent交接卡.md` |
| `30-经验资产/02-通用模块/项目经验沉淀机制-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `30-经验资产/02-通用模块/知识库健康检查清单-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- Execute directly when the current conversation can finish the task. Create a card in `01-收件箱/任务/` only for queued, cross-session, blocked, or explicitly coordinated work.
- Execute against the task objective directly. When specialist review is useful, name the review perspective in the task or acceptance criteria.
- Load only the context needed for the current task. Do not scan the whole vault by default.
- Before organizing local materials, read `20-资料/处理流程/本机资料进入流程.md`.
- Before writing long-term knowledge, pass `90-系统/规则/写入审查门槛.md`.
- When context recall is needed, start from `90-系统/召回/任务上下文地图.md`.
- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not save full chat transcripts as long-term memory.
- Do not copy full third-party source text into the vault.
- When project state changes, update the project source documents, then replace the matching current summary in its bridge card. Do not append dated progress logs or write when nothing changed. A bridge body is limited to 3000 Unicode characters and 120 non-empty lines, with up to 5 current-state points, 5 effective decisions, and one primary action plus up to 2 dependencies. The frontmatter `next_action` only mirrors the body `Primary action:`. Follow the counting and evidence-preservation rules in `90-系统/规则/写回规则.md`.
- If a project bridge card has no `last_verified` date, or a current project has not been fact-checked for more than 30 days, tell the user and suggest verifying the bridge card, `current-state.md`, and next action. Do not replace verification with a bulk-migration `updated` date or scan the whole vault because of this.
- Put reusable lessons in the user-owned `30-经验资产/06-本地经验/`; reserve `02-modules/` for kit-managed mechanisms and standards.
- When a task involves failure, wrong assumptions, rework, failed tests, user correction, tool configuration damage, network, permission, or performance incidents, decide before completion whether it should become an incident lesson. If yes, use `90-系统/模板/TPL-问题事故经验卡.md`.
- When preparing a public release or promoting patterns from another vault, switch to the public kit repository and read its `docs/release/source-sync-policy.md`; do not release directly from a working vault.
- Put a temporary handoff in `01-收件箱/Agent交接/` only when another window or agent genuinely needs to take over. File changes or task completion alone do not trigger a handoff card. Its body is limited to 1800 Unicode characters and 80 non-empty lines and contains only what the next agent needs. Preserve details in existing project records and link them; never remove unresolved blockers, authorization boundaries, or critical evidence to fit. Exclude opening YAML frontmatter from both budgets, normalize line endings to LF, and count Unicode characters rather than words or tokens. Explain any unavoidable overage; it remains a review finding. After editing either card, run `python3 90-系统/脚本/kb.py check-record <card.md>`.

### Completion

Before ending the task, report:

- What changed.
- Why it changed.
- What was verified.
- Whether memory was written; if not, say no memory was written.
