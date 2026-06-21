# units-x In-Scope Type Inventory

## Purpose

This document is the authoritative checklist for the MVP public type surface.

Sprint plans, validation work, and documentation work must reference this file
instead of maintaining diverging copies of the same inventory.

## Scope Rule

The MVP in-scope public type inventory consists of:

- every reference type from `base`
- every reference type from `geometry`
- every reference type from `mechanical`
- every reference type from `electromagnetic`
- additional first-class reciprocal domain types explicitly added for `units-x`

Current additional reciprocal domain types:

- `Diopter`

## Checklist

### `base`

- [ ] `Amount`
- [ ] `Current`
- [ ] `Distance`
- [ ] `InverseAmount`
- [ ] `InverseCurrent`
- [ ] `InverseDistance`
- [ ] `InverseLuminosity`
- [ ] `InverseMass`
- [ ] `InverseTemperature`
- [ ] `Luminosity`
- [ ] `Mass`
- [ ] `Temperature`
- [ ] `Time`

### `geometry`

- [ ] `Angle`
- [ ] `Area`
- [ ] `InverseAngle`
- [ ] `InverseArea`
- [ ] `InverseSolidAngle`
- [ ] `InverseVolume`
- [ ] `SolidAngle`
- [ ] `Volume`

### `mechanical`

- [ ] `Acceleration`
- [ ] `AngularAcceleration`
- [ ] `AngularMomentum`
- [ ] `AngularVelocity`
- [ ] `AreaDensity`
- [ ] `AreaPerMass`
- [ ] `Density`
- [ ] `Energy`
- [ ] `Force`
- [ ] `Frequency`
- [ ] `InverseAcceleration`
- [ ] `InverseAngularAcceleration`
- [ ] `InverseAngularMomentum`
- [ ] `InverseAngularVelocity`
- [ ] `InverseEnergy`
- [ ] `InverseForce`
- [ ] `InverseMomentOfInertia`
- [ ] `InverseMomentum`
- [ ] `InversePower`
- [ ] `InversePressure`
- [ ] `InverseTorque`
- [ ] `MomentOfInertia`
- [ ] `Momentum`
- [ ] `Power`
- [ ] `Pressure`
- [ ] `TimePerDistance`
- [ ] `Torque`
- [ ] `Velocity`
- [ ] `VolumePerMass`

### `electromagnetic`

- [ ] `AreaPerLumen`
- [ ] `Capacitance`
- [ ] `Charge`
- [ ] `Conductance`
- [ ] `Elastance`
- [ ] `Illuminance`
- [ ] `Inductance`
- [ ] `InverseCharge`
- [ ] `InverseInductance`
- [ ] `InverseLuminousFlux`
- [ ] `InverseMagneticFlux`
- [ ] `InverseMagneticFluxDensity`
- [ ] `InverseVoltage`
- [ ] `LuminousFlux`
- [ ] `MagneticFlux`
- [ ] `MagneticFluxDensity`
- [ ] `Resistance`
- [ ] `Voltage`

### Additional public reciprocal types

- [ ] `Diopter`
