---
type: recall-map
status: active
---

# Task To Context Map

需要定位任务上下文时使用此表；已知目标可直达对应事实源，不要求先读本表。

| 任务类型 | 常用入口 | 按缺口补充 |
|---|---|---|
| 整理本机资料 | `00-AI/pipeline/local-material-intake.md` | `00-AI/pipeline/source-to-knowledge-workflow.md` |
| 接手项目 | 对应项目桥接卡、`current-state.md`、`decisions.md` | 相关经验资产 |
| 整理外部资料 | `00-AI/pipeline/README.md`、`00-AI/templates/TPL-source-analysis-card.md` | 对应项目桥接卡 |
| 沉淀经验 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-question-knowledge-experience-asset-card.md` | 来源交接卡 |
| 复盘问题/事故 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-incident-experience-card.md` | 来源交接卡、项目桥接卡、相关日志 |
| 维护知识库 | `00-AI/governance/maintenance-loop.md`、`20-SharedAssets/02-modules/vault-health-checklist-v1.md` | 最近健康报告 |
| 写交接 | `00-AI/templates/TPL-agent-handoff-card.md` | 项目桥接卡 |
| 理解召回链 | `00-AI/recall/example-recall-chain.md` | 当前任务对应的真实项目桥接卡 |

## 使用规则

- 只读取任务缺少的上下文；同一行列出的文件不是必须全部读取的清单。
- 私人经验需要跨任务召回时，补到用户所有的主题或本地召回入口；项目内部引用已有桥接或事实页即可。本表只维护通用路由，改进应在公开源码完成后导入。
- 如果项目桥接卡过期，先提醒用户，再继续短任务；长任务开始前建议更新桥接卡。
