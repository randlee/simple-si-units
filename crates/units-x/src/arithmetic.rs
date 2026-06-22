use crate::conversion::{from_base_value, lookup_unit_metadata, to_base_value, ValueStorage};
use crate::generated::public_types::*;
use crate::model::{Quantity, QuantityType, UnitMarker};
use core::ops::{Add, Div, Mul, Sub};

mod private {
    pub trait SealedArithmeticPolicy {}
    pub trait SealedArithmeticStorage {}
}

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum ArithmeticError {
    DivisionByZero,
    NonIntegralDivision,
    Overflow,
    PrecisionLoss,
}

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum ComputeError {
    ZeroDuration,
}

pub trait AddSubPromotion<Rhs>: private::SealedArithmeticPolicy + ValueStorage {
    type Output: ValueStorage;
}

pub trait InfallibleAddSubPromotion<Rhs>: AddSubPromotion<Rhs> {}
pub trait CheckedAddSubPromotion<Rhs>: AddSubPromotion<Rhs> {}

pub trait MulPromotion<Rhs>: private::SealedArithmeticPolicy + ValueStorage {
    type Output: ValueStorage;
}

pub trait InfallibleMulPromotion<Rhs>: MulPromotion<Rhs> {}
pub trait CheckedMulPromotion<Rhs>: MulPromotion<Rhs> {}

pub trait DivPromotion<Rhs>: private::SealedArithmeticPolicy + ValueStorage {
    type Output: ValueStorage;
}

pub trait InfallibleDivPromotion<Rhs>: DivPromotion<Rhs> {}
pub trait CheckedDivPromotion<Rhs>: DivPromotion<Rhs> {}

