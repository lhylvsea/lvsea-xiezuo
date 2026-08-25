#!/usr/bin/env python3
"""Shared standard-library helpers for the lvsea-xiezuo data pipeline."""

# internal module: imported by the command-line scripts and tests

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1"
METRIC_FIELDS = ("likes", "comments", "saves")
CSV_ALIASES = {
    "笔记标题": "title",
    "来源链接": "source_url",
    "来源ID": "source_id",
    "搜索关键词": "keyword",
    "内容分类": "content_category",
    "素材类型": "content_type",
    "发布时间": "published_at",
    "点赞": "likes",
    "评论": "comments",
    "收藏": "saves",
    "核心矛盾": "core_conflict",
    "评论区主要观点": "comment_summary",
    "高赞评论原文": "top_comment",
    "二创价值": "remix_value",
}


def parse_datetime(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("datetime must include a timezone")
    return parsed


def as_number(value: Any) -> int | float | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a metric")
    if isinstance(value, (int, float)):
        number = value
    else:
        text = str(value).strip().replace(",", "")
        number = float(text) if "." in text else int(text)
    if not math.isfinite(float(number)) or number < 0:
        raise ValueError("metric must be a non-negative finite number")
    return number


def load_items(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if source.suffix.lower() == ".csv":
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = []
            for raw in csv.DictReader(handle):
                row: dict[str, Any] = {}
                for key, value in raw.items():
                    row[CSV_ALIASES.get(key, key)] = value
                rows.append(row)
            return rows

    payload = json.loads(source.read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict) and isinstance(payload.get("items"), list):
        items = payload["items"]
    else:
        raise ValueError("input must be a JSON array or an object with an items array")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("every item must be a JSON object")
    return [dict(item) for item in items]


def write_json(path: str | Path, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_item(item: dict[str, Any], index: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for field in ("source_id", "title", "source_url"):
        if not str(item.get(field, "")).strip():
            errors.append(f"item {index}: missing {field}")
    url = str(item.get("source_url", ""))
    if url and not (url.startswith("https://") or url.startswith("http://") or url.startswith("local:")):
        errors.append(f"item {index}: source_url must use http(s) or local:")
    if item.get("published_at") not in (None, ""):
        try:
            parse_datetime(item["published_at"])
        except (TypeError, ValueError) as exc:
            errors.append(f"item {index}: invalid published_at ({exc})")
    else:
        warnings.append(f"item {index}: missing published_at; metric gate will use local_review")
    for field in METRIC_FIELDS:
        if item.get(field) in (None, ""):
            warnings.append(f"item {index}: missing {field}; metric gate may use local_review")
            continue
        try:
            as_number(item[field])
        except ValueError as exc:
            errors.append(f"item {index}: invalid {field} ({exc})")
    if not str(item.get("keyword", "")).strip():
        warnings.append(f"item {index}: missing keyword")
    if not str(item.get("text", "")).strip():
        warnings.append(f"item {index}: missing text; analysis will be limited")
    if not str(item.get("ownership", "")).strip():
        warnings.append(f"item {index}: missing ownership; human rights review required")
    return errors, warnings


def metric_gate(item: dict[str, Any], reference_time: datetime) -> dict[str, Any]:
    published_raw = item.get("published_at")
    try:
        published = parse_datetime(published_raw)
    except (TypeError, ValueError) as exc:
        return {"gate_status": "local_review", "gate_reason": f"invalid published_at: {exc}", "age_hours": None, "metric_basis": None}

    missing = [field for field in ("likes", "comments") if item.get(field) in (None, "")]
    if published is None or missing:
        reason = "missing published_at" if published is None else "missing metrics: " + ", ".join(missing)
        return {"gate_status": "local_review", "gate_reason": reason, "age_hours": None, "metric_basis": None}

    try:
        likes = as_number(item.get("likes"))
        comments = as_number(item.get("comments"))
    except ValueError as exc:
        return {"gate_status": "local_review", "gate_reason": f"invalid metrics: {exc}", "age_hours": None, "metric_basis": None}

    age_hours = (reference_time - published).total_seconds() / 3600
    if age_hours < 0:
        return {"gate_status": "local_review", "gate_reason": "published_at is in the future", "age_hours": round(age_hours, 3), "metric_basis": None}

    if age_hours <= 6 and likes >= 500:
        return {"gate_status": "eligible", "gate_reason": "within 6h and likes >= 500", "age_hours": round(age_hours, 3), "metric_basis": "likes_6h_500"}
    if age_hours > 6 and likes >= 1000:
        return {"gate_status": "eligible", "gate_reason": "after 6h and likes >= 1000", "age_hours": round(age_hours, 3), "metric_basis": "likes_after_6h_1000"}
    if comments >= 1000:
        return {"gate_status": "eligible", "gate_reason": "comments >= 1000", "age_hours": round(age_hours, 3), "metric_basis": "comments_1000"}
    return {"gate_status": "excluded", "gate_reason": "does not meet the configured interaction threshold", "age_hours": round(age_hours, 3), "metric_basis": None}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
