# 素材字段契约

输入可以是 JSON 数组，也可以是：

```json
{
  "schema_version": "0.1",
  "items": [
    {
      "source_id": "owned-001",
      "source_url": "https://example.com/note/owned-001",
      "title": "一个可核验的素材标题",
      "text": "用户有权处理的正文或摘要",
      "published_at": "2026-08-25T08:30:00+08:00",
      "likes": 600,
      "comments": 30,
      "saves": 120,
      "keyword": "冷门生意",
      "content_category": "生意经",
      "content_type": "low_fan_high_like",
      "images": [],
      "core_conflict": "消费者期待与平台规则之间的落差",
      "comment_summary": "评论数据提炼出的主要观点；没有数据就写 missing_evidence",
      "top_comment": "用户有权处理的高赞评论原文",
      "remix_value": "可以切换到普通消费者视角，补充一个可验证案例",
      "ownership": "public_reference"
    }
  ]
}
```

## 字段状态

- `observed`：原始来源中可以直接核对的事实，例如标题、发布时间、互动数、评论原文。
- `inference`：基于素材作出的分析，例如核心矛盾、受众假设、二创价值；必须单独标注。
- `open_question`：缺少数据或需要人工确认的事项，例如作者是否授权、评论是否完整、图片版权。

## 指标门禁字段

脚本会在每条记录上写入：

- `gate_status`: `eligible`、`local_review` 或 `excluded`；
- `gate_reason`: 可复核的规则命中或缺失原因；
- `age_hours`: 以 `reference_time` 计算的素材年龄；
- `metric_basis`: 命中的点赞/评论条件。

默认条件来自公开案例截图，不是平台官方规则：

1. `age_hours <= 6` 且 `likes >= 500`；
2. `age_hours > 6` 且 `likes >= 1000`；
3. `comments >= 1000`。

发布时间、点赞或评论缺失时不能判定“低质量”，只能进入 `local_review`。导出和远端同步默认只包含 `eligible`。

## 去重与来源

`source_id` 是 canonical key；同一个来源不得因为不同关键词重复写成多条。`source_url` 必须是公开可访问的 `http(s)` 链接或用户明确提供的 `local:` 标识。不要把 Cookie、Token、私有链接、下载路径或本机绝对路径写入字段。

