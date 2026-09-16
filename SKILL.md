---
name: lvsea-xiezuo
description: "中文触发：仅当用户要做小红书素材库/素材雷达、关键词与角度采集、互动指标筛选、评论分析、飞书整理或来源驱动的二创写作简报时调用。作为 $lvsea-writing 的素材前置专家，生成可审阅的 source-backed handoff；不要用于普通写作、通用改稿、独立最终去 AI 味、单次标题或自动发布。Use for evidence-led Xiaohongshu material radar and reviewable writing handoffs. The primary entry for combined writing is $lvsea-writing."
metadata:
  author: "海洋哥 / lhylvsea"
  version: "0.1.3"
  upstream_inspiration: "https://x.com/weiyux2021/status/2091828459630960703; https://x.com/Zhiyu333/status/2099746344466579566; https://github.com/larashero3-dotcom/lieflat-less-ai-tone; https://github.com/lhylvsea/lvsea-writing"
---

# Lvsea 小红书素材雷达专家

把“找素材、看数据、读评论、提炼角度、交接给写作 Skill”变成一个可追溯的内容前置工作流。默认只读，不代替用户登录、绕过平台限制、复制原文或直接发布。

## 单入口关系

用户面对多 Skill 写作任务时，默认只调用 `$lvsea-writing`。本 Skill 是它按需调用的小红书素材专家：

```text
$lvsea-writing -> $lvsea-xiezuo: 小红书素材、指标、评论和来源证据
$lvsea-xiezuo -> $lvsea-writing: 写作接力包
$lvsea-writing -> $lieflat-less-ai-tone: 完整初稿后的最后一轮定点编辑
```

用户也可以显式调用 `$lvsea-xiezuo`，但仅用于素材雷达、证据卡、二创简报和写作接力；通用写作、完整文章改稿和最终去 AI 味应回到 `$lvsea-writing`。

## 中文使用说明

输入关键词、角度、排除项和素材导出文件，按“校验 -> 指标门禁 -> 证据卡 -> 二创简报 -> 本地导出”的顺序执行；没有 provider 或飞书连接器时，继续使用本地 JSON/CSV，并明确写出 `missing_evidence`。

## 触发条件与边界

触发于以下组合意图：

- 关键词/角度/排除项驱动的小红书素材采集或素材库建设；
- 按互动指标筛选高讨论、低粉高赞或类似素材，并做内容复盘；
- 需要提炼“核心矛盾、评论区主要观点、高赞评论、二创价值”；
- 将素材整理为飞书多维表字段，或从素材批量生成可审核的二创写作简报；
- 已完成素材筛选、希望继续写正文时，生成写作接力包交给 `$lvsea-writing`；不要让本 Skill 越过证据和简报直接批量产出最终正文。

仅要求通用写作、改写一篇完整文章、做最终去 AI 味、解释小红书概念、生成一次性标题、直接搬运原文或发布内容时不要触发。

## 应用场景

- 用“闲鱼选品 / 冷门生意”素材提炼副业选题；
- 用制造业公开资料和自有案例生成知识账号简报；
- 用消费争议和评论观点生成不同受众的内容方向；
- 用自有账号历史数据做月度素材复盘与批量二创规划。

## 输入契约

先锁定一份简短 brief：

```yaml
keywords: ["主题或搜索词"]
angles: ["想看的角度"]
exclude: ["不要的内容"]
target_count: 30
audience: "目标读者"
source_mode: "provider | local-import"
reference_time: "可选，带时区的 ISO-8601 时间"
```

素材记录至少包含 `source_id`、`title`、`source_url`；可选字段包括 `text`、`author`、`published_at`、`likes`、`comments`、`saves`、`images`、`keyword`、`content_category`、`content_type`、`core_conflict`、`comment_summary`、`top_comment`、`remix_value` 和 `ownership`。字段详情见 [素材字段契约](references/material-schema.md)。

## 执行流程

