from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from validate_catalog_contract import ValidationError
from validate_catalog_contract import validate_catalog


ROOT = Path(__file__).resolve().parent.parent.parent


class CatalogContractTests(unittest.TestCase):
    def load_sample(self) -> dict:
        return json.loads((ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json").read_text(encoding="utf-8"))

    def test_schema_and_sample_catalog_parse(self) -> None:
        schema = json.loads((ROOT / "catalog" / "schema" / "units-catalog.schema.json").read_text(encoding="utf-8"))
        sample = self.load_sample()
        self.assertEqual(schema["title"], "units-x catalog schema")
        self.assertEqual(sample["catalog_version"], "0.1.0-phase-a-sample")
        self.assertEqual(
            schema["$defs"]["dimension"]["properties"]["family"]["enum"],
            ["base", "geometry", "mechanical", "electromagnetic"],
        )
        self.assertIn("canonical_dimension_id", schema["$defs"]["dimension"]["required"])
        conversion = schema["$defs"]["conversion"]
        self.assertIn("allOf", conversion)
        unit_required = set(schema["$defs"]["unit"]["required"])
        self.assertTrue({"reserved_word_alias", "aliases", "conversion"}.issubset(unit_required))

    def test_sample_catalog_passes_contract_validation(self) -> None:
        validate_catalog(self.load_sample())

    def test_production_catalog_passes_contract_validation(self) -> None:
        payload = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        validate_catalog(payload)

    def test_generation_edge_fixture_passes_contract_validation(self) -> None:
        payload = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        validate_catalog(payload)

    def test_sample_catalog_keeps_case_sensitive_and_offset_units_distinct(self) -> None:
        sample = self.load_sample()
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
        self.assertEqual(dimensions["diopter"]["canonical_dimension_id"], "inverse_distance")
        self.assertEqual(temperature_units["degC"]["unit_symbol"], "C")
        self.assertEqual(temperature_units["degF"]["unit_symbol"], "F")
        self.assertEqual(temperature_units["degC"]["conversion"]["kind"], "affine")
        self.assertEqual(temperature_units["degF"]["conversion"]["kind"], "affine")

    def test_contract_validation_rejects_duplicate_and_invalid_conversion_data(self) -> None:
        sample = self.load_sample()
        sample["dimensions"][0]["units"].append(dict(sample["dimensions"][0]["units"][0]))
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        temperature = next(dimension for dimension in sample["dimensions"] if dimension["dimension_id"] == "temperature")
        temperature["units"][1]["conversion"]["offset_to_base"] = None
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["base_unit_code_id"] = "km"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["json_forms"]["scalar"]["type_ids"] = ["distance_f32", "distance_f64"]
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][2]["canonical_dimension_id"] = "no_such_dimension"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["unit_code_id"] = "type"
        sample["dimensions"][0]["units"][0]["binary_unit_id"] = "distance.type"
        sample["dimensions"][0]["units"][0]["reserved_word_alias"] = None
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["unit_code_id"] = "m²"
        sample["dimensions"][0]["units"][0]["binary_unit_id"] = "distance.m²"
        sample["dimensions"][0]["units"][0]["reserved_word_alias"] = None
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["unit_code_id"] = "m-m"
        sample["dimensions"][0]["units"][0]["binary_unit_id"] = "distance.m-m"
        sample["dimensions"][0]["units"][0]["reserved_word_alias"] = "m_m"
        sample["dimensions"][0]["units"][1]["unit_code_id"] = "m/m"
        sample["dimensions"][0]["units"][1]["binary_unit_id"] = "distance.m/m"
        sample["dimensions"][0]["units"][1]["reserved_word_alias"] = "m_m"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["reserved_word_alias"] = "shared_marker"
        sample["dimensions"][1]["units"][0]["reserved_word_alias"] = "shared_marker"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["unexpected"] = True
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["unexpected"] = "value"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["json_forms"]["scalar"]["type_ids"] = []
        with self.assertRaises(ValidationError) as context:
            validate_catalog(sample)
        self.assertEqual(context.exception.code, "schema_validation_failed")

        sample = self.load_sample()
        sample["dimensions"][0]["dimension_id"] = "   "
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][2]["units"][0]["display_name"] = "   "
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["reserved_word_alias"] = ""
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["binary_unit_id"] = "   "
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

        sample = self.load_sample()
        sample["dimensions"][0]["units"][0]["binary_unit_id"] = "distance.centimeter"
        with self.assertRaises(ValidationError):
            validate_catalog(sample)

    def test_validator_cli_emits_machine_readable_envelope_for_file_errors(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-catalog-cli-") as tmpdir:
            tmpdir_path = Path(tmpdir)
            missing = tmpdir_path / "missing.json"
            malformed = tmpdir_path / "malformed.json"
            malformed.write_text("{ invalid json", encoding="utf-8", newline="\n")

            missing_run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_catalog_contract.py"), str(missing)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(missing_run.returncode, 1)
            missing_envelope = json.loads(missing_run.stderr.strip())
            self.assertEqual(missing_envelope["code"], "catalog_read_failed")

            malformed_run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_catalog_contract.py"), str(malformed)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(malformed_run.returncode, 1)
            malformed_envelope = json.loads(malformed_run.stderr.strip())
            self.assertEqual(malformed_envelope["code"], "catalog_json_decode_failed")


if __name__ == "__main__":
    unittest.main()
