#!/usr/bin/env python3
"""Turn gated records into a source-backed, human-reviewable writing brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from material_lib import load_items


def text_or_missing(value: Any) -> str:
    value = "" if value is None else str(value).strip()
    return value or "missing_evidence"


def render_brief(items: list[dict[str, Any]], count: int, include_review: bool = False) -> str:
    allowed = {"eligible"}
    if include_review:
        allowed.add("local_review")
    selected = [item for item in items if str(item.get("gate_status", "")) in allowed][:count]
    lines = [
        "# 小红书二创写作简报",
        "",
        "> 本文件只把已筛选素材整理成写作输入，不是自动发布稿，也不替代事实、版权和人工审核。",
        "",
        f"- 候选上限：{count}",
        f"- 实际候选：{len(selected)}",
        f"- 是否含 local_review：{'是' if include_review else '否'}",
        "- provider / 人工质量证据：missing_evidence（除非调用方另行提供）",
        "",
        "## 写作总规则",
        "",
        "1. 每个候选只解决一个读者问题。",
        "2. 保留 source_basis，新增角度、场景或解释，不逐句复述。",
        "3. 事实、推断和待核问题分开写。",
        "4. 不使用未经来源支持的收益承诺、身份标签或平台效果数据。",
        "",
    ]
    if not selected:
        lines.extend(["## 结果", "", "没有满足当前门禁的候选；不要用猜测补齐数量。", ""])
        return "\n".join(lines)
    for index, item in enumerate(selected, start=1):
        source_id = text_or_missing(item.get("source_id"))
        lines.extend([
            f"## 候选 {index:02d}：{text_or_missing(item.get('title'))}",
            "",
            f"- `concept_id`: xhs-{index:03d}",
            f"- `source_basis`: {source_id}:title; {source_id}:core_conflict; {source_id}:comment_summary",
            f"- `source_url`: {text_or_missing(item.get('source_url'))}",
            f"- `gate_status`: {text_or_missing(item.get('gate_status'))}（{text_or_missing(item.get('gate_reason'))}）",
            f"- `keyword`: {text_or_missing(item.get('keyword'))}",
            f"- `content_category`: {text_or_missing(item.get('content_category'))}",
            f"- `content_type`: {text_or_missing(item.get('content_type'))}",
            f"- `observed`: 发布时间 {text_or_missing(item.get('published_at'))}；点赞 {text_or_missing(item.get('likes'))}；评论 {text_or_missing(item.get('comments'))}。",
            f"- `core_conflict`: {text_or_missing(item.get('core_conflict'))}",
            f"- `comment_summary`: {text_or_missing(item.get('comment_summary'))}",
            f"- `top_comment`: {text_or_missing(item.get('top_comment'))}",
            f"- `remix_value`: {text_or_missing(item.get('remix_value'))}",
            "- `inference`: 需要 Agent 根据上述观察提出一个新增视角，并明确这是推断。",
            "- `open_question`: 核验原文使用权、评论完整性、图片权利和任何具体收益/效果说法。",
            "- `outline`: hook -> evidence -> analysis -> action -> reader_question",
            "- `test_variable`: 只选择一个（标题钩子 / 受众视角 / 内容形式 / 评论回应）。",
            "- `prohibited_directions`: 逐句改写、拼接原文、编造评论或互动数据、自动发布。",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a source-backed rewrite brief from gated materials.")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--include-review", action="store_true")
    args = parser.parse_args()
    if args.count < 1:
        print("ERROR: count must be positive", file=sys.stderr)
        return 1
    try:
        content = render_brief(load_items(args.input), args.count, args.include_review)
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

