# 与 lvsea-writing 的写作接力

## 两个 Skill 的分工

`lvsea-xiezuo` 是上游的“小红书素材雷达”：负责在用户有权处理的公开或自有数据中做来源校验、互动门禁、证据拆分、评论分析、去重和二创选题简报。它停在“可审阅的写作输入”，不在没有任务契约、主判断和作者声音的情况下直接批量生成最终正文。

`lvsea-writing` 是下游的通用写作入口，负责把接力输入重新放回完整写作流程：

```text
$lvsea-xiezuo: 素材 -> 门禁 -> 证据卡 -> 二创简报 -> 写作接力包
$lvsea-writing: 任务契约 -> 资料/证据 -> 主判断与结构 -> 读者 -> 声音 -> 场景 -> 初稿 -> 最后去 AI 味 -> 作者终审
```

不要把两个 Skill 合并成一个宽泛的“写作 Skill”：前者的触发条件应保持小红书素材任务边界，后者才负责通用写作和最后编辑。

## 接力字段映射

`scripts/build_writing_handoff.py` 只生成 Markdown 接力包，不生成正文，也不把推断升级成事实。

| `lvsea-xiezuo` 字段 | 交给 `lvsea-writing` 的处理 | 不能直接当成 |
| --- | --- | --- |
| `source_basis`、`source_url` | 证据账本和来源核验入口 | 已经核实的全部背景 |
| `observed`、互动指标 | 资料事实与范围 | 质量、传播或收益保证 |
| `inference`、`remix_value` | 主判断候选和二创角度 | 原作者结论 |
| `open_question`、`ownership` | 待核项、权限和版权边界 | 可以忽略的备注 |
| `core_conflict`、`problem_to_cut` | 任务契约与读者问题 | 唯一正确的文章主旨 |
| `target_reader`、`new_angle`、`outline` | 读者测试和结构设计 | 已完成的文章结构 |
| `content_type`、`test_variable` | 场景格式和实验变量 | 平台效果预测 |
| `prohibited_directions` | 写作约束 | 对事实核验的替代 |

接力后，`lvsea-writing` 仍需重新确认体裁、作者意图、目标读者、篇幅、来源截止时间、不能改变的事实和交付格式。若信息不足，宁可停在简报或待核项，不用“去 AI 味”掩盖前置缺口。

## 最后去 AI 味的来源边界

X 文章 [做了一个可能有最多数据支撑的去 AI 味 skill](https://x.com/Zhiyu333/status/2099746344466579566) 指向了 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)。本项目只把它作为下游最后编辑阶段的研究参考，不复制它的完整 Skill、数据集、脚本或研究结论。

可以吸收的工作方法是：白名单式定点修改、信息守恒、先审计命中样本再推广操作符，并把统计特征当作风险信号而不是作者身份或质量真值。仓库中的比例、阈值和特征结论属于该项目的研究报告，不能直接外推到所有模型、体裁或作者。

## 使用边界

1. 只有在素材已经完成门禁和证据整理后，才生成接力包；默认不包含 `local_review`。
2. 用户明确要求继续写正文时，把接力包交给 `$lvsea-writing`；若只要求素材分析，停在 `lvsea-xiezuo` 的证据卡和简报。
3. `$lvsea-writing` 完成资料复核、结构和初稿后，最后一步才做 Humanizer/去 AI 味，再交给作者人工终审。
4. 任何真实经历、数字、引语、评论共识、版权许可和平台效果都必须在下游再次核对，不能因为接力包已有字段就视为已验证。