pub trait CheckedArithmeticStorage: private::SealedArithmeticStorage + ValueStorage {
    fn from_f64_for_arithmetic(value: f64) -> Result<Self, ArithmeticError>;
    fn checked_add(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_sub(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_mul(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_div(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
}

pub trait InfallibleArithmeticStorage: ValueStorage {
    fn from_f64_for_arithmetic_infallible(value: f64) -> Self;
    fn add_infallible(lhs: Self, rhs: Self) -> Self;
    fn sub_infallible(lhs: Self, rhs: Self) -> Self;
    fn mul_infallible(lhs: Self, rhs: Self) -> Self;
    fn div_infallible(lhs: Self, rhs: Self) -> Self;
}

impl private::SealedArithmeticPolicy for f64 {}
impl private::SealedArithmeticPolicy for f32 {}
impl private::SealedArithmeticPolicy for i32 {}

impl private::SealedArithmeticStorage for f64 {}
impl private::SealedArithmeticStorage for f32 {}
impl private::SealedArithmeticStorage for i32 {}

impl InfallibleArithmeticStorage for f64 {
    fn from_f64_for_arithmetic_infallible(value: f64) -> Self {
        value
    }

    fn add_infallible(lhs: Self, rhs: Self) -> Self {
        lhs + rhs
    }

    fn sub_infallible(lhs: Self, rhs: Self) -> Self {
        lhs - rhs
    }

    fn mul_infallible(lhs: Self, rhs: Self) -> Self {
        lhs * rhs
    }

    fn div_infallible(lhs: Self, rhs: Self) -> Self {
        lhs / rhs
    }
}

impl InfallibleArithmeticStorage for f32 {
    fn from_f64_for_arithmetic_infallible(value: f64) -> Self {
        value as f32
    }

    fn add_infallible(lhs: Self, rhs: Self) -> Self {
        lhs + rhs
    }

    fn sub_infallible(lhs: Self, rhs: Self) -> Self {
        lhs - rhs
    }

    fn mul_infallible(lhs: Self, rhs: Self) -> Self {
        lhs * rhs
    }

    fn div_infallible(lhs: Self, rhs: Self) -> Self {
        lhs / rhs
    }
}

impl CheckedArithmeticStorage for i32 {
    fn from_f64_for_arithmetic(value: f64) -> Result<Self, ArithmeticError> {
        if !value.is_finite() {
            return Err(ArithmeticError::Overflow);
        }
        if value < i32::MIN as f64 || value > i32::MAX as f64 {
            return Err(ArithmeticError::Overflow);
        }
        let truncated = value.trunc();
        if truncated != value {
            return Err(ArithmeticError::PrecisionLoss);
        }
        Ok(truncated as i32)
    }

    fn checked_add(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        lhs.checked_add(rhs).ok_or(ArithmeticError::Overflow)
    }

    fn checked_sub(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        lhs.checked_sub(rhs).ok_or(ArithmeticError::Overflow)
    }

    fn checked_mul(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        lhs.checked_mul(rhs).ok_or(ArithmeticError::Overflow)
    }

    fn checked_div(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        if rhs == 0 {
            return Err(ArithmeticError::DivisionByZero);
        }
        if lhs % rhs != 0 {
            return Err(ArithmeticError::NonIntegralDivision);
        }
        Ok(lhs / rhs)
    }
}

macro_rules! impl_add_sub_rule {
    ($lhs:ty, $rhs:ty => $out:ty, infallible) => {
        impl AddSubPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl InfallibleAddSubPromotion<$rhs> for $lhs {}
    };
    ($lhs:ty, $rhs:ty => $out:ty, checked) => {
        impl AddSubPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl CheckedAddSubPromotion<$rhs> for $lhs {}
    };
}

macro_rules! impl_mul_rule {
    ($lhs:ty, $rhs:ty => $out:ty, infallible) => {
        impl MulPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl InfallibleMulPromotion<$rhs> for $lhs {}
    };
    ($lhs:ty, $rhs:ty => $out:ty, checked) => {
        impl MulPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl CheckedMulPromotion<$rhs> for $lhs {}
    };
}

macro_rules! impl_div_rule {
    ($lhs:ty, $rhs:ty => $out:ty, infallible) => {
        impl DivPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl InfallibleDivPromotion<$rhs> for $lhs {}
    };
    ($lhs:ty, $rhs:ty => $out:ty, checked) => {
        impl DivPromotion<$rhs> for $lhs {
            type Output = $out;
        }
        impl CheckedDivPromotion<$rhs> for $lhs {}
    };
}

fn checked_add_quantities<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> Result<<Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
where
    Lhs: QuantityType,
    Rhs: QuantityType,
    Lhs::Storage: ValueStorage + CheckedAddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: CheckedArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs)?;
    let rhs_value = convert_quantity_for_arithmetic::<
        Rhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(rhs)?;
    let result =
        OutStorage::checked_add(lhs_value.quantity().storage, rhs_value.quantity().storage)?;
    Ok(<Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result))
}

fn checked_sub_quantities<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> Result<<Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
where
    Lhs: QuantityType,
    Rhs: QuantityType,
    Lhs::Storage: ValueStorage + CheckedAddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: CheckedArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs)?;
    let rhs_value = convert_quantity_for_arithmetic::<
        Rhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(rhs)?;
    let result =
        OutStorage::checked_sub(lhs_value.quantity().storage, rhs_value.quantity().storage)?;
    Ok(<Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result))
}

fn checked_mul_scalar<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> Result<<Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
where
    Lhs: QuantityType,
    Lhs::Storage: ValueStorage + CheckedMulPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: CheckedArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs)?;
    let rhs_value = OutStorage::from_f64_for_arithmetic(rhs.to_f64())?;
    let result = OutStorage::checked_mul(lhs_value.quantity().storage, rhs_value)?;
    Ok(<Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result))
}

fn checked_div_scalar<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> Result<<Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
where
    Lhs: QuantityType,
    Lhs::Storage: ValueStorage + CheckedDivPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: CheckedArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs)?;
    let rhs_value = OutStorage::from_f64_for_arithmetic(rhs.to_f64())?;
    let result = OutStorage::checked_div(lhs_value.quantity().storage, rhs_value)?;
    Ok(<Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result))
}

