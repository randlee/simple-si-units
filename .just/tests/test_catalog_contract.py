from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent.parent


class CatalogContractTests(unittest.TestCase):
    def test_schema_and_sample_catalog_parse(self) -> None:
        schema = json.loads((ROOT / "catalog" / "schema" / "units-catalog.schema.json").read_text(encoding="utf-8"))
        sample = json.loads((ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "units-x catalog schema")
        self.assertEqual(sample["catalog_version"], "0.1.0-phase-a-sample")

    def test_sample_catalog_keeps_case_sensitive_and_offset_units_distinct(self) -> None:
        sample = json.loads((ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json").read_text(encoding="utf-8"))
        dimensions = {dimension["dimension_id"]: dimension for dimension in sample["dimensions"]}

        distance_units = {
            unit["unit_code_id"]: unit
            for unit in dimensions["distance"]["units"]
        }
        self.assertIn("mm", distance_units)
        self.assertIn("Mm", distance_units)
        self.assertNotEqual(distance_units["mm"]["binary_unit_id"], distance_units["Mm"]["binary_unit_id"])

        temperature_units = {
            unit["unit_code_id"]: unit
            for unit in dimensions["temperature"]["units"]
        }
        self.assertEqual(temperature_units["degC"]["unit_symbol"], "C")
        self.assertEqual(temperature_units["degF"]["unit_symbol"], "F")
        self.assertEqual(temperature_units["degC"]["conversion"]["kind"], "affine")
        self.assertEqual(temperature_units["degF"]["conversion"]["kind"], "affine")


if __name__ == "__main__":
    unittest.main()
