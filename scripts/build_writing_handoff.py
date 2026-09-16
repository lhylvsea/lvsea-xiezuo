#!/usr/bin/env python3
"""Build a source-backed handoff package for the downstream lvsea-writing Skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from material_lib import load_items


def text_or_missing(value: Any) -> str:
    value = "" if value is None else str(value).strip()
    return value or "missing_evidence"


def render_handoff(items: list[dict[str, Any]], count: int, include_review: bool = False) -> str:
    allowed = {"eligible"}
    if include_review:
        allowed.add("local_review")
    selected = [item for item in items if str(item.get("gate_status", "")) in allowed][:count]
    lines = [
        "# lvsea-writing 接力包（由 lvsea-xiezuo 生成）",
        "",
        "> 这是写作输入，不是成稿。`lvsea-writing` 必须重新核对事实、任务契约、读者、结构、声音和交付场景；最后一步才做去 AI 味。",
        "",
        f"- 候选上限：{count}",
        f"- 实际候选：{len(selected)}",
        f"- 是否含 local_review：{'是' if include_review else '否'}",
        "- 上游状态：素材门禁与证据字段由 lvsea-xiezuo 提供；provider、版权和人工质量证据仍需下游确认。",
        "- 下游入口：`$lvsea-writing`",
        "",
        "## 接力规则",
        "",
        "1. `source_basis`、`observed`、`inference` 和 `open_question` 必须在写作中保持分层。",
        "2. 不把互动指标变成传播、收益或平台效果承诺。",
        "3. 不把评论摘要写成全体读者共识，不补写没有来源的经历、动作、数字和引语。",
        "4. 接力包只提供方向和约束，不提前执行最后的 Humanizer。",
        "",
    ]
    if not selected:
        lines.extend(["## 结果", "", "没有满足当前门禁的候选；不要用猜测补齐数量。", ""])
        return "\n".join(lines)

    for index, item in enumerate(selected, start=1):
        source_id = text_or_missing(item.get("source_id"))
        gate_status = text_or_missing(item.get("gate_status"))
        lines.extend([
            f"## 候选 {index:02d}：{text_or_missing(item.get('title'))}",
            "",
            f"- `handoff_status`: {'ready_for_lvsea-writing' if gate_status == 'eligible' else 'local_review_requires_user_check'}",
            f"- `source_basis`: {source_id}:title; {source_id}:text; {source_id}:core_conflict; {source_id}:comment_summary",
            f"- `source_url`: {text_or_missing(item.get('source_url'))}",
            f"- `ownership`: {text_or_missing(item.get('ownership'))}",
            f"- `gate_status`: {gate_status}（{text_or_missing(item.get('gate_reason'))}）",
            f"- `observed`: 发布时间 {text_or_missing(item.get('published_at'))}；点赞 {text_or_missing(item.get('likes'))}；评论 {text_or_missing(item.get('comments'))}；收藏 {text_or_missing(item.get('saves'))}。",
            f"- `core_conflict`: {text_or_missing(item.get('core_conflict'))}",
            f"- `comment_summary`: {text_or_missing(item.get('comment_summary'))}",
            f"- `top_comment`: {text_or_missing(item.get('top_comment'))}",
            f"- `remix_value`: {text_or_missing(item.get('remix_value'))}",
            "",
            "### 交给 lvsea-writing",
            "",
            f"- `problem_to_cut`: {text_or_missing(item.get('core_conflict'))}",
            f"- `target_reader`: {text_or_missing(item.get('target_reader'))}",
            f"- `new_angle`: {text_or_missing(item.get('remix_value'))}",
            "- `main_claim_candidate`: 待下游根据证据写成可被反驳的主判断；本行不是事实结论。",
            "- `outline_seed`: hook -> evidence -> analysis -> action -> reader_question；由下游按体裁重排。",
            "- `test_variable`: 只选择一个（标题钩子 / 受众视角 / 内容形式 / 评论回应）。",
            f"- `open_question`: 核验原文使用权、评论完整性、图片权利，以及任何具体收益或效果说法；原始字段：{text_or_missing(item.get('open_question'))}",
            "- `prohibited_directions`: 逐句改写、拼接原文、编造评论或互动数据、把推断写成来源结论、提前做去 AI 味以掩盖证据缺口。",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a source-backed handoff package for lvsea-writing.")
    parser.add_argument("input", help="gated JSON/CSV input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--include-review", action="store_true")
    args = parser.parse_args()
    if args.count < 1:
        print("ERROR: count must be positive", file=sys.stderr)
        return 1
    try:
        content = render_handoff(load_items(args.input), args.count, args.include_review)
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
