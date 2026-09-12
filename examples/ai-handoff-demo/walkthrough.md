---
type: example
status: active
---

# 从接手任务到复用经验 / From handoff to lesson reuse

这是虚构的产品更新写作案例，不含真实项目、私人路径或客户材料。下面展示预期过程，不代表 Agent 已执行这些操作。现有 [Launch Notes](../filled-example/README.md) 示例停在“事实未补齐”，保持不变。

## 1. 接手：先知道缺什么

用户任务：“接手 Launch Notes，准备新版引导流程的发布说明。”

Agent 读取开工入口、[项目桥接卡](../filled-example/BRIDGE-launch-notes.md)、[当前事实](../filled-example/current-state.md)和[决策](../filled-example/decisions.md)。事实页缺发布日期、前后对比、适用人群和限制。

合理回应：“提纲已就绪，但最终稿还缺四项产品事实。我先整理现有结构，待事实补齐后完成正文。”此时可以整理提纲，不能编造发布日期或宣称已发布。

## 2. 推进：把事实和摘要分开

假设用户随后提供这些虚构事实：10 月 1 日开放；必填问题由五个减至两个；只适用于新账户；旧账户暂不迁移。

Agent 先将事实与来源写入实际项目的 `current-state.md`，完成草稿并链接到该页，再替换桥接卡中的当前状态和下一步。已有决定仍在 `decisions.md` 保存。

桥接卡摘要可以是：

```text
当前状态：产品事实已补齐，发布说明草稿完成，等待内容审核。
有效决策：保留适用人群和旧账户限制；未获发布授权。
首要动作：请项目负责人审核草稿中的事实和适用范围。
```

frontmatter `next_action` 与首要动作保持一致。`last_verified` 只填实际事实核验日期；格式整理不能刷新它。桥接卡写后运行 `python3 00-AI/scripts/kb.py check-record <card.md>`。

任务在当前对话完成且无需转交时，不建交接卡。若另一个 Agent 确实要接手审核，交接只保留草稿入口、待审核点、发布授权边界和首要动作。

## 3. 沉淀：保存能再次使用的方法

值得复用的经验是：“写产品更新前，先确认发布日期、具体变化、适用对象和已知限制。”使用[经验卡模板](../../src/00-AI/templates/TPL-question-knowledge-experience-asset-card.md)，在实际 vault 的 `20-SharedAssets/01-user-assets/` 保存，而不写入受管通用模块。

经验卡应包含：触发场景是准备发布说明；方法是四项事实检查；依据链接到项目事实和审核记录；边界是检查清单不能替代产品核验或发布授权。这个案例只能提供候选方法，后续任务验证有效后再扩展适用范围。

## 4. 再次召回：新任务直接用上

下一次任务：“为另一个产品写更新说明。”

将确认有用的经验卡链接加入用户维护的项目桥接卡，或本地扩展任务地图。下次 Agent 沿该入口找到四项检查清单，先核实新项目自己的事实，再写正文；不能复用前一个项目的日期、范围或授权。

验收依据：新会话能找到当前事实和一个首要动作；旧过程没有挤进桥接摘要；经验能从明确入口找回；没有自动生成多余交接卡，也没有未经授权发布。

## English walkthrough

This fictional example demonstrates expected behavior, not completed operations. The existing Launch Notes fixture remains at its original facts-incomplete stage.

1. **Resume:** read the entry, bridge, current state, and decisions. Identify the missing release date, before/after change, audience, and limitations. Prepare the outline while awaiting those facts.
2. **Write back:** suppose the owner confirms an October 1 release, five required questions reduced to two, new accounts only, and no migration for existing accounts. Record the facts and their source in the project's current-state document, link the draft, and replace the bridge's current summary. Keep one primary action: owner review of the draft's facts and scope. Mirror it in `next_action`; use only an actual fact-check date for `last_verified`. Run `check-record` after editing the bridge. Publication remains unauthorized.
3. **Promote a lesson:** create a user-owned experience card for the four-fact checklist, linking its evidence and stating its limits. Treat it as a candidate method until subsequent tasks validate its usefulness. Do not write generated lessons into managed modules.
4. **Recall:** link the lesson from a user-maintained bridge or local task map. A later writing task follows that link and checks its own product facts. It must not reuse the previous project's dates, audience, or authorization.

Create a temporary handoff only for an actual transfer to another session or agent. Include the draft link, review questions, publication boundary, and primary action. Success means a new session can find current facts, one next action, and the reusable lesson without reading a conversation log.
