---
type: system-guide
status: active
---

# System Guide / 系统说明

日常从知识库首页进入项目、资料和自己的经验区。这里集中保存支持这些工作的规则与工具。

Use the vault home for daily work. This area contains the rules and tools that support it.

- [Agent entry / AI 开工入口](START-HERE.md)
- [Governance / 协作规则](governance/README.md)
- [Templates / 项目桥接卡模板](templates/TPL-project-bridge-card.md)
- [Recall / 召回](recall/README.md)
- [Material intake / 资料整理](pipeline/README.md)

完整安装还包含使用指南、演示和动态视图；最小安装可先建立自己的项目。脚本通过命令行按需运行。默认用首页的开工提示词启动 AI。授权和版本信息收在 about/，更新清单收在 config/kit-manifest.json；中文安装对应「关于/」和「配置/」。如需自动发现入口，按需将 integrations/（中文为「接入/」）中的 AGENTS.md 或 CLAUDE.md 复制到知识库根目录；已有同名文件时合并指令，不要覆盖。

Full installs also include guides, demonstrations, and dynamic views. Minimal installs are ready for your own projects. Use the startup prompt on the home page to begin an AI session. License and version information live in about/, and the update manifest lives in config/kit-manifest.json. For optional automatic discovery, copy the matching AGENTS.md or CLAUDE.md from integrations/ to the vault root; merge instructions if a root file already exists. Keeping these templates in the system directory does not enable root-level discovery.
