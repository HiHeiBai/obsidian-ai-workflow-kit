# 30 秒演示

下载后直接打开中文知识库，再让 AI 用约 30 秒说明项目状态。

## 打开演示库

1. [下载 GitHub ZIP](https://github.com/HiHeiBai/obsidian-ai-workflow-kit/archive/refs/heads/main.zip)，解压。
2. 在 Obsidian 中选择 **打开本地仓库 / Open folder as vault**，打开解压目录里的 **`kit/` 文件夹**。
3. 点击 `首页.md`。已填好的演示项目在 `90-系统/示例/filled-example/`。

无需运行安装命令。你在 GitHub 的 `kit/` 中看到的就是这个知识库；开发源码与发布文档在它外面。

## 体验只读接手

将下面的占位符替换为演示库的绝对路径，发给能读取本地文件的 AI Agent：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<kit 文件夹的绝对路径>。请先读取 00-入口/开始这里.md，然后使用 90-系统/示例/filled-example 里的只读演示项目。告诉我当前项目状态、最新决策和下一步动作。不要编辑文件或创建任务卡。
```

## 预期效果

AI 应该读取：

- `00-入口/开始这里.md`
- `首页.md`
- `90-系统/示例/filled-example/BRIDGE-launch-notes.md`
- `90-系统/示例/filled-example/current-state.md`
- `90-系统/示例/filled-example/decisions.md`

然后说明演示项目的当前状态、最新决策、下一步动作，以及真实任务应该写回哪里。使用指南与参考示例集中在 `90-系统/`，研发文档留在源码仓库。
