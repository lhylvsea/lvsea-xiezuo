from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_rewrite_brief import render_brief  # noqa: E402
from build_writing_handoff import render_handoff  # noqa: E402
from export_feishu_csv import export_rows  # noqa: E402
from filter_materials import build_dataset  # noqa: E402
from material_lib import load_items  # noqa: E402
from validate_materials import validate_items  # noqa: E402


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = ROOT / "tests/fixtures/demo-materials.json"
        cls.reference_time = datetime.fromisoformat("2026-08-25T12:00:00+08:00")
        cls.items = load_items(cls.fixture)

    def test_fixture_is_valid_with_review_warnings(self) -> None:
        result = validate_items(self.items)
        self.assertTrue(result["valid"])
        self.assertEqual(result["count"], 4)
        self.assertGreaterEqual(len(result["warnings"]), 3)

    def test_metric_gate_counts(self) -> None:
        dataset = build_dataset(self.items, self.reference_time)
        self.assertEqual(dataset["summary"], {"total": 4, "eligible": 2, "local_review": 1, "excluded": 1})
        statuses = {item["source_id"]: item["gate_status"] for item in dataset["items"]}
        self.assertEqual(statuses["demo-eligible-hot"], "eligible")
        self.assertEqual(statuses["demo-eligible-comments"], "eligible")
        self.assertEqual(statuses["demo-review-missing"], "local_review")
        self.assertEqual(statuses["demo-excluded"], "excluded")

    def test_export_defaults_to_eligible(self) -> None:
        dataset = build_dataset(self.items, self.reference_time)
        rows, counts = export_rows(dataset["items"])
        self.assertEqual(counts["exported"], 2)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "半天内出现大量讨论的冷门生意")

    def test_brief_is_source_backed_and_does_not_fill_review(self) -> None:
        dataset = build_dataset(self.items, self.reference_time)
        brief = render_brief(dataset["items"], count=3)
        self.assertIn("source_basis", brief)
        self.assertIn("demo-eligible-hot", brief)
        self.assertNotIn("demo-review-missing", brief)
        self.assertIn("missing_evidence", brief)

    def test_writing_handoff_is_source_backed_and_stops_before_prose(self) -> None:
        dataset = build_dataset(self.items, self.reference_time)
        handoff = render_handoff(dataset["items"], count=3)
        self.assertIn("lvsea-writing", handoff)
        self.assertIn("source_basis", handoff)
        self.assertIn("main_claim_candidate", handoff)
        self.assertNotIn("demo-review-missing", handoff)
        self.assertIn("不是成稿", handoff)

    def test_csv_roundtrip_is_utf8_and_has_headers(self) -> None:
        dataset = build_dataset(self.items, self.reference_time)
        rows, _ = export_rows(dataset["items"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle, lineterminator="\n")
                writer.writerow(["笔记标题", "来源链接"])
                writer.writerows([[row[0], row[1]] for row in rows])
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
            self.assertIn("笔记标题", path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
