# 证据驱动二创写作

## 先拆事实，再写观点

对每个素材使用以下四栏：

| 栏位 | 写什么 | 禁止什么 |
| --- | --- | --- |
| `observed` | 来源中能回看或由脚本计算的事实 | 把猜测写成数据 |
| `inference` | 对冲突、受众、结构和二创方向的分析 | 假装是原作者结论 |
| `open_question` | 需要补查、授权或人工判断的事项 | 用一句“应该没问题”跳过 |
| `source_basis` | 具体 `source_id`、字段和证据位置 | 只写“参考了爆款” |

## 每个二创候选的最小结构

```yaml
concept_id: "xhs-001"
problem_to_cut: "这篇内容要解决的一个读者问题"
target_reader: "有明确依据的受众；否则写 open_question"
hook_family: "冲突 / 反常识 / 清单 / 经验复盘 / 评论回应"
new_angle: "相对来源新增的视角或场景"
outline: ["hook", "evidence", "analysis", "action", "question"]
source_basis: ["owned-001:core_conflict", "owned-001:comment_summary"]
test_variable: "标题钩子、内容形式或受众视角中的一个变量"
prohibited_directions: ["逐句复述原文", "未经核实的收益承诺"]
evidence_status: "ready_for_human_review"
```

## 批量写作规则

- 目标数量只是候选上限，不是保证完成数量；证据不足时宁可少产出。
- 同一来源最多生成有限的不同角度，优先扩大受众、问题或形式，而不是同义替换。
- 每篇候选至少增加一个新事实、新案例、新解释或新行动建议；无法增加时标为 `open_question`。
- 不能把作者的具体经历、收益、身份和评论观点泛化成所有人的结论。
- 先生成简报和标题方向，再生成正文；正文发布前保留人工审核节点。
- 不默认强加 emoji、标签或夸张“爆款”话术；以账号定位和真实证据为准。

