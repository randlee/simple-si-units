//! Primary Rust deliverable crate for the `units-x` project.
//!
//! Phase B-1 introduces the unit-preserving scalar quantity model built from
//! the catalog-owned public type inventory.
//!
//! ```rust
//! use units_x::Distance;
//!
//! let distance = Distance::mm(1250_i32);
//! assert_eq!(distance.value(), 1250);
//! assert_eq!(distance.unit(), "mm");
//! ```
//!
//! ```rust
//! use units_x::{degC, degF, m, Distance, Temperature};
//!
//! let meters = Distance::mm(1250.0_f64).to_unit::<m>();
//! assert_eq!(meters.value(), 1.25);
//!
//! let freezing = Temperature::degC(0.0_f64).to_unit::<degF>();
//! assert!((freezing.value() - 32.0).abs() < 1.0e-9);
//! ```
//!
//! ```compile_fail
//! use units_x::{degC, mm, Distance, Temperature};
//!
//! let _ = Distance::<f64, degC>::new(1.0);
//! let _ = Temperature::<f64, mm>::new(1.0);
//! ```
//!
//! ```compile_fail
//! use units_x::conversion::ConvertUnit;
//! use units_x::{Distance, ft, mm};
//!
//! let _ = Distance::ft(1.0_f32).to_unit::<mm>();
//! ```

pub mod conversion;
pub mod ffi_contract;
pub mod generated;
pub mod model;

pub use conversion::{
    ConversionError, ConvertUnit, InfallibleUnitStorage, ReciprocalBridge, TryConvertQuantity,
    TryConvertUnit, ValueStorage,
};
pub use generated::public_types::*;
pub use model::{Quantity, QuantityType, UnitMarker};

/// Current package version exposed for scaffolding and smoke-test use.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg(test)]
mod tests {
    use super::generated::{catalog_metadata, public_types};
    use super::model::QuantityType;
    use super::{degC, degF, mm, Diopter, Distance, Quantity, Temperature, UnitMarker, VERSION};
    use core::any::TypeId;
    use core::mem::size_of;

    #[allow(non_camel_case_types)]
    struct Mm;

    #[test]
    fn version_constant_is_wired() {
        assert_eq!(VERSION, env!("CARGO_PKG_VERSION"));
    }

    #[test]
    fn generated_catalog_metadata_is_present() {
        assert!(catalog_metadata::DIMENSIONS
            .iter()
            .any(|dimension| dimension.dimension_id.as_str() == "distance"));
    }

    #[test]
    fn diopter_maps_to_inverse_distance_in_generated_metadata() {
        let diopter = catalog_metadata::DIMENSIONS
            .iter()
            .find(|dimension| dimension.public_type == "Diopter")
            .expect("Diopter metadata row must exist");
        assert_eq!(diopter.canonical_dimension_id.as_str(), "inverse_distance");
    }

    #[test]
    fn quantity_and_public_wrappers_are_zero_overhead() {
        assert_eq!(size_of::<Quantity<mm, i32>>(), size_of::<i32>());
        assert_eq!(size_of::<Distance<i32, mm>>(), size_of::<i32>());
    }

    #[test]
    fn unit_marker_types_are_case_sensitive() {
        assert_ne!(TypeId::of::<mm>(), TypeId::of::<Mm>());
        assert_eq!(<mm as UnitMarker>::UNIT_CODE_ID, "mm");
    }

    #[test]
    fn affine_temperature_markers_keep_human_symbols() {
        assert_eq!(<degC as UnitMarker>::UNIT_CODE_ID, "degC");
        assert_eq!(<degC as UnitMarker>::UNIT_SYMBOL, "C");
        assert_eq!(<degF as UnitMarker>::UNIT_CODE_ID, "degF");
        assert_eq!(<degF as UnitMarker>::UNIT_SYMBOL, "F");
        assert_ne!(TypeId::of::<degC>(), TypeId::of::<degF>());
    }

    #[test]
    fn generated_public_surface_matches_catalog_metadata() {
        let generated_rows: std::collections::BTreeSet<(&'static str, &'static str, &'static str)> =
            public_types::PUBLIC_TYPE_METADATA
                .iter()
                .map(|row| {
                    (
                        row.public_type,
                        row.dimension_id,
                        row.canonical_dimension_id,
                    )
                })
                .collect();
        let catalog_rows: std::collections::BTreeSet<(&'static str, &'static str, &'static str)> =
            catalog_metadata::DIMENSIONS
                .iter()
                .map(|row| {
                    (
                        row.public_type,
                        row.dimension_id.as_str(),
                        row.canonical_dimension_id.as_str(),
                    )
                })
                .collect();
        assert_eq!(generated_rows, catalog_rows);
        assert_eq!(
            public_types::GENERATED_PUBLIC_TYPE_COUNT,
            catalog_metadata::DIMENSIONS.len()
        );
    }

    #[test]
    fn representative_public_types_expose_metadata_and_storage() {
        let distance = Distance::mm(1250_i32);
        assert_eq!(distance.value(), 1250);
        assert_eq!(distance.unit(), "mm");
        assert_eq!(distance.unit_code_id(), "mm");
        assert_eq!(distance.dimension_id(), "distance");
        assert_eq!(distance.canonical_dimension_id(), "distance");
        assert_eq!(Distance::<i32, mm>::PUBLIC_TYPE, "Distance");
        assert_eq!(
            <Distance<i32, mm> as QuantityType>::CANONICAL_DIMENSION_ID,
            "distance"
        );

        let freezing = Temperature::degC(0.0_f64);
        assert_eq!(freezing.value(), 0.0);
        assert_eq!(freezing.unit(), "C");

        let focus = Diopter::dpt(2.0_f64);
        assert_eq!(focus.unit(), "D");
        assert_eq!(focus.canonical_dimension_id(), "inverse_distance");
    }
}
