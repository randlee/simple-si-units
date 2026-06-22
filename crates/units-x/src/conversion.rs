use crate::generated::conversion_metadata::{
    CatalogConversionKind, GeneratedUnitConversionMetadata, BRIDGES, UNIT_CONVERSIONS,
};
use crate::model::{Quantity, QuantityType, UnitMarker};

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum ConversionError {
    IncompatibleCanonicalDimension,
    UnsupportedBridge,
    MissingCatalogPath,
    DomainViolation,
    Overflow,
    PrecisionLoss,
}

pub trait ConvertUnit<TargetUnit> {
    type Output;

    fn to_unit(self) -> Self::Output;
}

pub trait TryConvertUnit<TargetUnit, TargetStorage> {
    type Output;

    fn try_to_unit(self) -> Result<Self::Output, ConversionError>;
}

pub trait TryConvertQuantity<TargetQuantity, TargetUnit, TargetStorage> {
    fn try_to_quantity(self) -> Result<TargetQuantity, ConversionError>;
}

pub trait ReciprocalBridge<TargetQuantity, TargetUnit, TargetStorage> {
    fn to_reciprocal_quantity(self) -> Result<TargetQuantity, ConversionError>;
}

pub trait ValueStorage: Copy + 'static {
    fn to_f64(self) -> f64;
    fn try_from_f64(value: f64) -> Result<Self, ConversionError>;
}

pub trait InfallibleUnitStorage: ValueStorage {
    fn from_f64_infallible(value: f64) -> Self;
}

impl ValueStorage for f64 {
    fn to_f64(self) -> f64 {
        self
    }

    fn try_from_f64(value: f64) -> Result<Self, ConversionError> {
        Ok(value)
    }
}

impl InfallibleUnitStorage for f64 {
    fn from_f64_infallible(value: f64) -> Self {
        value
    }
}

impl ValueStorage for f32 {
    fn to_f64(self) -> f64 {
        f64::from(self)
    }

    fn try_from_f64(value: f64) -> Result<Self, ConversionError> {
        if value.is_nan() {
            return Ok(f32::NAN);
        }
        if !value.is_finite() || value > f32::MAX as f64 || value < f32::MIN as f64 {
            return Err(ConversionError::Overflow);
        }
        let narrowed = value as f32;
        if f64::from(narrowed) == value {
            Ok(narrowed)
        } else {
            Err(ConversionError::PrecisionLoss)
        }
    }
}

impl InfallibleUnitStorage for f32 {
    fn from_f64_infallible(value: f64) -> Self {
        value as f32
    }
}

impl ValueStorage for i32 {
    fn to_f64(self) -> f64 {
        f64::from(self)
    }

    fn try_from_f64(value: f64) -> Result<Self, ConversionError> {
        if !value.is_finite() {
            return Err(ConversionError::Overflow);
        }
        if value < i32::MIN as f64 || value > i32::MAX as f64 {
            return Err(ConversionError::Overflow);
        }
        let truncated = value.trunc();
        if truncated != value {
            return Err(ConversionError::PrecisionLoss);
        }
        Ok(truncated as i32)
    }
}