fn add_quantities_infallible<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity
where
    Lhs: QuantityType,
    Rhs: QuantityType,
    Lhs::Storage: ValueStorage + AddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: InfallibleArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic_infallible::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs);
    let rhs_value = convert_quantity_for_arithmetic_infallible::<
        Rhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(rhs);
    let result =
        OutStorage::add_infallible(lhs_value.quantity().storage, rhs_value.quantity().storage);
    <Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result)
}

fn sub_quantities_infallible<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity
where
    Lhs: QuantityType,
    Rhs: QuantityType,
    Lhs::Storage: ValueStorage + AddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: InfallibleArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic_infallible::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs);
    let rhs_value = convert_quantity_for_arithmetic_infallible::<
        Rhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(rhs);
    let result =
        OutStorage::sub_infallible(lhs_value.quantity().storage, rhs_value.quantity().storage);
    <Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result)
}

fn mul_scalar_infallible<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity
where
    Lhs: QuantityType,
    Lhs::Storage: ValueStorage + MulPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: InfallibleArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic_infallible::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs);
    let rhs_value = OutStorage::from_f64_for_arithmetic_infallible(rhs.to_f64());
    let result = OutStorage::mul_infallible(lhs_value.quantity().storage, rhs_value);
    <Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result)
}

fn div_scalar_infallible<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity
where
    Lhs: QuantityType,
    Lhs::Storage: ValueStorage + DivPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: InfallibleArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic_infallible::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs);
    let rhs_value = OutStorage::from_f64_for_arithmetic_infallible(rhs.to_f64());
    let result = OutStorage::div_infallible(lhs_value.quantity().storage, rhs_value);
    <Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result)
}

pub fn velocity_from_distance_and_time<DistanceStorage, DistanceMeasure, TimeStorage, TimeMeasure>(
    distance: Distance<DistanceStorage, DistanceMeasure>,
    duration: Time<TimeStorage, TimeMeasure>,
) -> Result<Velocity<f64, mps>, ComputeError>
where
    DistanceStorage: ValueStorage,
    DistanceMeasure: DistanceUnit,
    TimeStorage: ValueStorage,
    TimeMeasure: TimeUnit,
{
    let distance_canonical =
        convert_quantity_for_arithmetic_infallible::<_, Distance<f64, m>>(distance);
    let duration_canonical =
        convert_quantity_for_arithmetic_infallible::<_, Time<f64, s>>(duration);
    if duration_canonical.value() == 0.0 {
        return Err(ComputeError::ZeroDuration);
    }
    Ok(Velocity::mps(
        distance_canonical.value() / duration_canonical.value(),
    ))
}

pub fn acceleration_from_velocity_and_time<
    VelocityStorage,
    VelocityMeasure,
    TimeStorage,
    TimeMeasure,
>(
    velocity: Velocity<VelocityStorage, VelocityMeasure>,
    duration: Time<TimeStorage, TimeMeasure>,
) -> Result<Acceleration<f64, mps2>, ComputeError>
where
    VelocityStorage: ValueStorage,
    VelocityMeasure: VelocityUnit,
    TimeStorage: ValueStorage,
    TimeMeasure: TimeUnit,
{
    let velocity_canonical =
        convert_quantity_for_arithmetic_infallible::<_, Velocity<f64, mps>>(velocity);
    let duration_canonical =
        convert_quantity_for_arithmetic_infallible::<_, Time<f64, s>>(duration);
    if duration_canonical.value() == 0.0 {
        return Err(ComputeError::ZeroDuration);
    }
    Ok(Acceleration::mps2(
        velocity_canonical.value() / duration_canonical.value(),
    ))
}

