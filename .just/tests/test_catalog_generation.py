from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_catalog_artifacts import arithmetic_support_rows
from generate_catalog_artifacts import build_summary
from generate_catalog_artifacts import bulk_support_rows
from generate_catalog_artifacts import conversion_coverage_rows
from generate_catalog_artifacts import expected_outputs
from generate_catalog_artifacts import marker_name_for_unit
from generate_catalog_artifacts import render_generated_arithmetic_impls
from generate_catalog_artifacts import render_generated_bulk_storage_impls
from generate_catalog_artifacts import render_generated_conversion_metadata
from generate_catalog_artifacts import render_generated_ffi_types
from generate_catalog_artifacts import render_generated_public_types
from generate_catalog_artifacts import render_rust_module
from generate_catalog_artifacts import scalar_storage_name


class CatalogGenerationTests(unittest.TestCase):
    def derived_inventory(self) -> set[str]:
        inventory = (ROOT / "docs" / "crates" / "units-x" / "in-scope-type-inventory.md").read_text(encoding="utf-8")
        return set(re.findall(r"^- \[[ x]\] `([^`]+)`$", inventory, flags=re.MULTILINE))

    def expected_unit_storage_impls(self, summary: dict) -> tuple[set[str], set[str]]:
        scalar_impls: set[str] = set()
        bulk_impls: set[str] = set()
        for dimension in summary["dimensions"]:
            storages = [scalar_storage_name(type_id) for type_id in dimension["scalar"]["type_ids"]]
            for unit in dimension["units"]:
                marker = marker_name_for_unit(unit)
                for storage in storages:
                    scalar_impls.add(f"impl private::SealedScalarStorageFor<{marker}> for {storage} {{}}")
                    scalar_impls.add(f"impl ScalarStorageFor<{marker}> for {storage} {{}}")
                    bulk_impls.add(f"impl private::SealedBulkStorageFor<{marker}> for {storage} {{}}")
                    bulk_impls.add(f"impl BulkStorageFor<{marker}> for {storage} {{}}")
        return scalar_impls, bulk_impls

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
        self.assertEqual(
            summary["conversion_policies"]["same_public_type"]["identity_policy_id"],
            "identity",
        )
        self.assertEqual(
            summary["conversion_policies"]["same_canonical_dimension"]["api_surface"],
            "try_to_quantity",
        )
        self.assertEqual(
            summary["conversion_policies"]["reciprocal_bridge"]["api_surface"],
            "to_reciprocal_quantity",
        )
        self.assertEqual(
            summary["arithmetic_policies"]["same_dimension_add_sub"]["storage_pair_policies"][0]["api_mode"],
            "checked",
        )
        self.assertEqual(
            summary["arithmetic_policies"]["compute_bridges"][1]["operator"],
            "acceleration_from_velocity_and_time",
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
        self.assertEqual({dimension["public_type"] for dimension in summary["dimensions"]}, self.derived_inventory())

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

    def test_generated_public_types_use_reserved_alias_for_default_unit(self) -> None:
        fixture = json.loads((ROOT / "catalog" / "examples" / "generation-edge-catalog.json").read_text(encoding="utf-8"))
        fixture["dimensions"][0]["base_unit_code_id"] = "type"
        summary = build_summary(fixture)

        rendered = render_generated_public_types(summary)
        self.assertIn("pub struct Distance<Storage = f64, Unit = type_>", rendered)

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
        summary = build_summary(catalog)
        rendered = render_generated_public_types(summary)
        expected_scalar_impls, _ = self.expected_unit_storage_impls(summary)
        actual_scalar_impls = {
            line.strip()
            for line in rendered.splitlines()
            if line.startswith("impl private::SealedScalarStorageFor<") or line.startswith("impl ScalarStorageFor<")
        }

        self.assertIn("pub struct mm;", rendered)
        self.assertIn("pub struct degC;", rendered)
        self.assertIn("ConvertUnit", rendered)
        self.assertIn("pub trait QuantityForStorage<Storage>: UnitMarker {", rendered)
        self.assertIn("impl ScalarArithmeticUnit for mm {}", rendered)
        self.assertIn("TryConvertQuantity", rendered)
        self.assertIn("pub trait DistanceUnit: UnitMarker {}", rendered)
        self.assertIn("impl DistanceUnit for mm {}", rendered)
        self.assertEqual(actual_scalar_impls, expected_scalar_impls)
        self.assertIn("pub struct Distance<Storage = f64, Unit = m>", rendered)
        self.assertIn("impl<Storage> Distance<Storage, mm>", rendered)
        self.assertIn("Storage: ScalarStorageFor<mm>,", rendered)
        self.assertIn("pub const fn mm(storage: Storage) -> Self {", rendered)
        self.assertIn("impl<Storage> QuantityForStorage<Storage> for mm", rendered)
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

    def test_generated_arithmetic_impls_are_catalog_owned(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        rendered = render_generated_arithmetic_impls(build_summary(catalog))

        self.assertIn("impl_add_sub_rule!(i32, i32 => i32, checked);", rendered)
        self.assertIn("impl_mul_rule!(f32, f64 => f64, infallible);", rendered)
        self.assertIn("impl_div_rule!(i32, f32 => f64, infallible);", rendered)
        self.assertIn("impl_same_public_type_arithmetic!(Distance, DistanceUnit);", rendered)
        self.assertIn(
            "impl_cross_public_add_sub!(Diopter, DiopterUnit, InverseDistance, InverseDistanceUnit);",
            rendered,
        )
        self.assertIn(
            "impl_cross_public_add_sub!(InverseDistance, InverseDistanceUnit, Diopter, DiopterUnit);",
            rendered,
        )
        self.assertNotIn("impl_same_public_type_arithmetic!(Temperature, TemperatureUnit);", rendered)

    def test_generated_bulk_storage_impls_are_catalog_owned(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8"))
        summary = build_summary(catalog)
        rendered = render_generated_bulk_storage_impls(summary)
        _, expected_bulk_impls = self.expected_unit_storage_impls(summary)
        actual_bulk_impls = {
            line.strip()
            for line in rendered.splitlines()
            if line.startswith("impl private::SealedBulkStorageFor<") or line.startswith("impl BulkStorageFor<")
        }

        self.assertEqual(actual_bulk_impls, expected_bulk_impls)

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
        ft_to_mm_f32 = next(
            row
            for row in coverage
            if row["source_public_type"] == "Distance"
            and row["source_unit"] == "ft"
            and row["source_storage"] == "f32"
            and row["target_public_type"] == "Distance"
            and row["target_unit"] == "mm"
            and row["target_storage"] == "f32"
        )
        self.assertEqual(ft_to_mm_f32["api_surface"], "try_to_unit")
        self.assertEqual(ft_to_mm_f32["expected_failure"], "Overflow|PrecisionLoss")

        mm_to_m_f32 = next(
            row
            for row in coverage
            if row["source_public_type"] == "Distance"
            and row["source_unit"] == "mm"
            and row["source_storage"] == "f32"
            and row["target_public_type"] == "Distance"
            and row["target_unit"] == "m"
            and row["target_storage"] == "f32"
        )
        self.assertEqual(mm_to_m_f32["api_surface"], "try_to_unit")
        self.assertEqual(mm_to_m_f32["expected_failure"], "Overflow|PrecisionLoss")

        mm_to_m_f64 = next(
            row
            for row in coverage
            if row["source_public_type"] == "Distance"
            and row["source_unit"] == "mm"
            and row["source_storage"] == "f64"
            and row["target_public_type"] == "Distance"
            and row["target_unit"] == "m"
            and row["target_storage"] == "f64"
        )
        self.assertEqual(mm_to_m_f64["api_surface"], "to_unit")
        self.assertIsNone(mm_to_m_f64["expected_failure"])

        kelvin_to_celsius_f32 = next(
            row
            for row in coverage
            if row["source_public_type"] == "Temperature"
            and row["source_unit"] == "K"
            and row["source_storage"] == "f32"
            and row["target_public_type"] == "Temperature"
            and row["target_unit"] == "degC"
            and row["target_storage"] == "f32"
        )
        self.assertEqual(kelvin_to_celsius_f32["api_surface"], "try_to_unit")
        self.assertEqual(kelvin_to_celsius_f32["expected_failure"], "Overflow|PrecisionLoss")

        reciprocal_widen = next(
            row
            for row in coverage
            if row["source_public_type"] == "Distance"
            and row["source_unit"] == "m"
            and row["source_storage"] == "f32"
            and row["target_public_type"] == "Diopter"
            and row["target_unit"] == "dpt"
            and row["target_storage"] == "f64"
        )
        self.assertEqual(reciprocal_widen["api_surface"], "to_reciprocal_quantity")
        self.assertEqual(reciprocal_widen["expected_failure"], "DomainViolation")

    def test_arithmetic_support_report_is_complete_for_b3_scope(self) -> None:
        summary = build_summary(json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8")))
        support = arithmetic_support_rows(summary)

        self.assertTrue(any(row["path_family"] == "scalar_arithmetic" and row["lhs_public_type"] == "Distance" for row in support))
        self.assertTrue(any(row["path_family"] == "same_canonical_add_sub" and row["lhs_public_type"] == "Diopter" and row["rhs_public_type"] == "InverseDistance" for row in support))
        self.assertTrue(any(row["path_family"] == "compute_bridge" and row["result_public_type"] == "Velocity" for row in support))
        self.assertTrue(any(row["lhs_public_type"] == "Temperature" and row["support_status"] == "unsupported" for row in support))
        scalar_keys = [
            (
                row["lhs_public_type"],
                row["lhs_unit"],
                row["lhs_storage"],
                row["operator"],
                row["rhs_public_type"],
                row["rhs_storage"],
            )
            for row in support
            if row["path_family"] == "scalar_arithmetic"
        ]
        self.assertEqual(len(scalar_keys), len(set(scalar_keys)))

        cross_pair = next(
            row
            for row in support
            if row["lhs_public_type"] == "Diopter"
            and row["lhs_storage"] == "f32"
            and row["operator"] == "add"
            and row["rhs_public_type"] == "InverseDistance"
            and row["rhs_storage"] == "f32"
        )
        self.assertEqual(cross_pair["api_mode"], "infallible")
        self.assertEqual(cross_pair["support_status"], "supported")
        self.assertIsNone(cross_pair["expected_failure"])

        compute_bridge = next(
            row
            for row in support
            if row["lhs_public_type"] == "Distance"
            and row["operator"] == "velocity_from_distance_and_time"
            and row["rhs_public_type"] == "Time"
        )
        self.assertEqual(compute_bridge["result_unit_code_id"], "mps")
        self.assertEqual(compute_bridge["result_storage"], "f64")
        self.assertEqual(compute_bridge["expected_failure"], "ZeroDuration")

        unsupported_add = next(
            row
            for row in support
            if row["lhs_public_type"] == "Distance"
            and row["operator"] == "add"
            and row["rhs_public_type"] == "Time"
            and row["path_family"] == "cross_dimension_non_support"
        )
        self.assertEqual(unsupported_add["api_mode"], "absent")
        self.assertEqual(unsupported_add["support_status"], "unsupported")
        self.assertEqual(unsupported_add["expected_failure"], "IntentionallyUnsupported")

        unsupported_mul = next(
            row
            for row in support
            if row["lhs_public_type"] == "Velocity"
            and row["operator"] == "mul_quantity"
            and row["rhs_public_type"] == "Time"
            and row["path_family"] == "cross_dimension_non_support"
        )
        self.assertEqual(unsupported_mul["api_mode"], "absent")

    def test_bulk_support_report_is_complete_for_b4_scope(self) -> None:
        summary = build_summary(json.loads((ROOT / "catalog" / "units-catalog.json").read_text(encoding="utf-8")))
        support = bulk_support_rows(summary)
        expected_rows = []
        review_arities = {0, 2, 3, 4}
        for dimension in summary["dimensions"]:
            storages = {type_id.rsplit("_", maxsplit=1)[1] for type_id in dimension["scalar"]["type_ids"]}
            for storage in storages:
                for arity in review_arities:
                    expected_rows.append(
                        (
                            dimension["public_type"],
                            "array",
                            arity,
                            storage,
                            dimension["small_array"]["encoding"],
                            "supported",
                            None,
                        )
                    )
                expected_rows.append(
                    (
                        dimension["public_type"],
                        "buffer",
                        None,
                        storage,
                        dimension["buffer"]["encoding"],
                        "supported",
                        None,
                    )
                )
                expected_rows.append(
                    (
                        dimension["public_type"],
                        "buffer_view",
                        None,
                        storage,
                        dimension["buffer"]["encoding"],
                        "supported",
                        None,
                    )
                )

        actual_rows = [
            (
                row["public_type"],
                row["bulk_kind"],
                row["array_arity"],
                row["storage"],
                row["classification"],
                row["support_status"],
                row["expected_failure"],
            )
            for row in support
        ]
        self.assertEqual(len(actual_rows), len(set(actual_rows)))
        self.assertEqual(set(actual_rows), set(expected_rows))
        self.assertEqual(
            {row["array_arity"] for row in support if row["bulk_kind"] == "array"},
            review_arities,
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
