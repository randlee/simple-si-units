# units-x In-Scope Type Inventory

## Purpose

This document is a derived reference checklist for the MVP public type surface.

The authoritative source is `catalog/generated/units-catalog-summary.json`.
This markdown checklist exists for human review and planning readability and
must mirror the catalog-derived summary instead of replacing it.

## Scope Rule

The MVP reference checklist mirrors the catalog-derived public type surface for:

- every reference type from `base`
- every reference type from `geometry`
- every reference type from `mechanical`
- every reference type from `electromagnetic`
- additional first-class reciprocal domain types explicitly added for `units-x`

Current additional reciprocal domain types:

- `Diopter`

## Checklist

### `base`

- [x] `Amount`
- [x] `Current`
- [x] `Distance`
- [x] `InverseAmount`
- [x] `InverseCurrent`
- [x] `InverseDistance`
- [x] `InverseLuminosity`
- [x] `InverseMass`
- [x] `InverseTemperature`
- [x] `Luminosity`
- [x] `Mass`
- [x] `Temperature`
- [x] `Time`

### `geometry`

- [x] `Angle`
- [x] `Area`
- [x] `InverseAngle`
- [x] `InverseArea`
- [x] `InverseSolidAngle`
- [x] `InverseVolume`
- [x] `SolidAngle`
- [x] `Volume`

### `mechanical`

- [x] `Acceleration`
- [x] `AngularAcceleration`
- [x] `AngularMomentum`
- [x] `AngularVelocity`
- [x] `AreaDensity`
- [x] `AreaPerMass`
- [x] `Density`
- [x] `Energy`
- [x] `Force`
- [x] `Frequency`
- [x] `InverseAcceleration`
- [x] `InverseAngularAcceleration`
- [x] `InverseAngularMomentum`
- [x] `InverseAngularVelocity`
- [x] `InverseEnergy`
- [x] `InverseForce`
- [x] `InverseMomentOfInertia`
- [x] `InverseMomentum`
- [x] `InversePower`
- [x] `InversePressure`
- [x] `InverseTorque`
- [x] `MomentOfInertia`
- [x] `Momentum`
- [x] `Power`
- [x] `Pressure`
- [x] `TimePerDistance`
- [x] `Torque`
- [x] `Velocity`
- [x] `VolumePerMass`

### `electromagnetic`

- [x] `AreaPerLumen`
- [x] `Capacitance`
- [x] `Charge`
- [x] `Conductance`
- [x] `Elastance`
- [x] `Illuminance`
- [x] `Inductance`
- [x] `InverseCharge`
- [x] `InverseInductance`
- [x] `InverseLuminousFlux`
- [x] `InverseMagneticFlux`
- [x] `InverseMagneticFluxDensity`
- [x] `InverseVoltage`
- [x] `LuminousFlux`
- [x] `MagneticFlux`
- [x] `MagneticFluxDensity`
- [x] `Resistance`
- [x] `Voltage`

### Additional public reciprocal types

- [x] `Diopter`
