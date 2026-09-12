# Obsidian AI Workflow Kit

中文 | [English](README.md)

[![CI](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/actions/workflows/ci.yml)

让你的本地 Obsidian vault 变成 AI 能读取、写回和维护的知识库。

你打开一个新的 Claude Code、Cursor、Codex 或 ChatGPT 会话。它又问你：这个项目是什么？关键资料在哪？上次做到哪？哪些内容不能乱改？

这套 kit 解决的就是这个接手问题：用一个本地优先的 Obsidian 结构，提供唯一开工入口、项目桥接卡、写回规则、资料分流、召回地图和维护检查。

它不是 App、社区插件、云端记忆服务，也不是 RAG 系统。它是一套文件系统层的工作流：人能直接改，任何能读取本地文件的 AI Agent 都能执行。可选动态工作台使用 Obsidian 自带的 Bases 核心插件。

它不让 AI 全库乱搜，而是用任务路由和召回字段，让 AI 先读最该读的少数文件。

## 快速开始

### 新建或安装到已有 vault

先把最小层安装到空目录或已有 vault，再用 Obsidian 打开**安装目标文件夹**，点击 `首页.md`。GitHub 仓库保存开发源码；安装器从中生成日常使用的知识库目录。

安装器默认写入 English 路径和启动文本。中文用户请加 `--language zh-CN`，安装后的核心目录也会使用中文路径。

先预览：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --dry-run "/path/to/your-vault"
```

确认后安装：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN "/path/to/your-vault"
```

检查：

```bash
python3 "/path/to/your-vault/90-系统/脚本/kb.py" health-check --vault "/path/to/your-vault" --mode barebone
```

然后把这句话发给你的 AI Agent：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<your-vault-path>。请先读取该目录下的 00-入口/开始这里.md，并按里面的开工流程执行。
```

如果你想安装完整 starter vault，包括资料流水线、召回系统、文档、示例和模板，可以使用进阶的 full 模式：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --mode full "/path/to/your-vault"
```

安装器默认跳过已有文件；只有你明确传入 `--overwrite` 才会覆盖。

后续更新：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --update --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --update "/path/to/your-vault"
```

更新时会读取本地 manifest，只替换仍然保持原样的 kit 文件，不静默覆盖你改过的内容。

`v0.9.1` 下载包仅保留为历史快照。从 `v0.10.0` 起，后续维护只使用仓库源码和 managed installer，不再构建定制客户 ZIP 包。

### 让长期使用的本地主库保持同步

如果 Vault 已有自己的入口、项目、Inbox、归档和私人上下文，使用受限的 `shared-core` 模式。它只管理通用系统文件，不接管工作内容。

在公开仓库本地 clone 中先预览，再执行：

```bash
python3 kit/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN --dry-run
python3 kit/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN
```

目标 Vault 必须在 `.obsidian-ai-workflow-kit/adoption-policy.json` 中明确只允许 `shared-core`。详细边界见 [Source Sync Policy](docs/release/source-sync-policy.md)。

### 30 秒演示

先安装一个独立的演示库，体验后再用于自己的笔记：

1. 按 [30 秒演示](docs/30-second-demo.zh-CN.md) 将 full 模式安装到新的测试文件夹。
2. 在 Obsidian 里选择 **Open folder as vault**，选中安装目标文件夹。
3. 打开 `首页.md`，再把演示提示词发给 AI Agent。

安装完成后，AI 会用只读方式读取已填好的项目桥接卡，回答当前状态、最新决策和下一步动作。不需要 Obsidian 社区插件。

## 你会得到什么

| 需求 | 对应结构 |
|---|---|
| AI 不知道从哪开始 | `00-入口/开始这里.md` |
| 项目上下文散落各处 | `10-项目/` 里的项目桥接卡 |
| AI 写入太随意 | `90-系统/规则/` 里的治理规则 |
| 本机资料需要整理 | `20-资料/处理流程/` 里的资料处理流程 |
| 有用经验难召回 | `90-系统/召回/` 里的任务地图和召回字段 |
| 手写索引容易过期 | `90-系统/视图/` 中的项目、任务和资料 Base |
| 字段填错后页面从视图消失 | 类型化 status、`project_entry` 和 Base 字段健康检查 |
| vault 越用越乱 | 只读的链接、元数据和维护检查 |

## 它怎么工作

![Obsidian AI Workflow Kit 架构图](docs/images/architecture-flow.png)

日常使用保持很小：

```text
用户任务
  -> 00-入口/开始这里.md
  -> 对应项目桥接卡或任务地图
  -> 当前对话能完成就直接执行
  -> 只有排队、跨会话或阻塞时才写入 01-收件箱/任务/
  -> 只读取必要上下文
  -> 结构化写回
  -> 可复用经验进入后续召回
```

AI 默认不应该扫描整个 vault。它应该先读开工入口，再按任务映射打开必要上下文，完成任务后写回正确位置。需要专业视角时，直接在任务或验收标准中说明检查角度。

## 安装范围

默认安装最小启动模板。进阶用户可以传 `--mode full`，长期工作库则使用受限的 `--mode shared-core`。

| 模式 | 适合场景 | 会安装什么 |
|---|---|---|
| `barebone` | 给已有 vault 加一个最小入口 | 开工入口、核心工作目录、治理规则、项目登记、模板、`90-系统/脚本/kb.py` |
| `full` | 新建完整 starter vault | 核心工作流、模板、脚本、Bases 动态视图，以及 `90-系统/使用指南/` 和 `90-系统/示例/` |
| `shared-core` | 让长期工作库跟随公开核心 | 通用规则、资料流程、召回、模板、Bases、脚本和标准；不包含入口、项目、Inbox、归档和根目录文件 |

如果你不想用远程 `curl` 安装，可以本地克隆后运行：

```bash
bash install.sh --language zh-CN --dry-run "/path/to/your-vault"
bash install.sh --language zh-CN "/path/to/your-vault"
```

## 适合你吗？

适合：

- 你已经用 Obsidian 保存项目笔记、资料或决策。
- 你经常用 AI Agent，已经感受到换窗口后的上下文断层。
- 你想要本地优先、人工可编辑的 AI 记忆。
- 你愿意持续维护项目状态、交接和经验。

不适合：

- 你想要图形化 Obsidian 插件。
- 你想要云端记忆服务或托管 RAG 后端。
- 你想让 AI 自动扫描整台电脑。
- 你想自动批量改写已有 vault。

## 继续阅读

- [30 秒演示](docs/30-second-demo.zh-CN.md)
- [10 分钟首次体验](docs/10-minute-first-run.zh-CN.md)
- [Before / After 案例](docs/before-after-case.zh-CN.md)
- [自动化入门](docs/automation.zh-CN.md)
- [迁移指南](docs/migration.md)
- [核心概念](docs/concepts.zh-CN.md)
- [模板说明](docs/templates.zh-CN.md)
- [脚本说明](kit/00-AI/scripts/README.md)
- [v0.9.1 发布说明](docs/release/v0.9.1-release-notes.md)

## 安装后的知识库

中文安装的日常目录如下：

```text
首页.md                    人从这里开始
00-入口/开始这里.md          AI 从这里开工
01-收件箱/                  临时资料、待办和交接
10-项目/                    项目笔记与项目桥接卡
20-资料/                    外部资料和本机资料处理流程
30-经验资产/                可复用方法和经验
90-系统/                    规则、召回、视图、模板、脚本和配置
  使用指南/                 日常使用说明（仅 full）
  示例/                     工作流参考示例（仅 full）
```

日常先看首页，再按任务进入项目、资料或经验资产。系统规则和参考说明集中在 `90-系统/`，不用逐个浏览才能开始。

根目录另外保留 `AGENTS.md`、`CLAUDE.md` 供 AI 自动发现入口，以及 `LICENSE`、`VERSION` 记录授权和版本。隐藏目录 `.obsidian-ai-workflow-kit/` 保存更新清单。

English 安装沿用英文目录，详见 [English guide](README.md)。

## GitHub 源码目录

仓库按维护职责组织，供开发和贡献使用：

```text
kit/                       可安装的知识库模板与运行脚本
  00-AI/                   规则、模板、多语言版本和 CLI
  01-Inbox/                收件箱初始内容
  10-Projects/             项目初始内容
  20-SharedAssets/          经验资产初始内容
  40-ExternalSources/      资料初始内容
  index.md                 安装后首页的源文件
  AGENTS.md / CLAUDE.md    安装后 AI 入口的源文件
docs/                      使用文档和开发记录
examples/                  full 安装选用的示例源文件
assets/                    仓库展示素材
tests/                     开发测试
install.sh                 安装入口
```

在仓库目录运行 `bash install.sh --language zh-CN "/path/to/your-vault"`，然后用 Obsidian 打开目标目录。full 模式只安装选定的使用说明与示例，仓库 README、安装器、更新日志、发布清单和研发计划留在源码仓库。

## 成熟度

当前是 `0.x` beta starter kit，适合受控试用、小范围 vault 和反馈验证；不承诺兼容所有已有 Obsidian vault 结构。

这是一套 workflow kit，不是自动化平台。如果项目状态、决策、交接和经验长期不维护，它会慢慢退化成普通文件夹。

[任务接手与经验复用完整示例](examples/ai-handoff-demo/walkthrough.md)

## License

- 代码、脚本和可执行片段：[MIT](LICENSE)。
- 原创文字内容、模板、示例和文档：[CC BY 4.0](docs/legal/content-license.md)。
- 第三方内容不包含在本仓库授权范围内。

## Version

当前版本：`0.12.0`。见 [CHANGELOG.md](CHANGELOG.md)。