fn convert_quantity_for_arithmetic<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> Result<TargetQuantity, ArithmeticError>
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: CheckedArithmeticStorage,
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
    let converted_value = if SourceQuantity::PUBLIC_TYPE == TargetQuantity::PUBLIC_TYPE
        && <SourceQuantity::Unit as UnitMarker>::UNIT_CODE_ID
            == <TargetQuantity::Unit as UnitMarker>::UNIT_CODE_ID
    {
        source.quantity().storage.to_f64()
    } else {
        let base_value = to_base_value(source.quantity().storage.to_f64(), source_meta);
        from_base_value(base_value, target_meta)
    };
    let target_storage =
        <TargetQuantity::Storage as CheckedArithmeticStorage>::from_f64_for_arithmetic(
            converted_value,
        )?;
    Ok(TargetQuantity::from_quantity(Quantity::new(target_storage)))
}

fn convert_quantity_for_arithmetic_infallible<SourceQuantity, TargetQuantity>(
    source: SourceQuantity,
) -> TargetQuantity
where
    SourceQuantity: QuantityType,
    SourceQuantity::Storage: ValueStorage,
    TargetQuantity: QuantityType,
    TargetQuantity::Storage: InfallibleArithmeticStorage,
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
    let converted_value = if SourceQuantity::PUBLIC_TYPE == TargetQuantity::PUBLIC_TYPE
        && <SourceQuantity::Unit as UnitMarker>::UNIT_CODE_ID
            == <TargetQuantity::Unit as UnitMarker>::UNIT_CODE_ID
    {
        source.quantity().storage.to_f64()
    } else {
        let base_value = to_base_value(source.quantity().storage.to_f64(), source_meta);
        from_base_value(base_value, target_meta)
    };
    let target_storage =
        <TargetQuantity::Storage as InfallibleArithmeticStorage>::from_f64_for_arithmetic_infallible(
            converted_value,
        );
    TargetQuantity::from_quantity(Quantity::new(target_storage))
}

macro_rules! impl_same_public_type_arithmetic {
    ($public_type:ident, $unit_trait:ident) => {
        impl<LhsStorage, LhsUnit> $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage,
            LhsUnit: $unit_trait,
        {
            pub fn checked_add<RhsStorage, RhsUnit, OutStorage>(
                self,
                rhs: $public_type<RhsStorage, RhsUnit>,
            ) -> Result<<LhsUnit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
            where
                LhsStorage: CheckedAddSubPromotion<RhsStorage, Output = OutStorage>,
                RhsStorage: ValueStorage,
                RhsUnit: $unit_trait,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: CheckedArithmeticStorage,
            {
                checked_add_quantities::<Self, $public_type<RhsStorage, RhsUnit>, OutStorage>(
                    self, rhs,
                )
            }

            pub fn checked_sub<RhsStorage, RhsUnit, OutStorage>(
                self,
                rhs: $public_type<RhsStorage, RhsUnit>,
            ) -> Result<<LhsUnit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
            where
                LhsStorage: CheckedAddSubPromotion<RhsStorage, Output = OutStorage>,
                RhsStorage: ValueStorage,
                RhsUnit: $unit_trait,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: CheckedArithmeticStorage,
            {
                checked_sub_quantities::<Self, $public_type<RhsStorage, RhsUnit>, OutStorage>(
                    self, rhs,
                )
            }
        }

        impl<LhsStorage, LhsUnit, RhsStorage, RhsUnit> Add<$public_type<RhsStorage, RhsUnit>>
            for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleAddSubPromotion<RhsStorage>,
            RhsStorage: ValueStorage,
            LhsUnit: $unit_trait
                + QuantityForStorage<<LhsStorage as AddSubPromotion<RhsStorage>>::Output>,
            RhsUnit: $unit_trait,
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn add(self, rhs: $public_type<RhsStorage, RhsUnit>) -> Self::Output {
                add_quantities_infallible::<
                    Self,
                    $public_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
            }
        }

        impl<LhsStorage, LhsUnit, RhsStorage, RhsUnit> Sub<$public_type<RhsStorage, RhsUnit>>
            for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleAddSubPromotion<RhsStorage>,
            RhsStorage: ValueStorage,
            LhsUnit: $unit_trait
                + QuantityForStorage<<LhsStorage as AddSubPromotion<RhsStorage>>::Output>,
            RhsUnit: $unit_trait,
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn sub(self, rhs: $public_type<RhsStorage, RhsUnit>) -> Self::Output {
                sub_quantities_infallible::<
                    Self,
                    $public_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
            }
        }
    };
}

