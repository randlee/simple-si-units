use crate::conversion::{from_base_value, lookup_unit_metadata, to_base_value, ValueStorage};
use crate::generated::public_types::*;
use crate::model::{Quantity, QuantityType, UnitMarker};
use core::ops::{Add, Div, Mul, Sub};

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

pub trait CheckedScalarArithmeticOps<Rhs = Self> {
    type Output;

    fn checked_add(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_sub(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_mul(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_div(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
}

pub trait AddSubPromotion<Rhs>: ValueStorage {
    type Output: ArithmeticStorage;
}

pub trait InfallibleAddSubPromotion<Rhs>: AddSubPromotion<Rhs> {}

pub trait MulPromotion<Rhs>: ValueStorage {
    type Output: ArithmeticStorage;
}

pub trait InfallibleMulPromotion<Rhs>: MulPromotion<Rhs> {}

pub trait DivPromotion<Rhs>: ValueStorage {
    type Output: ArithmeticStorage;
}

pub trait InfallibleDivPromotion<Rhs>: DivPromotion<Rhs> {}

pub trait ArithmeticStorage: ValueStorage {
    fn from_f64_for_arithmetic(value: f64) -> Result<Self, ArithmeticError>;
    fn checked_add(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_sub(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_mul(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
    fn checked_div(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError>;
}

impl ArithmeticStorage for f64 {
    fn from_f64_for_arithmetic(value: f64) -> Result<Self, ArithmeticError> {
        Ok(value)
    }

    fn checked_add(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs + rhs)
    }

    fn checked_sub(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs - rhs)
    }

    fn checked_mul(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs * rhs)
    }

    fn checked_div(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs / rhs)
    }
}

impl ArithmeticStorage for f32 {
    fn from_f64_for_arithmetic(value: f64) -> Result<Self, ArithmeticError> {
        if value.is_nan() {
            return Ok(f32::NAN);
        }
        if !value.is_finite() || value > f32::MAX as f64 || value < f32::MIN as f64 {
            return Err(ArithmeticError::Overflow);
        }
        Ok(value as f32)
    }

    fn checked_add(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs + rhs)
    }

    fn checked_sub(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs - rhs)
    }

    fn checked_mul(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs * rhs)
    }

    fn checked_div(lhs: Self, rhs: Self) -> Result<Self, ArithmeticError> {
        Ok(lhs / rhs)
    }
}

impl ArithmeticStorage for i32 {
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
    };
}

impl_add_sub_rule!(f64, f64 => f64, infallible);
impl_add_sub_rule!(f64, f32 => f64, infallible);
impl_add_sub_rule!(f64, i32 => f64, infallible);
impl_add_sub_rule!(f32, f64 => f64, infallible);
impl_add_sub_rule!(f32, f32 => f32, infallible);
impl_add_sub_rule!(f32, i32 => f32, infallible);
impl_add_sub_rule!(i32, f64 => f64, infallible);
impl_add_sub_rule!(i32, f32 => f32, infallible);
impl_add_sub_rule!(i32, i32 => i32, checked);

impl_mul_rule!(f64, f64 => f64, infallible);
impl_mul_rule!(f64, f32 => f64, infallible);
impl_mul_rule!(f64, i32 => f64, infallible);
impl_mul_rule!(f32, f64 => f64, infallible);
impl_mul_rule!(f32, f32 => f32, infallible);
impl_mul_rule!(f32, i32 => f32, infallible);
impl_mul_rule!(i32, f64 => f64, infallible);
impl_mul_rule!(i32, f32 => f32, infallible);
impl_mul_rule!(i32, i32 => i32, checked);

impl_div_rule!(f64, f64 => f64, infallible);
impl_div_rule!(f64, f32 => f64, infallible);
impl_div_rule!(f64, i32 => f64, infallible);
impl_div_rule!(f32, f64 => f64, infallible);
impl_div_rule!(f32, f32 => f32, infallible);
impl_div_rule!(f32, i32 => f32, infallible);
impl_div_rule!(i32, f64 => f64, infallible);
impl_div_rule!(i32, f32 => f32, infallible);
impl_div_rule!(i32, i32 => i32, checked);

