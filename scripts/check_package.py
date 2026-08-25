#!/usr/bin/env python3
"""Run a dependency-free structural and secret hygiene check for this package."""

# internal module: package gate entrypoint

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "README.md", "LICENSE", "agents/interface.yaml", "manifest.json", "evals/trigger_cases.json"]
SECRET_PATTERNS = [re.compile(r"gho_[A-Za-z0-9]{12,}"), re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), re.compile(r"sk-[A-Za-z0-9]{20,}")]


def main() -> int:
    failures: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            failures.append(f"missing {relative}")
    discoverable_skill_files = [
        path for path in ROOT.rglob("SKILL.md")
        if ".git" not in path.relative_to(ROOT).parts and path.relative_to(ROOT).parts[:1] != ("work",) and "__pycache__" not in path.relative_to(ROOT).parts
    ]
    if len(discoverable_skill_files) != 1:
        failures.append("package must contain exactly one discoverable SKILL.md")
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        evals = json.loads((ROOT / "evals/trigger_cases.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON: {exc}")
        manifest, evals = {}, {}
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").is_file() else ""
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    interface_text = (ROOT / "agents/interface.yaml").read_text(encoding="utf-8") if (ROOT / "agents/interface.yaml").is_file() else ""
    if not skill_text.startswith("---\n") or "name: lvsea-xiezuo" not in skill_text:
        failures.append("SKILL.md frontmatter is missing or mismatched")
    if manifest.get("name") != "lvsea-xiezuo" or manifest.get("version") != "0.1.0":
        failures.append("manifest name/version mismatch")
    for marker in ("display_name:", "short_description:", "default_prompt:", "examples:"):
        if marker not in interface_text:
            failures.append(f"interface missing {marker}")
    for marker in ("安装", "最短可运行路径", "四个实际场景", "权限、隐私与限制"):
        if marker not in readme_text:
            failures.append(f"README missing {marker}")
    for group in ("should_trigger", "should_not_trigger", "near_neighbor", "adversarial"):
        if not isinstance(evals.get(group), list) or not evals[group]:
            failures.append(f"trigger eval group missing: {group}")
    scan_paths = [
        path for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts and path.relative_to(ROOT).parts[:1] != ("work",) and "__pycache__" not in path.relative_to(ROOT).parts and path.suffix.lower() not in {".pyc", ".pyo"} and path.name != "check_package.py"
    ]
    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in scan_paths)
    for pattern in SECRET_PATTERNS:
        if pattern.search(all_text):
            failures.append(f"secret-like pattern detected: {pattern.pattern}")
    windows_abs_marker = "C:" + "\\" + "Users" + "\\"
    windows_forward_marker = "C:" + "/" + "Users" + "/"
    for path in scan_paths:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if path.is_file() and (windows_abs_marker in content or windows_forward_marker in content):
            failures.append(f"absolute Windows path found in {path.relative_to(ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: package structure, trigger groups, README markers, and secret hygiene")
    return 0


if __name__ == "__main__":
    sys.exit(main())