macro_rules! impl_scalar_arithmetic {
    ($public_type:ident, $unit_trait:ident) => {
        impl<LhsStorage, LhsUnit> $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage,
            LhsUnit: $unit_trait,
        {
            pub fn checked_mul<Rhs, OutStorage>(
                self,
                rhs: Rhs,
            ) -> Result<<LhsUnit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
            where
                LhsStorage: CheckedMulPromotion<Rhs, Output = OutStorage>,
                Rhs: ValueStorage,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: CheckedArithmeticStorage,
            {
                checked_mul_scalar::<Self, Rhs, OutStorage>(self, rhs)
            }

            pub fn checked_div<Rhs, OutStorage>(
                self,
                rhs: Rhs,
            ) -> Result<<LhsUnit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
            where
                LhsStorage: CheckedDivPromotion<Rhs, Output = OutStorage>,
                Rhs: ValueStorage,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: CheckedArithmeticStorage,
            {
                checked_div_scalar::<Self, Rhs, OutStorage>(self, rhs)
            }
        }

        impl<LhsStorage, LhsUnit, Rhs> Mul<Rhs> for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleMulPromotion<Rhs>,
            Rhs: ValueStorage,
            LhsUnit: $unit_trait + QuantityForStorage<<LhsStorage as MulPromotion<Rhs>>::Output>,
            <LhsStorage as MulPromotion<Rhs>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as MulPromotion<Rhs>>::Output,
            >>::Quantity;

            fn mul(self, rhs: Rhs) -> Self::Output {
                mul_scalar_infallible::<Self, Rhs, <LhsStorage as MulPromotion<Rhs>>::Output>(
                    self, rhs,
                )
            }
        }

        impl<LhsStorage, LhsUnit, Rhs> Div<Rhs> for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleDivPromotion<Rhs>,
            Rhs: ValueStorage,
            LhsUnit: $unit_trait + QuantityForStorage<<LhsStorage as DivPromotion<Rhs>>::Output>,
            <LhsStorage as DivPromotion<Rhs>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as DivPromotion<Rhs>>::Output,
            >>::Quantity;

            fn div(self, rhs: Rhs) -> Self::Output {
                div_scalar_infallible::<Self, Rhs, <LhsStorage as DivPromotion<Rhs>>::Output>(
                    self, rhs,
                )
            }
        }
    };
}

macro_rules! impl_cross_public_add_sub {
    ($lhs_type:ident, $lhs_unit_trait:ident, $rhs_type:ident, $rhs_unit_trait:ident) => {
        impl<LhsStorage, LhsUnit, RhsStorage, RhsUnit> Add<$rhs_type<RhsStorage, RhsUnit>>
            for $lhs_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleAddSubPromotion<RhsStorage>,
            RhsStorage: ValueStorage,
            LhsUnit: $lhs_unit_trait
                + QuantityForStorage<<LhsStorage as AddSubPromotion<RhsStorage>>::Output>,
            RhsUnit: $rhs_unit_trait,
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn add(self, rhs: $rhs_type<RhsStorage, RhsUnit>) -> Self::Output {
                add_quantities_infallible::<
                    Self,
                    $rhs_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
            }
        }

        impl<LhsStorage, LhsUnit, RhsStorage, RhsUnit> Sub<$rhs_type<RhsStorage, RhsUnit>>
            for $lhs_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleAddSubPromotion<RhsStorage>,
            RhsStorage: ValueStorage,
            LhsUnit: $lhs_unit_trait
                + QuantityForStorage<<LhsStorage as AddSubPromotion<RhsStorage>>::Output>,
            RhsUnit: $rhs_unit_trait,
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: InfallibleArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn sub(self, rhs: $rhs_type<RhsStorage, RhsUnit>) -> Self::Output {
                sub_quantities_infallible::<
                    Self,
                    $rhs_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
            }
        }
    };
}

