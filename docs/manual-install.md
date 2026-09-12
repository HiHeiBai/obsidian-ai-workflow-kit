# 手动安装与更新

通常只需要把 [首页](../README.md) 的一句话发给 AI。本页供需要自己操作或维护已有知识库的人使用；AI 部署流程见 [AI_DEPLOY.md](../AI_DEPLOY.md)。

## 下载中文知识库

1. [下载 ZIP](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/archive/refs/heads/main.zip) 并解压。
2. 将整个 `kit/` 文件夹放到希望长期保存的位置，可以重命名为「AI知识库」。
3. 在 Obsidian 中选择「打开本地仓库 / Open folder as vault」，打开这个文件夹，点击 `首页.md`。

不要把整个源码仓库当作知识库。`kit/` 是完整中文库，开发文档、源码和测试在其外部。

将实际绝对路径填入，再发给能读取本地文件的 AI：

```text
这个知识库位于：<知识库绝对路径>。请先读取其中的 00-入口/开始这里.md，按开工流程接手。
```

## 使用安装器

下载或克隆仓库后，在仓库根目录运行以下命令（需要 Bash 和 Python 3）。以下命令显式安装完整中文库；底层安装器不带参数时仍为英文最小模式。始终将示例路径换成你的目标路径，并先查看预览：

```bash
bash install.sh --language zh-CN --mode full --dry-run "/path/to/your-vault"
bash install.sh --language zh-CN --mode full "/path/to/your-vault"
```

如需英文完整库，显式指定：

```bash
bash install.sh --language en --mode full --dry-run "/path/to/your-vault"
bash install.sh --language en --mode full "/path/to/your-vault"
```

安装器默认跳过已有文件；这不等于能自动适配任意已有库。目标已有内容但没有托管清单时，先判断要接入已有结构还是另建知识库，不要整体覆盖或直接重排。只有明确要替换内容时才考虑 `--overwrite`。

也可直接使用 Python 3 CLI，无需 Bash：

```bash
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --language zh-CN --mode full --dry-run
python3 src/00-AI/scripts/kb.py install-core "/path/to/your-vault" --language zh-CN --mode full
```

## 更新已有托管库

在最新源码仓库内，先预览，再更新：

```bash
bash install.sh --update --dry-run "/path/to/your-vault"
bash install.sh --update "/path/to/your-vault"
```

省略语言和模式时，更新器自动沿用清单中的安装设置，下载后直接使用的 `kit/` 也适用。托管更新只替换未被用户改动的受管文件；保留并报告冲突。不要将新版 `kit/` 整体复制覆盖到正在使用的库上。

Python 3 的对应命令是 `python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/your-vault"`；预览时追加 `--dry-run`。

## 安装范围与长期工作库

| 模式 | 用途 |
|---|---|
| `full` | 新建完整知识库，包含工作流、模板、视图、用户指南和示例；首页 AI 部署的默认选择 |
| `barebone` | 明确只需要最小启动工作流时，使用 `--mode barebone` |
| `shared-core` | 已有成熟工作库只同步通用规则、模板和脚本，不接管入口和私人工作内容 |

受保护的长期工作库须遵守其 `.obsidian-ai-workflow-kit/adoption-policy.json`，不要绕过保护。采用 shared-core 的工作库可在核对授权范围后执行：

```bash
python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN --dry-run
python3 src/00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN
```

具体边界见 [Source Sync Policy](release/source-sync-policy.md)。

## 检查与 AI 接入

中文完整库的只读检查：

```bash
python3 "/path/to/your-vault/90-系统/脚本/kb.py" health-check --vault "/path/to/your-vault" --mode full
```

英文库脚本路径为 `00-AI/scripts/kb.py`，人从 `index.md` 开始，AI 从 `00-AI/START-HERE.md` 开工。已有库检查时使用实际安装模式。没有 Python 3 时仍可直接打开下载的中文库，但自动健康检查不能运行。

默认知识库顶层只有首页与功能目录。许可证、版本、更新清单和接入模板在系统区。若明确需要 Codex 或 Claude Code 自动发现入口，可把中文库 `90-系统/接入/`（英文库 `00-AI/integrations/`）中对应的 `AGENTS.md` 或 `CLAUDE.md` 模板复制到知识库根目录；已有同名文件时合并，不要替换。

## 继续阅读

- [30 秒演示](30-second-demo.zh-CN.md)
- [10 分钟首次体验](10-minute-first-run.zh-CN.md)
- [任务接手与经验复用示例](../examples/ai-handoff-demo/walkthrough.md)
- [迁移指南](migration.md)
- [核心概念](concepts.zh-CN.md)
- [模板说明](templates.zh-CN.md)
- [脚本说明](../src/00-AI/scripts/README.md)

当前为 `0.x` 版本，适合逐步采用；已有知识库需按实际结构评估接入方式。内容保存在本地 Markdown 文件中，持续更新项目状态和经验才能帮助后续会话接手。