1. **确定来源**：优先使用当前已配置且用户授权的官方/平台适配器；没有可用 provider 时，要求用户提供 JSON/JSONL/CSV 导出，或只生成待采集清单。不得凭空补写点赞、评论、发布时间、作者或原文。
2. **规范化与门禁**：先运行 `scripts/validate_materials.py`，再运行 `scripts/filter_materials.py`。默认保留规则为：发布 6 小时内点赞不少于 500；超过 6 小时点赞不少于 1000；或评论不少于 1000。时间和数值缺失、矛盾或来源不可核验时标为 `local_review`，不得自动同步。
3. **证据化分析**：对入选素材分别写出 `observed`、`inference`、`open_question`。提炼核心矛盾、评论区主要观点、高赞评论原文和二创价值；没有评论数据时写明缺口，不模拟“评论共识”。
4. **分类与去重**：按关键词、内容分类和素材类型归档；同一来源只保留一个 canonical 记录。二创必须改变切入点、受众或表达结构，并记录 `source_basis`，不逐句改写或拼接多篇原文。
5. **生成写作简报**：运行 `scripts/build_rewrite_brief.py` 输出可审核简报。每个候选只解决一个问题，标出事实依据、待核问题、拟测试变量和禁止方向；最终笔记由 Agent 基于简报创作，不把脚本输出冒充成已完成的 30 篇成稿。
6. **写作接力**：用户要求继续写正文时运行 `scripts/build_writing_handoff.py`，默认只传递 `eligible`；用户明确允许时才加入 `local_review`。接力包交给 `$lvsea-writing` 重新做任务契约、证据、结构、读者、声音和场景检查；最后去 AI 味属于下游最后编辑阶段，不在这里提前执行。字段映射和来源边界见 [写作接力说明](references/lvsea-writing-handoff.md)。
7. **导出/同步**：需要飞书时先运行 `scripts/export_feishu_csv.py` 做本地预览。只有用户明确授权并且字段、账号和目标表已经确认，才调用对应飞书连接器；`local_review`、缺来源或含敏感信息的记录不写入远端。

## 输出契约

输出必须分为五层：

1. `素材门禁结果`：总数、`eligible`、`local_review`、`excluded`，以及每条记录的理由；
2. `证据卡`：来源、指标、原始观察、推断、开放问题；
3. `二创简报`：候选标题方向、核心矛盾、目标读者、内容结构、来源依据、测试变量和风险；
4. `写作接力包`：仅在用户要继续写正文时生成，明确交给 `$lvsea-writing`，不包含自动成稿；
5. `限制与下一步`：provider 是否真实运行、是否有人工复核、是否完成飞书同步，缺失时写 `missing_evidence`。

不要使用“保证爆款”“提升 X%”“已自动采集”等超出来源和实跑证据的表述。

## 关键安全边界

- 只处理用户有权使用的公开或自有素材；尊重平台条款、作者署名、版权和隐私。
- 不读取、保存或提交 Cookie、Token、API Key、私有附件或本机绝对路径。
- 不执行未审查的第三方安装器、爬虫、hook 或发布脚本；平台 provider 缺失时降级到本地导入。
- 不自动点赞、评论、发帖或批量同步；所有外部写入都必须是用户当轮明确授权的动作。
- 原文引用只用于证据卡，二创输出必须有新增观点、结构或场景；不把“改几个词”当作原创。
- `lieflat-less-ai-tone` 只作为下游最后编辑阶段的公开研究参考；统计特征是风险信号，不是通用阈值，也不能替代事实核验和作者终审。

## 本地可运行验证

在 Skill 根目录执行：

```powershell
python scripts/validate_materials.py tests/fixtures/demo-materials.json
python scripts/filter_materials.py tests/fixtures/demo-materials.json --reference-time 2026-08-25T12:00:00+08:00 --output work/gated.json
python scripts/build_rewrite_brief.py work/gated.json --output work/rewrite-brief.md --count 3
python scripts/build_writing_handoff.py work/gated.json --output work/lvsea-writing-handoff.md --count 3
python scripts/export_feishu_csv.py work/gated.json --output work/feishu-preview.csv
python -m unittest discover -s tests -v
```

这些命令只使用仓库内合成 fixture，不代表已连接小红书或飞书。连接器、登录态、真实用户输出和人工盲评均在当前版本标为 `missing_evidence`。