include!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/src/generated/arithmetic_impls.rs"
));

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::public_types::{dpt, per_m, Diopter, InverseDistance};

    fn assert_close(left: f64, right: f64) {
        assert!((left - right).abs() < 1.0e-6, "left={left}, right={right}");
    }

    #[test]
    fn mixed_unit_addition_preserves_left_hand_unit() {
        let lhs = Distance::mm(250.0_f64);
        let rhs = Distance::m(1.0_f64);
        let out = lhs + rhs;
        assert_eq!(out.unit(), "mm");
        assert_close(out.value(), 1250.0);
    }

    #[test]
    fn mixed_storage_promotion_works() {
        let lhs = Distance::mm(25_i32);
        let rhs = Distance::m(1.0_f64);
        let out: Distance<f64, mm> = lhs + rhs;
        assert_eq!(out.unit(), "mm");
        assert_close(out.value(), 1025.0);

        let widened: Distance<f64, m> = Distance::m(i32::MAX) + Distance::m(0.0_f32);
        assert_close(widened.value(), i32::MAX as f64);
    }

    #[test]
    fn checked_integer_overflow_is_reported() {
        let error =
            checked_add_quantities::<_, _, i32>(Distance::mm(i32::MAX), Distance::mm(1_i32))
                .unwrap_err();
        assert_eq!(error, ArithmeticError::Overflow);
    }

    #[test]
    fn exact_integer_division_is_supported_and_non_integral_division_is_rejected() {
        let exact = Distance::mm(20_i32).checked_div(2_i32).unwrap();
        assert_eq!(exact.value(), 10);

        let error = Distance::mm(1_i32).checked_div(2_i32).unwrap_err();
        assert_eq!(error, ArithmeticError::NonIntegralDivision);
    }

    #[test]
    fn integer_division_by_zero_is_reported() {
        let error = Distance::mm(1_i32).checked_div(0_i32).unwrap_err();
        assert_eq!(error, ArithmeticError::DivisionByZero);
    }

    #[test]
    fn checked_add_reports_precision_loss_for_integer_unit_conversion() {
        let error = Distance::m(1_i32)
            .checked_add::<i32, ft, i32>(Distance::ft(1_i32))
            .unwrap_err();
        assert_eq!(error, ArithmeticError::PrecisionLoss);
    }

    #[test]
    fn cross_public_type_addition_preserves_left_hand_identity() {
        let lhs = Diopter::dpt(2.0_f64);
        let rhs = InverseDistance::per_m(0.5_f64);
        let out: Diopter<f64, dpt> = lhs + rhs;
        assert_eq!(out.unit(), "D");
        assert_close(out.value(), 2.5);
    }

    #[test]
    fn velocity_and_acceleration_compute_bridges_are_available() {
        let velocity =
            velocity_from_distance_and_time(Distance::ft(3.28084_f64), Time::s(1.0_f64)).unwrap();
        assert_close(velocity.value(), 1.0);

        let acceleration =
            acceleration_from_velocity_and_time(Velocity::mps(10.0_f64), Time::s(2.0_f64)).unwrap();
        assert_close(acceleration.value(), 5.0);
    }

    #[test]
    fn zero_duration_is_rejected_in_compute_bridges() {
        let error =
            velocity_from_distance_and_time(Distance::m(1.0_f64), Time::s(0.0_f64)).unwrap_err();
        assert_eq!(error, ComputeError::ZeroDuration);
    }

    #[test]
    fn reciprocal_canonical_pair_supports_subtraction() {
        let lhs = InverseDistance::per_m(3.0_f64);
        let rhs = Diopter::dpt(1.5_f64);
        let out: InverseDistance<f64, per_m> = lhs - rhs;
        assert_close(out.value(), 1.5);
    }
}
