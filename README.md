# lvsea-xiezuo

一个中文优先、证据驱动的小红书素材雷达专家 Skill，也是 `$lvsea-writing` 的可选前置研究节点。

它把关键词采集、互动指标筛选、核心矛盾分析、评论区复盘、素材分类、二创简报和飞书多维表导出串成一条可检查的流程。默认只读，平台采集与远端写入需要用户已有的授权和连接器。

## 来源与设计边界

本项目参考了 [X 上的公开案例](https://x.com/weiyux2021/status/2091828459630960703)：案例描述了按既有爆款关键词每日搜集素材、按分类归档到飞书多维表、再从中批量二创的工作流；配图可观察到关键词、角度、排除项、检查篇数、互动门槛，以及“核心矛盾 / 评论区主要观点 / 高赞评论原文 / 二创价值”等字段。

这里把截图中可复核的字段和门槛固化为规则，但没有把案例作者所述的数量或效率当成已验证效果。真实小红书 provider、飞书 API、账号权限、人工质量评审在本版本均标为 `missing_evidence`。

## 与 lvsea-writing 的关系：单入口路由

本 Skill 与 [lvsea-writing](https://github.com/lhylvsea/lvsea-writing) 是上下游关系，不是两个重复的通用写作 Skill。组合任务默认从 `$lvsea-writing` 进入：

- `lvsea-writing` 是用户默认入口，负责判断是否需要小红书素材前置、通用写作流程和最终编辑；
- `lvsea-xiezuo` 负责小红书素材的来源、指标门禁、评论证据、去重和二创方向，停止在“可审阅的写作输入”；
- `lvsea-writing` 负责通用写作的任务契约、研究复核、主判断、结构、读者、作者声音、场景格式、初稿、终稿，以及最后一步去 AI 味；
- 需要继续写正文时，先运行 `scripts/build_writing_handoff.py` 生成接力包，再交给 `$lvsea-writing`。不要把素材门禁和最终 Humanizer 塞进同一个入口。

如果用户只说“写一篇文章”“改稿”或“最后去 AI 味”，不要直接触发本 Skill；只有明确需要小红书素材研究、指标筛选、评论复盘或素材到写作的接力时，才显式调用 `$lvsea-xiezuo`。

本次接力设计参考了 [Zhiyu333 的公开文章](https://x.com/Zhiyu333/status/2099746344466579566) 指向的 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)。它只作为最后编辑阶段的研究参考：保留白名单式定点修改、信息守恒和样本审计；不复制其完整 Skill、研究数据或把报告中的统计特征当成普适阈值。详细字段映射见 [references/lvsea-writing-handoff.md](references/lvsea-writing-handoff.md)。

## 安装

### Codex / Agent Skills

```powershell
npx skills add lhylvsea/lvsea-xiezuo --skill lvsea-xiezuo --yes
```

安装后在新任务中使用。普通写作请调用 `$lvsea-writing`；只有素材研究或素材接力才调用本 Skill：

```text
使用 $lvsea-xiezuo：读取我的素材导出文件，按默认互动门槛筛选，输出 5 个带来源依据的二创简报；先不要同步飞书。
```

### 本地源码

```powershell
git clone https://github.com/lhylvsea/lvsea-xiezuo.git
cd lvsea-xiezuo
```

仅使用 Python 标准库，无额外依赖。

## 中文使用说明

先提供关键词、想找的角度、排除项、目标数量和 JSON/CSV 素材文件；再让 `$lvsea-xiezuo` 依次执行校验、指标门禁、证据分析、二创简报和 CSV 预览。没有真实 provider 或飞书连接器时不要补写数据，保留 `missing_evidence`。

## 最短可运行路径

仓库内的 `tests/fixtures/demo-materials.json` 是合成数据，只用于验证管线，不是平台真实数据。

```powershell
python scripts/validate_materials.py tests/fixtures/demo-materials.json
python scripts/filter_materials.py tests/fixtures/demo-materials.json `
  --reference-time 2026-08-25T12:00:00+08:00 `
  --output work/gated.json
python scripts/build_rewrite_brief.py work/gated.json `
  --output work/rewrite-brief.md --count 3
python scripts/build_writing_handoff.py work/gated.json `
  --output work/lvsea-writing-handoff.md --count 3
python scripts/export_feishu_csv.py work/gated.json `
  --output work/feishu-preview.csv
python -m unittest discover -s tests -v
```

预期结果：4 条 fixture 中 2 条通过指标门禁、1 条进入 `local_review`、1 条排除；同时生成二创简报、交给 `$lvsea-writing` 的接力包和可导入飞书的 UTF-8 CSV 预览。

## 输入字段

输入可以是 JSON 数组，也可以是 `{ "items": [...] }`。单条素材推荐结构：

| 字段 | 作用 | 备注 |
| --- | --- | --- |
| `source_id` | 来源唯一标识 | 不要编造；缺失会阻断 |
| `title` | 笔记标题 | 用于去重和选题 |
| `source_url` | 来源链接 | 支持 `http(s)` 或 `local:` |
| `text` | 正文或摘要 | 无正文只能做有限分析 |
| `published_at` | 发布时间 | 必须带时区；缺失进入本地复核 |
| `likes` / `comments` / `saves` | 互动数据 | 缺失或不确定不自动同步 |
| `keyword` | 搜索关键词 | 对应素材雷达任务 |
| `content_category` | 内容分类 | 例如“消费”“生意经” |
| `content_type` | 素材类型 | 例如 `high_discussion`、`low_fan_high_like`、`both` |
| `core_conflict` | 核心矛盾 | 观察事实，不写空泛标签 |
| `comment_summary` | 评论区主要观点 | 没有评论数据写 `missing_evidence` |
| `top_comment` | 高赞评论原文 | 只存用户有权处理的内容 |
| `remix_value` | 二创价值 | 必须说明新增角度或用途 |
| `ownership` | 权利边界 | `public_reference`、`owned`、`unknown` |

完整契约见 [references/material-schema.md](references/material-schema.md)。

## 默认门禁

以用户指定的 `reference_time` 为准：

- 发布 `<= 6` 小时且点赞 `>= 500`：`eligible`；
- 发布 `> 6` 小时且点赞 `>= 1000`：`eligible`；
- 评论 `>= 1000`：`eligible`；
- 指标、时间或来源无法核验：`local_review`；
- 其余明确低于门槛：`excluded`。

这些阈值来自公开案例配图，属于可配置的工作流默认值，不是小红书官方规则，也不是效果保证。

## 四个实际场景

1. **闲鱼 / 副业选题雷达**：以“闲鱼选品、冷门生意、信息差”为关键词，筛出高讨论素材，分析买卖双方的核心矛盾，再产出不同受众的二创选题。
2. **制造业知识账号**：以膨润土、高岭土、设备管理或安全生产为关键词，导入公开文章和自有案例，先做证据卡，再生成面向老板、采购或一线员工的不同写作简报。
3. **产品体验与消费观察**：按“吐槽 / 中产消费 / 会员争议”等角度采集公开素材，排除开箱、种草等不需要的方向，输出可复盘的观点矩阵。
4. **账号月度复盘与批量改写**：导入一段时间内的自有笔记数据，区分高讨论、低粉高赞和普通样本，生成带来源依据的系列选题，而不是把一篇原文机械改写 30 次。

## 注意事项：权限、隐私与限制

- 不内置小红书爬虫，不绕过登录、验证码或平台限制。若已有小红书 MCP 或其他合规 provider，Agent 只调用其已公开能力；否则使用用户导出的 JSON/CSV。
- 不内置飞书 Token，也不自动调用飞书写接口。`export_feishu_csv.py` 只生成本地预览；真实同步由用户明确授权的飞书连接器完成。
- 不把第三方 API Key、Cookie、私有附件、账号密码或本机绝对路径写入仓库。
- `local_review` 和 `unknown` 记录默认不进入远端；源记录、评论原文和图片的版权/隐私由使用者负责核验。
- “二创”不是洗稿。每条成稿应保留来源依据，同时新增观点、场景、结构或数据；发布前需要人工审核。
- 接力包不是成稿。`$lvsea-writing` 必须重新确认事实、读者、结构和作者声音，最后一步才做去 AI 味；统计检测不能替代人工判断。

## 开发与验证

```powershell
python scripts/check_package.py
python -m unittest discover -s tests -v
python scripts/build_writing_handoff.py tests/fixtures/demo-materials.json --output work/lvsea-writing-handoff.md --count 2
```

公开发布前由 `lvsea-zao-skill` 运行结构、触发、Skill IR、上下文、秘密扫描、功能分支、PR、Release、发现和干净安装门禁。详见 `reports/`。

## 许可

MIT，见 [LICENSE](LICENSE)。
