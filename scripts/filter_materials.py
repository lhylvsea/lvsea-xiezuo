#!/usr/bin/env python3
"""Apply the article-derived interaction gate to material records."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

from material_lib import load_items, metric_gate, now_utc, parse_datetime, write_json


def filter_items(items: list[dict], reference_time: datetime) -> list[dict]:
    output = []
    for item in items:
        enriched = dict(item)
        enriched.update(metric_gate(item, reference_time))
        output.append(enriched)
    return output


def build_dataset(items: list[dict], reference_time: datetime) -> dict:
    gated = filter_items(items, reference_time)
    summary = {status: sum(1 for item in gated if item["gate_status"] == status) for status in ("eligible", "local_review", "excluded")}
    return {
        "schema_version": "0.1",
        "generated_at": now_utc().isoformat(),
        "reference_time": reference_time.isoformat(),
        "criteria": {
            "within_6_hours_likes": 500,
            "after_6_hours_likes": 1000,
            "comments": 1000,
            "missing_metrics": "local_review"
        },
        "summary": {"total": len(gated), **summary},
        "items": gated
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter materials using the default interaction gate.")
    parser.add_argument("input")
    parser.add_argument("--reference-time", help="timezone-aware ISO-8601 time; defaults to current UTC")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        reference_time = parse_datetime(args.reference_time) if args.reference_time else now_utc()
        if reference_time is None:
            raise ValueError("reference time cannot be empty")
        dataset = build_dataset(load_items(args.input), reference_time)
        write_json(args.output, dataset)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(dataset["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

