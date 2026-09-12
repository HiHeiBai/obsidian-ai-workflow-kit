# 30 秒演示

先安装一个独立演示库，再让 AI 用约 30 秒说明项目状态。Obsidian 打开的文件夹是安装目标目录。

## 安装演示库

下载或克隆仓库后，在仓库目录运行：

```bash
bash install.sh --language zh-CN --mode full "$HOME/obsidian-ai-workflow-demo"
```

也可以直接安装：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --mode full "$HOME/obsidian-ai-workflow-demo"
```

给演示使用一个新文件夹。在 Obsidian 中选择 **Open folder as vault**，打开 `~/obsidian-ai-workflow-demo`，点击 `首页.md`。

## 体验只读接手

将下面的占位符替换为演示库的绝对路径，发给能读取本地文件的 AI Agent：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<安装后的演示库绝对路径>。请先读取 00-入口/开始这里.md，然后使用 90-系统/示例/filled-example 里的只读演示项目。告诉我当前项目状态、最新决策和下一步动作。不要编辑文件或创建任务卡。
```

## 预期效果

AI 应该读取：

- `00-入口/开始这里.md`
- `首页.md`
- `90-系统/示例/filled-example/BRIDGE-launch-notes.md`
- `90-系统/示例/filled-example/current-state.md`
- `90-系统/示例/filled-example/decisions.md`

然后说明演示项目的当前状态、最新决策、下一步动作，以及真实任务应该写回哪里。使用指南与参考示例集中在 `90-系统/`，研发文档留在源码仓库。
