#!/usr/bin/env python3
"""Export eligible material records as a reviewable Feishu-compatible CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

from material_lib import load_items

HEADERS = [
    "笔记标题", "来源链接", "来源ID", "搜索关键词", "内容分类", "素材类型", "发布时间",
    "点赞", "评论", "收藏", "指标门禁", "门禁理由", "证据状态", "核心矛盾",
    "评论区主要观点", "高赞评论原文", "二创价值", "本地图片", "同步状态"
]
FIELDS = [
    "title", "source_url", "source_id", "keyword", "content_category", "content_type", "published_at",
    "likes", "comments", "saves", "gate_status", "gate_reason", "evidence_status", "core_conflict",
    "comment_summary", "top_comment", "remix_value", "images", "sync_status"
]


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        text = " | ".join(str(part) for part in value)
    elif isinstance(value, dict):
        text = "; ".join(f"{key}={value[key]}" for key in sorted(value))
    else:
        text = str(value)
    if text[:1] in "=+-@":
        return "'" + text
    return text


def make_row(item: dict[str, Any]) -> list[str]:
    row = dict(item)
    row.setdefault("evidence_status", "missing_evidence" if not item.get("text") else "observed_only")
    row.setdefault("sync_status", "not_synced")
    return [cell(row.get(field)) for field in FIELDS]


def export_rows(items: list[dict[str, Any]], include_review: bool = False, include_excluded: bool = False) -> tuple[list[list[str]], dict[str, int]]:
    allowed = {"eligible"}
    if include_review:
        allowed.add("local_review")
    if include_excluded:
        allowed.add("excluded")
    counts = {"eligible": 0, "local_review": 0, "excluded": 0, "unscreened": 0, "exported": 0}
    rows = []
    for item in items:
        status = str(item.get("gate_status") or "unscreened")
        counts[status] = counts.get(status, 0) + 1
        if status in allowed:
            rows.append(make_row(item))
            counts["exported"] += 1
    return rows, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Export eligible materials as Feishu-compatible CSV.")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--include-review", action="store_true", help="include local_review rows for manual review")
    parser.add_argument("--include-excluded", action="store_true", help="include excluded rows for audit")
    args = parser.parse_args()
    try:
        rows, counts = export_rows(load_items(args.input), args.include_review, args.include_excluded)
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(HEADERS)
            writer.writerows(rows)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"exported={counts['exported']} eligible={counts.get('eligible', 0)} local_review={counts.get('local_review', 0)} excluded={counts.get('excluded', 0)} unscreened={counts.get('unscreened', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

