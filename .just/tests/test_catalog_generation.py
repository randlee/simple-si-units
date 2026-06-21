from __future__ import annotations

import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_catalog_artifacts import build_summary
from generate_catalog_artifacts import render_rust_module


class CatalogGenerationTests(unittest.TestCase):
    def test_bootstrap_catalog_exists(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["catalog_version"], "0.1.0-phase-a")

    def test_generated_summary_captures_scalar_buffer_and_unit_ids(self) -> None:
        summary = json.loads((ROOT / "catalog" / "generated" / "units-catalog-summary.json").read_text(encoding="utf-8"))
        dimensions = {dimension["dimension_id"]: dimension for dimension in summary["dimensions"]}
        self.assertIn("distance", dimensions)
        self.assertIn("distance_i32", dimensions["distance"]["scalar_type_ids"])
        self.assertEqual(dimensions["distance"]["small_array_type_id_template"], "distance{arity}_{storage}")
        self.assertEqual(dimensions["distance"]["buffer_type_id_template"], "distance_buffer_{storage}")
        self.assertIn("distance.mm", dimensions["distance"]["unit_ids"])
        self.assertIn("temperature.degC", dimensions["temperature"]["unit_ids"])

    def test_generation_fixture_preserves_case_reserved_alias_and_affine_units(self) -> None:
        fixture = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        summary = build_summary(fixture)
        distance_units = {unit["unit_code_id"]: unit for unit in summary["dimensions"][0]["units"]}
        self.assertEqual(distance_units["mm"]["binary_unit_id"], "distance.mm")
        self.assertEqual(distance_units["Mm"]["binary_unit_id"], "distance.Mm")
        self.assertEqual(distance_units["type"]["reserved_word_alias"], "type_")

        temperature = next(dimension for dimension in summary["dimensions"] if dimension["dimension_id"] == "temperature")
        self.assertIn("temperature.degC", temperature["unit_ids"])
        self.assertIn("temperature.degF", temperature["unit_ids"])

    def test_render_rust_module_escapes_catalog_strings(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        catalog["dimensions"][0]["public_type"] = 'Distance "Quoted" \\\\ Path'
        summary = build_summary(catalog)
        rendered = render_rust_module(summary)
        self.assertIn('public_type: "Distance \\"Quoted\\" \\\\\\\\ Path"', rendered)


if __name__ == "__main__":
    unittest.main()
