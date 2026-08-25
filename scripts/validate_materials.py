#!/usr/bin/env python3
"""Validate an imported material dataset without network access."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from material_lib import load_items, validate_item


def validate_items(items: list[dict]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    source_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        item_errors, item_warnings = validate_item(item, index)
        errors.extend(item_errors)
        warnings.extend(item_warnings)
        source_id = str(item.get("source_id", "")).strip()
        if source_id and source_id in source_ids:
            errors.append(f"item {index}: duplicate source_id {source_id}")
        if source_id:
            source_ids.add(source_id)
    return {"valid": not errors, "count": len(items), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lvsea-xiezuo material JSON/CSV input.")
    parser.add_argument("input", help="JSON, JSONL is not accepted, or CSV material export")
    parser.add_argument("--json", action="store_true", dest="as_json", help="print machine-readable output")
    args = parser.parse_args()
    try:
        result = validate_items(load_items(args.input))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"valid": False, "count": 0, "errors": [str(exc)], "warnings": []}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"valid={result['valid']} count={result['count']} errors={len(result['errors'])} warnings={len(result['warnings'])}")
        for message in result["errors"]:
            print(f"ERROR: {message}")
        for message in result["warnings"]:
            print(f"WARN: {message}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())