pub fn convert_same_public_type_infallible<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> TargetQuantity
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: InfallibleUnitStorage,
    TargetQuantity: QuantityType<Storage = SourceQuantity::Storage>,
{
    let source_meta = lookup_unit_metadata(
        SourceQuantity::PUBLIC_TYPE,
        <SourceQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .expect("generated source unit metadata must exist");
    let target_meta = lookup_unit_metadata(
        TargetQuantity::PUBLIC_TYPE,
        <TargetQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .expect("generated target unit metadata must exist");
    let base_value = to_base_value(source.quantity().storage.to_f64(), source_meta);
    let converted_value = from_base_value(base_value, target_meta);
    TargetQuantity::from_quantity(Quantity::new(
        <SourceQuantity::Storage as InfallibleUnitStorage>::from_f64_infallible(converted_value),
    ))
}

pub fn try_convert_same_public_type<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> Result<TargetQuantity, ConversionError>
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: ValueStorage,
{
    if SourceQuantity::PUBLIC_TYPE != TargetQuantity::PUBLIC_TYPE {
        return Err(ConversionError::MissingCatalogPath);
    }
    convert_via_catalog::<SourceQuantity, TargetQuantity>(source)
}

pub fn try_convert_quantity<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> Result<TargetQuantity, ConversionError>
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: ValueStorage,
{
    if SourceQuantity::CANONICAL_DIMENSION_ID != TargetQuantity::CANONICAL_DIMENSION_ID {
        return Err(ConversionError::IncompatibleCanonicalDimension);
    }
    convert_via_catalog::<SourceQuantity, TargetQuantity>(source)
}

pub fn try_convert_reciprocal<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> Result<TargetQuantity, ConversionError>
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: ValueStorage,
{
    if !supports_reciprocal_bridge(SourceQuantity::PUBLIC_TYPE, TargetQuantity::PUBLIC_TYPE) {
        return Err(ConversionError::UnsupportedBridge);
    }
    let source_meta = lookup_unit_metadata(
        SourceQuantity::PUBLIC_TYPE,
        <SourceQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .ok_or(ConversionError::MissingCatalogPath)?;
    let target_meta = lookup_unit_metadata(
        TargetQuantity::PUBLIC_TYPE,
        <TargetQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .ok_or(ConversionError::MissingCatalogPath)?;
    let base_value = to_base_value(source.quantity().storage.to_f64(), source_meta);
    if base_value == 0.0 {
        return Err(ConversionError::DomainViolation);
    }
    let reciprocal_value = 1.0 / base_value;
    let converted_value = from_base_value(reciprocal_value, target_meta);
    let target_storage = <TargetQuantity::Storage as ValueStorage>::try_from_f64(converted_value)?;
    Ok(TargetQuantity::from_quantity(Quantity::new(target_storage)))
}

fn convert_via_catalog<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> Result<TargetQuantity, ConversionError>
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: ValueStorage,
{
    let source_meta = lookup_unit_metadata(
        SourceQuantity::PUBLIC_TYPE,
        <SourceQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .ok_or(ConversionError::MissingCatalogPath)?;
    let target_meta = lookup_unit_metadata(
        TargetQuantity::PUBLIC_TYPE,
        <TargetQuantity::Unit as UnitMarker>::UNIT_CODE_ID,
    )
    .ok_or(ConversionError::MissingCatalogPath)?;
    let base_value = to_base_value(source.quantity().storage.to_f64(), source_meta);
    let converted_value = from_base_value(base_value, target_meta);
    let target_storage = <TargetQuantity::Storage as ValueStorage>::try_from_f64(converted_value)?;
    Ok(TargetQuantity::from_quantity(Quantity::new(target_storage)))
}

fn lookup_unit_metadata(
    public_type: &str,
    unit_code_id: &str,
) -> Option<&'static GeneratedUnitConversionMetadata> {
    UNIT_CONVERSIONS
        .iter()
        .find(|row| row.public_type == public_type && row.unit_code_id == unit_code_id)
}

fn supports_reciprocal_bridge(source_public_type: &str, target_public_type: &str) -> bool {
    BRIDGES.iter().any(|bridge| {
        bridge.kind == "reciprocal"
            && ((bridge.left_public_type == source_public_type
                && bridge.right_public_type == target_public_type)
                || (bridge.left_public_type == target_public_type
                    && bridge.right_public_type == source_public_type))
    })
}

fn to_base_value(value: f64, metadata: &GeneratedUnitConversionMetadata) -> f64 {
    match metadata.kind {
        CatalogConversionKind::Linear => value * metadata.scale_to_base,
        CatalogConversionKind::Affine => {
            value * metadata.scale_to_base + metadata.offset_to_base.unwrap_or(0.0)
        }
    }
}

fn from_base_value(base_value: f64, metadata: &GeneratedUnitConversionMetadata) -> f64 {
    match metadata.kind {
        CatalogConversionKind::Linear => base_value / metadata.scale_to_base,
        CatalogConversionKind::Affine => {
            (base_value - metadata.offset_to_base.unwrap_or(0.0)) / metadata.scale_to_base
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::conversion_metadata;
    use crate::generated::public_types::{
        degC, degF, dpt, ft, m, mm, per_m, s, Diopter, Distance, InverseDistance, Temperature, Time,
    };
    use crate::model::{private, Quantity, QuantityType, UnitMarker};

    fn assert_close(left: f64, right: f64) {
        assert!((left - right).abs() < 1.0e-9, "left={left}, right={right}");
    }

    #[derive(Copy, Clone, Debug, PartialEq, Eq)]
    struct FakeUnit;

    impl private::SealedUnit for FakeUnit {}

    impl UnitMarker for FakeUnit {
        const UNIT_SYMBOL: &'static str = "fake";
        const UNIT_CODE_ID: &'static str = "fake";
        const DIMENSION_ID: &'static str = "fake_distance";
        const CANONICAL_DIMENSION_ID: &'static str = "distance";
        const PUBLIC_TYPE: &'static str = "Distance";
    }

    #[derive(Copy, Clone, Debug, PartialEq)]
    struct FakeQuantity {
        quantity: Quantity<FakeUnit, f64>,
    }

    impl private::SealedQuantityType for FakeQuantity {}

    impl QuantityType for FakeQuantity {
        type Storage = f64;
        type Unit = FakeUnit;

        const PUBLIC_TYPE: &'static str = "Distance";
        const DIMENSION_ID: &'static str = "fake_distance";
        const CANONICAL_DIMENSION_ID: &'static str = "distance";

        fn from_quantity(quantity: Quantity<Self::Unit, Self::Storage>) -> Self {
            Self { quantity }
        }

        fn quantity(&self) -> &Quantity<Self::Unit, Self::Storage> {
            &self.quantity
        }

        fn quantity_mut(&mut self) -> &mut Quantity<Self::Unit, Self::Storage> {
            &mut self.quantity
        }

        fn into_quantity(self) -> Quantity<Self::Unit, Self::Storage> {
            self.quantity
        }
    }

    #[test]
    fn unit_conversion_metadata_is_generated() {
        assert!(conversion_metadata::UNIT_CONVERSIONS
            .iter()
            .any(|row| row.public_type == "Distance" && row.unit_code_id == "ft"));
        assert!(conversion_metadata::BRIDGES.iter().any(|row| {
            row.left_public_type == "Distance" && row.right_public_type == "Diopter"
        }));
    }

    #[test]
    fn distance_round_trip_mm_to_m_and_back() {
        let meters = Distance::mm(1250.0_f64).to_unit::<m>();
        assert_eq!(meters.value(), 1.25);
        let millimeters = meters.to_unit::<mm>();
        assert_eq!(millimeters.value(), 1250.0);
    }

    #[test]
    fn distance_round_trip_ft_to_m_and_back() {
        let meters = Distance::ft(3.280839895013123_f64).to_unit::<m>();
        assert_close(meters.value(), 1.0);
        let feet = meters.to_unit::<ft>();
        assert_close(feet.value(), 3.280839895013123);
    }

    #[test]
    fn temperature_offsets_are_correct() {
        let freezing = Temperature::degC(0.0_f64).to_unit::<degF>();
        assert_close(freezing.value(), 32.0);
        let boiling = Temperature::degF(212.0_f64).to_unit::<degC>();
        assert_close(boiling.value(), 100.0);
        let below_zero = Temperature::degF(-40.0_f64).to_unit::<degC>();
        assert_close(below_zero.value(), -40.0);
    }

    #[test]
    fn unit_symbols_keep_human_readable_temperature_codes() {
        assert_eq!(Temperature::degC(0.0_f64).unit(), "C");
        assert_eq!(Temperature::degF(0.0_f64).unit(), "F");
    }

    #[test]
    fn lossy_integer_conversion_is_rejected() {
        let error = Distance::mm(1_i32).try_to_unit::<m, i32>().unwrap_err();
        assert_eq!(error, ConversionError::PrecisionLoss);
    }

    #[test]
    fn same_canonical_dimension_cross_public_type_conversion_works() {
        let inverse = Diopter::dpt(2.0_f64)
            .try_to_quantity::<InverseDistance<f64, per_m>, per_m, f64>()
            .unwrap();
        assert_eq!(inverse.value(), 2.0);
        assert_eq!(inverse.canonical_dimension_id(), "inverse_distance");

        let diopter = InverseDistance::per_m(2.0_f64)
            .try_to_quantity::<Diopter<f64, dpt>, dpt, f64>()
            .unwrap();
        assert_eq!(diopter.value(), 2.0);
        assert_eq!(diopter.canonical_dimension_id(), "inverse_distance");
    }

    #[test]
    fn reciprocal_bridge_between_distance_and_diopter_works() {
        let diopter = Distance::m(0.5_f64)
            .to_reciprocal_quantity::<Diopter<f64, dpt>, dpt, f64>()
            .unwrap();
        assert_eq!(diopter.value(), 2.0);

        let distance = Diopter::dpt(2.0_f64)
            .to_reciprocal_quantity::<Distance<f64, m>, m, f64>()
            .unwrap();
        assert_eq!(distance.value(), 0.5);
    }

    #[test]
    fn incompatible_canonical_dimensions_are_rejected() {
        let error = Distance::m(1.0_f64)
            .try_to_quantity::<Time<f64, s>, s, f64>()
            .unwrap_err();
        assert_eq!(error, ConversionError::IncompatibleCanonicalDimension);
    }

    #[test]
    fn unsupported_bridge_is_rejected() {
        let error = Time::s(1.0_f64)
            .to_reciprocal_quantity::<Diopter<f64, dpt>, dpt, f64>()
            .unwrap_err();
        assert_eq!(error, ConversionError::UnsupportedBridge);
    }

    #[test]
    fn zero_distance_reciprocal_is_a_domain_violation() {
        let error = Distance::m(0.0_f64)
            .to_reciprocal_quantity::<Diopter<f64, dpt>, dpt, f64>()
            .unwrap_err();
        assert_eq!(error, ConversionError::DomainViolation);
    }

    #[test]
    fn overflow_is_reported_for_narrow_integer_targets() {
        let error = Distance::ft(f64::MAX).try_to_unit::<mm, i32>().unwrap_err();
        assert_eq!(error, ConversionError::Overflow);
    }

    #[test]
    fn missing_catalog_path_is_reported_for_fake_units() {
        let error =
            try_convert_same_public_type::<Distance<f64, mm>, FakeQuantity>(Distance::mm(1.0))
                .unwrap_err();
        assert_eq!(error, ConversionError::MissingCatalogPath);
    }

    #[test]
    fn i32_to_f32_storage_changes_are_explicitly_fallible() {
        let error = Distance::m(i32::MAX).try_to_unit::<m, f32>().unwrap_err();
        assert_eq!(error, ConversionError::PrecisionLoss);
    }
}
