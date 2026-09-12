---
type: agent-handoff
record_format: compact-v1
created: {{date}}
updated: {{date}}
aliases: ["TPL-Agent交接卡", "Agent交接卡模板", "Agent Handoff Card Template"]
source_context: "" # session, task, or project reference
rule_version: ""
handoff_type: "" # end-of-session / mid-sync / incident
status: open # open / blocked / done / archived
tl_dr: ""
next_action: "" # 与正文“首要动作”一致；只作为字段镜像
links: []
---

# 交接卡：{{title}}

> 仅在另一个窗口或 Agent 需要接手时创建。这里保存接手所需的当前摘要；已有卡片逐段替换，无变化不写。正文上限为 1800 个 Unicode 字符且 80 个非空行，移除开头 YAML frontmatter 后计量，不是字数或 Token。规则见 `90-系统/规则/写回规则.md`。

## 接手目标与当前结果

{{一句话说明接手目标；最多 3 点说明接手必需的已完成结果与尚未完成事项。}}

## 下一步

- 首要动作：{{一个可执行动作，与 next_action 完全一致}}
- 必要依赖：{{最多 2 项；没有则删除此行}}

## 阻塞与操作边界

- {{未解决阻塞、现有授权和禁止动作；没有则写“无”。}}

## 关键证据与入口

- {{桥接卡、当前任务文档及验证结论的定位链接；标明尚未验证的部分。}}

> 完整实现过程和测试报告保存在既有项目日志、验收文档或可追溯历史，卡中只引用。超限先分流；不得为达标删除阻塞、授权边界或关键证据。仍不可压缩时，写明例外原因和复核条件。更新后执行只读检查：`python3 90-系统/脚本/kb.py check-record <本卡路径>`。
