from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_catalog_artifacts import build_summary
from generate_catalog_artifacts import conversion_coverage_rows
from generate_catalog_artifacts import expected_outputs
from generate_catalog_artifacts import render_generated_conversion_metadata
from generate_catalog_artifacts import render_generated_ffi_types
from generate_catalog_artifacts import render_generated_public_types
from generate_catalog_artifacts import render_rust_module


class CatalogGenerationTests(unittest.TestCase):
    def authoritative_inventory(self) -> set[str]:
        inventory = (ROOT / "docs" / "crates" / "units-x" / "in-scope-type-inventory.md").read_text(encoding="utf-8")
        return set(re.findall(r"^- \[[ x]\] `([^`]+)`$", inventory, flags=re.MULTILINE))

    def test_bootstrap_catalog_exists(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["catalog_version"], "0.1.0-phase-a")

    def test_generated_summary_captures_scalar_buffer_and_unit_ids(self) -> None:
        summary = json.loads((ROOT / "catalog" / "generated" / "units-catalog-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(
            summary["bridges"],
            [
                {
                    "kind": "reciprocal",
                    "left_public_type": "Distance",
                    "right_public_type": "Diopter",
                }
            ],
        )
        dimensions = {dimension["dimension_id"]: dimension for dimension in summary["dimensions"]}
        self.assertIn("distance", dimensions)
        self.assertIn("distance_i32", dimensions["distance"]["scalar"]["type_ids"])
        self.assertEqual(dimensions["distance"]["scalar"]["encoding"], "object")
        self.assertEqual(dimensions["distance"]["small_array"]["type_id_template"], "distance{arity}_{storage}")
        self.assertEqual(dimensions["distance"]["small_array"]["encoding"], "array")
        self.assertEqual(dimensions["distance"]["buffer"]["type_id_template"], "distance_buffer_{storage}")
        self.assertEqual(dimensions["distance"]["buffer"]["encoding"], "base64-le")
        self.assertIn("distance.mm", dimensions["distance"]["unit_ids"])
        self.assertEqual(dimensions["diopter"]["canonical_dimension_id"], "inverse_distance")
        self.assertIn("temperature.degC", dimensions["temperature"]["unit_ids"])
        self.assertEqual({dimension["public_type"] for dimension in summary["dimensions"]}, self.authoritative_inventory())

    def test_generation_fixture_preserves_case_reserved_alias_and_affine_units(self) -> None:
        fixture = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        summary = build_summary(fixture)
        self.assertEqual(summary["bridges"][0]["left_public_type"], "Distance")
        self.assertEqual(summary["bridges"][0]["right_public_type"], "Diopter")
        distance_units = {unit["unit_code_id"]: unit for unit in summary["dimensions"][0]["units"]}
        self.assertEqual(distance_units["mm"]["binary_unit_id"], "distance.mm")
        self.assertEqual(distance_units["Mm"]["binary_unit_id"], "distance.Mm")
        self.assertEqual(distance_units["type"]["reserved_word_alias"], "type_")
        diopter = next(dimension for dimension in summary["dimensions"] if dimension["dimension_id"] == "diopter")
        self.assertEqual(diopter["canonical_dimension_id"], "inverse_distance")

        temperature = next(dimension for dimension in summary["dimensions"] if dimension["dimension_id"] == "temperature")
        self.assertIn("temperature.degC", temperature["unit_ids"])
        self.assertIn("temperature.degF", temperature["unit_ids"])

        rendered = render_generated_public_types(summary)
        self.assertIn("pub struct mm;", rendered)
        self.assertIn("pub struct Mm;", rendered)
        self.assertIn("impl DistanceUnit for mm {}", rendered)
        self.assertIn("impl DistanceUnit for Mm {}", rendered)

    def test_render_rust_module_escapes_catalog_strings(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        catalog["dimensions"][0]["public_type"] = 'Café "Quoted" \\\\ Path'
        summary = build_summary(catalog)
        rendered = render_rust_module(summary)
        self.assertIn('public_type: "Caf\\u{e9} \\"Quoted\\" \\\\\\\\ Path"', rendered)

    def test_generated_rust_metadata_uses_typed_catalog_wrappers(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        rendered = render_rust_module(build_summary(catalog))

        self.assertIn("pub struct CatalogDimensionId(pub &'static str);", rendered)
        self.assertIn("pub enum CatalogJsonEncoding {", rendered)
        self.assertIn('dimension_id: CatalogDimensionId("distance")', rendered)
        self.assertIn('canonical_dimension_id: CatalogDimensionId("distance")', rendered)
        self.assertIn("scalar_type_ids: &[CatalogTypeId(", rendered)
        self.assertIn("scalar_encoding: CatalogJsonEncoding::Object", rendered)

    def test_generated_ffi_types_are_catalog_owned(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        rendered = render_generated_ffi_types(build_summary(catalog))

        self.assertIn("pub struct distance_mm_i32 {", rendered)
        self.assertIn("pub value_mm: i32,", rendered)
        self.assertIn("pub struct distance_mm_i32_slice {", rendered)

    def test_generated_public_types_are_catalog_owned(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        rendered = render_generated_public_types(build_summary(catalog))

        self.assertIn("pub struct mm;", rendered)
        self.assertIn("pub struct degC;", rendered)
        self.assertIn("ConvertUnit", rendered)
        self.assertIn("TryConvertQuantity", rendered)
        self.assertIn("pub trait DistanceUnit: UnitMarker {}", rendered)
        self.assertIn("impl DistanceUnit for mm {}", rendered)
        self.assertIn("pub struct Distance<Storage = f64, Unit = m>", rendered)
        self.assertIn("pub const fn mm(storage: Storage) -> Self {", rendered)
        self.assertIn("pub struct Diopter<Storage = f64, Unit = dpt>", rendered)
        self.assertIn("const CANONICAL_DIMENSION_ID: &'static str = \"inverse_distance\";", rendered)

    def test_generated_conversion_metadata_is_catalog_owned(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        rendered = render_generated_conversion_metadata(build_summary(catalog))

        self.assertIn("pub enum CatalogConversionKind {", rendered)
        self.assertIn('public_type: "Distance"', rendered)
        self.assertIn('unit_code_id: "degC"', rendered)
        self.assertIn("kind: CatalogConversionKind::Affine", rendered)
        self.assertIn('left_public_type: "Distance"', rendered)
        self.assertIn('right_public_type: "Diopter"', rendered)

    def test_conversion_coverage_report_is_complete_for_b2_scope(self) -> None:
        summary = build_summary(json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8")))
        coverage = conversion_coverage_rows(summary)

        self.assertTrue(any(row["api_surface"] == "identity" for row in coverage))
        self.assertTrue(any(row["api_surface"] == "to_unit" and row["source_public_type"] == "Distance" for row in coverage))
        self.assertTrue(any(row["path_kind"] == "same_canonical_dimension" and row["source_public_type"] == "Diopter" and row["target_public_type"] == "InverseDistance" for row in coverage))
        self.assertTrue(any(row["path_kind"] == "reciprocal_bridge" and row["source_public_type"] == "Distance" and row["target_public_type"] == "Diopter" for row in coverage))
        self.assertEqual(
            {dimension["public_type"] for dimension in summary["dimensions"]},
            {row["source_public_type"] for row in coverage},
        )

    def test_generated_public_types_reject_invalid_marker_names(self) -> None:
        summary = json.loads((ROOT / "catalog" / "generated" / "units-catalog-summary.json").read_text(encoding="utf-8"))
        summary["dimensions"][0]["units"][0]["unit_code_id"] = "m²"
        summary["dimensions"][0]["units"][0]["reserved_word_alias"] = None
        with self.assertRaises(ValueError):
            render_generated_public_types(summary)

    def test_generated_outputs_use_lf_only(self) -> None:
        for path, expected in expected_outputs().items():
            self.assertNotIn(b"\r\n", expected.encode("utf-8"))
            self.assertNotIn(b"\r\n", path.read_bytes())


if __name__ == "__main__":
    unittest.main()