fn checked_add_quantities<Lhs, Rhs, OutStorage>(
    lhs: Lhs,
    rhs: Rhs,
) -> Result<<Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
where
    Lhs: QuantityType,
    Rhs: QuantityType,
    Lhs::Storage: ValueStorage + AddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: ArithmeticStorage,
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
    Lhs::Storage: ValueStorage + AddSubPromotion<Rhs::Storage, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs::Storage: ValueStorage,
    OutStorage: ArithmeticStorage,
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
    Lhs::Storage: ValueStorage + MulPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: ArithmeticStorage,
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
    Lhs::Storage: ValueStorage + DivPromotion<Rhs, Output = OutStorage>,
    Lhs::Unit: QuantityForStorage<OutStorage>,
    Rhs: ValueStorage,
    OutStorage: ArithmeticStorage,
{
    let lhs_value = convert_quantity_for_arithmetic::<
        Lhs,
        <Lhs::Unit as QuantityForStorage<OutStorage>>::Quantity,
    >(lhs)?;
    let rhs_value = OutStorage::from_f64_for_arithmetic(rhs.to_f64())?;
    let result = OutStorage::checked_div(lhs_value.quantity().storage, rhs_value)?;
    Ok(<Lhs::Unit as QuantityForStorage<OutStorage>>::wrap(result))
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
    let distance_canonical = convert_quantity_for_arithmetic::<_, Distance<f64, m>>(distance)
        .expect("f64 compute canonicalization must be infallible");
    let duration_canonical = convert_quantity_for_arithmetic::<_, Time<f64, s>>(duration)
        .expect("f64 compute canonicalization must be infallible");
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
    let velocity_canonical = convert_quantity_for_arithmetic::<_, Velocity<f64, mps>>(velocity)
        .expect("f64 compute canonicalization must be infallible");
    let duration_canonical = convert_quantity_for_arithmetic::<_, Time<f64, s>>(duration)
        .expect("f64 compute canonicalization must be infallible");
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
    TargetQuantity::Storage: ArithmeticStorage,
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
        <TargetQuantity::Storage as ArithmeticStorage>::from_f64_for_arithmetic(converted_value)?;
    Ok(TargetQuantity::from_quantity(Quantity::new(target_storage)))
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
                LhsStorage: AddSubPromotion<RhsStorage, Output = OutStorage>,
                RhsStorage: ValueStorage,
                RhsUnit: $unit_trait,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: ArithmeticStorage,
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
                LhsStorage: AddSubPromotion<RhsStorage, Output = OutStorage>,
                RhsStorage: ValueStorage,
                RhsUnit: $unit_trait,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: ArithmeticStorage,
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
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn add(self, rhs: $public_type<RhsStorage, RhsUnit>) -> Self::Output {
                checked_add_quantities::<
                    Self,
                    $public_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
                .expect("infallible add path must succeed")
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
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn sub(self, rhs: $public_type<RhsStorage, RhsUnit>) -> Self::Output {
                checked_sub_quantities::<
                    Self,
                    $public_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
                .expect("infallible sub path must succeed")
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
                LhsStorage: MulPromotion<Rhs, Output = OutStorage>,
                Rhs: ValueStorage,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: ArithmeticStorage,
            {
                checked_mul_scalar::<Self, Rhs, OutStorage>(self, rhs)
            }

            pub fn checked_div<Rhs, OutStorage>(
                self,
                rhs: Rhs,
            ) -> Result<<LhsUnit as QuantityForStorage<OutStorage>>::Quantity, ArithmeticError>
            where
                LhsStorage: DivPromotion<Rhs, Output = OutStorage>,
                Rhs: ValueStorage,
                LhsUnit: QuantityForStorage<OutStorage>,
                OutStorage: ArithmeticStorage,
            {
                checked_div_scalar::<Self, Rhs, OutStorage>(self, rhs)
            }
        }

        impl<LhsStorage, LhsUnit, Rhs> Mul<Rhs> for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleMulPromotion<Rhs>,
            Rhs: ValueStorage,
            LhsUnit: $unit_trait + QuantityForStorage<<LhsStorage as MulPromotion<Rhs>>::Output>,
            <LhsStorage as MulPromotion<Rhs>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as MulPromotion<Rhs>>::Output,
            >>::Quantity;

            fn mul(self, rhs: Rhs) -> Self::Output {
                checked_mul_scalar::<Self, Rhs, <LhsStorage as MulPromotion<Rhs>>::Output>(
                    self, rhs,
                )
                .expect("infallible mul path must succeed")
            }
        }

        impl<LhsStorage, LhsUnit, Rhs> Div<Rhs> for $public_type<LhsStorage, LhsUnit>
        where
            LhsStorage: ValueStorage + InfallibleDivPromotion<Rhs>,
            Rhs: ValueStorage,
            LhsUnit: $unit_trait + QuantityForStorage<<LhsStorage as DivPromotion<Rhs>>::Output>,
            <LhsStorage as DivPromotion<Rhs>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as DivPromotion<Rhs>>::Output,
            >>::Quantity;

            fn div(self, rhs: Rhs) -> Self::Output {
                checked_div_scalar::<Self, Rhs, <LhsStorage as DivPromotion<Rhs>>::Output>(
                    self, rhs,
                )
                .expect("infallible div path must succeed")
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
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn add(self, rhs: $rhs_type<RhsStorage, RhsUnit>) -> Self::Output {
                checked_add_quantities::<
                    Self,
                    $rhs_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
                .expect("infallible cross-type add path must succeed")
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
            <LhsStorage as AddSubPromotion<RhsStorage>>::Output: ArithmeticStorage,
        {
            type Output = <LhsUnit as QuantityForStorage<
                <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
            >>::Quantity;

            fn sub(self, rhs: $rhs_type<RhsStorage, RhsUnit>) -> Self::Output {
                checked_sub_quantities::<
                    Self,
                    $rhs_type<RhsStorage, RhsUnit>,
                    <LhsStorage as AddSubPromotion<RhsStorage>>::Output,
                >(self, rhs)
                .expect("infallible cross-type sub path must succeed")
            }
        }
    };
}

impl_same_public_type_arithmetic!(Amount, AmountUnit);
impl_scalar_arithmetic!(Amount, AmountUnit);
impl_same_public_type_arithmetic!(Current, CurrentUnit);
impl_scalar_arithmetic!(Current, CurrentUnit);
impl_same_public_type_arithmetic!(Distance, DistanceUnit);
impl_scalar_arithmetic!(Distance, DistanceUnit);
impl_same_public_type_arithmetic!(InverseAmount, InverseAmountUnit);
impl_scalar_arithmetic!(InverseAmount, InverseAmountUnit);
impl_same_public_type_arithmetic!(InverseCurrent, InverseCurrentUnit);
impl_scalar_arithmetic!(InverseCurrent, InverseCurrentUnit);
impl_same_public_type_arithmetic!(InverseDistance, InverseDistanceUnit);
impl_scalar_arithmetic!(InverseDistance, InverseDistanceUnit);
impl_same_public_type_arithmetic!(InverseLuminosity, InverseLuminosityUnit);
impl_scalar_arithmetic!(InverseLuminosity, InverseLuminosityUnit);
impl_same_public_type_arithmetic!(InverseMass, InverseMassUnit);
impl_scalar_arithmetic!(InverseMass, InverseMassUnit);
impl_same_public_type_arithmetic!(InverseTemperature, InverseTemperatureUnit);
impl_scalar_arithmetic!(InverseTemperature, InverseTemperatureUnit);
impl_same_public_type_arithmetic!(Luminosity, LuminosityUnit);
impl_scalar_arithmetic!(Luminosity, LuminosityUnit);
impl_same_public_type_arithmetic!(Mass, MassUnit);
impl_scalar_arithmetic!(Mass, MassUnit);
impl_same_public_type_arithmetic!(Time, TimeUnit);
impl_scalar_arithmetic!(Time, TimeUnit);
impl_same_public_type_arithmetic!(Acceleration, AccelerationUnit);
impl_scalar_arithmetic!(Acceleration, AccelerationUnit);
impl_same_public_type_arithmetic!(Angle, AngleUnit);
impl_scalar_arithmetic!(Angle, AngleUnit);
impl_same_public_type_arithmetic!(AngularAcceleration, AngularAccelerationUnit);
impl_scalar_arithmetic!(AngularAcceleration, AngularAccelerationUnit);
impl_same_public_type_arithmetic!(AngularMomentum, AngularMomentumUnit);
impl_scalar_arithmetic!(AngularMomentum, AngularMomentumUnit);
impl_same_public_type_arithmetic!(AngularVelocity, AngularVelocityUnit);
impl_scalar_arithmetic!(AngularVelocity, AngularVelocityUnit);
impl_same_public_type_arithmetic!(Area, AreaUnit);
impl_scalar_arithmetic!(Area, AreaUnit);
impl_same_public_type_arithmetic!(InverseAngle, InverseAngleUnit);
impl_scalar_arithmetic!(InverseAngle, InverseAngleUnit);
impl_same_public_type_arithmetic!(InverseAngularAcceleration, InverseAngularAccelerationUnit);
impl_scalar_arithmetic!(InverseAngularAcceleration, InverseAngularAccelerationUnit);
impl_same_public_type_arithmetic!(InverseAngularMomentum, InverseAngularMomentumUnit);
impl_scalar_arithmetic!(InverseAngularMomentum, InverseAngularMomentumUnit);
impl_same_public_type_arithmetic!(InverseAngularVelocity, InverseAngularVelocityUnit);
impl_scalar_arithmetic!(InverseAngularVelocity, InverseAngularVelocityUnit);
impl_same_public_type_arithmetic!(InverseArea, InverseAreaUnit);
impl_scalar_arithmetic!(InverseArea, InverseAreaUnit);
impl_same_public_type_arithmetic!(InverseSolidAngle, InverseSolidAngleUnit);
impl_scalar_arithmetic!(InverseSolidAngle, InverseSolidAngleUnit);
impl_same_public_type_arithmetic!(SolidAngle, SolidAngleUnit);
impl_scalar_arithmetic!(SolidAngle, SolidAngleUnit);
impl_same_public_type_arithmetic!(Velocity, VelocityUnit);
impl_scalar_arithmetic!(Velocity, VelocityUnit);
impl_same_public_type_arithmetic!(AreaDensity, AreaDensityUnit);
impl_scalar_arithmetic!(AreaDensity, AreaDensityUnit);
impl_same_public_type_arithmetic!(AreaPerLumen, AreaPerLumenUnit);
impl_scalar_arithmetic!(AreaPerLumen, AreaPerLumenUnit);
impl_same_public_type_arithmetic!(AreaPerMass, AreaPerMassUnit);
impl_scalar_arithmetic!(AreaPerMass, AreaPerMassUnit);
impl_same_public_type_arithmetic!(Capacitance, CapacitanceUnit);
impl_scalar_arithmetic!(Capacitance, CapacitanceUnit);
impl_same_public_type_arithmetic!(Charge, ChargeUnit);
impl_scalar_arithmetic!(Charge, ChargeUnit);
impl_same_public_type_arithmetic!(Conductance, ConductanceUnit);
impl_scalar_arithmetic!(Conductance, ConductanceUnit);
impl_same_public_type_arithmetic!(Density, DensityUnit);
impl_scalar_arithmetic!(Density, DensityUnit);
impl_same_public_type_arithmetic!(Diopter, DiopterUnit);
impl_scalar_arithmetic!(Diopter, DiopterUnit);
impl_same_public_type_arithmetic!(Elastance, ElastanceUnit);
impl_scalar_arithmetic!(Elastance, ElastanceUnit);
impl_same_public_type_arithmetic!(Energy, EnergyUnit);
impl_scalar_arithmetic!(Energy, EnergyUnit);
impl_same_public_type_arithmetic!(Force, ForceUnit);
impl_scalar_arithmetic!(Force, ForceUnit);
impl_same_public_type_arithmetic!(Frequency, FrequencyUnit);
impl_scalar_arithmetic!(Frequency, FrequencyUnit);
impl_same_public_type_arithmetic!(Illuminance, IlluminanceUnit);
impl_scalar_arithmetic!(Illuminance, IlluminanceUnit);
impl_same_public_type_arithmetic!(Inductance, InductanceUnit);
impl_scalar_arithmetic!(Inductance, InductanceUnit);
impl_same_public_type_arithmetic!(InverseAcceleration, InverseAccelerationUnit);
impl_scalar_arithmetic!(InverseAcceleration, InverseAccelerationUnit);
impl_same_public_type_arithmetic!(InverseCharge, InverseChargeUnit);
impl_scalar_arithmetic!(InverseCharge, InverseChargeUnit);
impl_same_public_type_arithmetic!(InverseEnergy, InverseEnergyUnit);
impl_scalar_arithmetic!(InverseEnergy, InverseEnergyUnit);
impl_same_public_type_arithmetic!(InverseForce, InverseForceUnit);
impl_scalar_arithmetic!(InverseForce, InverseForceUnit);
impl_same_public_type_arithmetic!(InverseInductance, InverseInductanceUnit);
impl_scalar_arithmetic!(InverseInductance, InverseInductanceUnit);
impl_same_public_type_arithmetic!(InverseLuminousFlux, InverseLuminousFluxUnit);
impl_scalar_arithmetic!(InverseLuminousFlux, InverseLuminousFluxUnit);
impl_same_public_type_arithmetic!(InverseMagneticFlux, InverseMagneticFluxUnit);
impl_scalar_arithmetic!(InverseMagneticFlux, InverseMagneticFluxUnit);
impl_same_public_type_arithmetic!(InverseMagneticFluxDensity, InverseMagneticFluxDensityUnit);
impl_scalar_arithmetic!(InverseMagneticFluxDensity, InverseMagneticFluxDensityUnit);
impl_same_public_type_arithmetic!(InverseMomentOfInertia, InverseMomentOfInertiaUnit);
impl_scalar_arithmetic!(InverseMomentOfInertia, InverseMomentOfInertiaUnit);
impl_same_public_type_arithmetic!(InverseMomentum, InverseMomentumUnit);
impl_scalar_arithmetic!(InverseMomentum, InverseMomentumUnit);
impl_same_public_type_arithmetic!(InversePower, InversePowerUnit);
impl_scalar_arithmetic!(InversePower, InversePowerUnit);
impl_same_public_type_arithmetic!(InversePressure, InversePressureUnit);
impl_scalar_arithmetic!(InversePressure, InversePressureUnit);
impl_same_public_type_arithmetic!(InverseTorque, InverseTorqueUnit);
impl_scalar_arithmetic!(InverseTorque, InverseTorqueUnit);
impl_same_public_type_arithmetic!(InverseVoltage, InverseVoltageUnit);
impl_scalar_arithmetic!(InverseVoltage, InverseVoltageUnit);
impl_same_public_type_arithmetic!(InverseVolume, InverseVolumeUnit);
impl_scalar_arithmetic!(InverseVolume, InverseVolumeUnit);
impl_same_public_type_arithmetic!(LuminousFlux, LuminousFluxUnit);
impl_scalar_arithmetic!(LuminousFlux, LuminousFluxUnit);
impl_same_public_type_arithmetic!(MagneticFlux, MagneticFluxUnit);
impl_scalar_arithmetic!(MagneticFlux, MagneticFluxUnit);
impl_same_public_type_arithmetic!(MagneticFluxDensity, MagneticFluxDensityUnit);
impl_scalar_arithmetic!(MagneticFluxDensity, MagneticFluxDensityUnit);
impl_same_public_type_arithmetic!(MomentOfInertia, MomentOfInertiaUnit);
impl_scalar_arithmetic!(MomentOfInertia, MomentOfInertiaUnit);
impl_same_public_type_arithmetic!(Momentum, MomentumUnit);
impl_scalar_arithmetic!(Momentum, MomentumUnit);
impl_same_public_type_arithmetic!(Power, PowerUnit);
impl_scalar_arithmetic!(Power, PowerUnit);
impl_same_public_type_arithmetic!(Pressure, PressureUnit);
impl_scalar_arithmetic!(Pressure, PressureUnit);
impl_same_public_type_arithmetic!(Resistance, ResistanceUnit);
impl_scalar_arithmetic!(Resistance, ResistanceUnit);
impl_same_public_type_arithmetic!(TimePerDistance, TimePerDistanceUnit);
impl_scalar_arithmetic!(TimePerDistance, TimePerDistanceUnit);
impl_same_public_type_arithmetic!(Torque, TorqueUnit);
impl_scalar_arithmetic!(Torque, TorqueUnit);
impl_same_public_type_arithmetic!(Voltage, VoltageUnit);
impl_scalar_arithmetic!(Voltage, VoltageUnit);
impl_same_public_type_arithmetic!(Volume, VolumeUnit);
impl_scalar_arithmetic!(Volume, VolumeUnit);
impl_same_public_type_arithmetic!(VolumePerMass, VolumePerMassUnit);
impl_scalar_arithmetic!(VolumePerMass, VolumePerMassUnit);

impl_cross_public_add_sub!(Diopter, DiopterUnit, InverseDistance, InverseDistanceUnit);
impl_cross_public_add_sub!(InverseDistance, InverseDistanceUnit, Diopter, DiopterUnit);

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
