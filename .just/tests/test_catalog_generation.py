from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent.parent


class CatalogGenerationTests(unittest.TestCase):
    def test_bootstrap_catalog_exists(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["catalog_version"], "0.1.0-phase-a")

    def test_generated_summary_captures_buffer_and_unit_ids(self) -> None:
        summary = json.loads((ROOT / "catalog" / "generated" / "units-catalog-summary.json").read_text(encoding="utf-8"))
        dimensions = {dimension["dimension_id"]: dimension for dimension in summary["dimensions"]}
        self.assertIn("distance", dimensions)
        self.assertEqual(dimensions["distance"]["buffer_type_id_template"], "distance_buffer_{storage}")
        self.assertIn("distance.mm", dimensions["distance"]["unit_ids"])
        self.assertIn("temperature.degC", dimensions["temperature"]["unit_ids"])


if __name__ == "__main__":
    unittest.main()
