# Type Model

## Short version

This library models each physical quantity as its own Rust type, parameterized by the numeric storage type.

Representative examples:

- [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039)
- [Time<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:11297)
- [Velocity<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25722)
- [Acceleration<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:26)

Each unit type stores one canonical SI value internally:

- `Distance<T>` stores meters in field `m`
- `Time<T>` stores seconds in field `s`
- `Velocity<T>` stores meters per second in field `mps`
- `Acceleration<T>` stores meters per second squared in field `mps2`

So the type system distinguishes:

- distance
- time
- velocity
- acceleration

even when all of them are backed by `f64`.

## Mental model

Think of the crate as:

1. A set of strongly typed wrappers around canonical SI values
2. A set of conversion constructors/getters for alternate units
3. A set of operator implementations that produce related derived types

Example:

```rust
use simple_si_units::base::{Distance, Time};
use simple_si_units::mechanical::{Velocity, Acceleration};

let d: Distance<f64> = Distance::from_m(100.0);
let t: Time<f64> = Time::from_s(20.0);
let v: Velocity<f64> = d / t;            // meters / seconds -> meters per second
let a: Acceleration<f64> = v / Time::from_s(4.0); // m/s / s -> m/s^2
```

## Example 1: Working with distance in meters and millimeters

`Distance` stores meters internally, but you can construct or read it in other supported units.

Relevant API:

- [Distance::from_m](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2056)
- [Distance::to_m](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2059)
- [Distance::from_mm](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2110)
- [Distance::to_mm](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2100)

```rust
use simple_si_units::base::Distance;

let d1 = Distance::from_m(2.5);
assert_eq!(d1.to_m(), 2.5);
assert_eq!(d1.to_mm(), 2500.0);

let d2 = Distance::from_mm(750.0);
assert_eq!(d2.to_m(), 0.75);
assert_eq!(d2.to_mm(), 750.0);

let total = d1 + d2;
assert_eq!(total.to_m(), 3.25);
assert_eq!(total.to_mm(), 3250.0);
```

What is happening:

- `d1` and `d2` are both `Distance<f64>`
- one was created from meters
- one was created from millimeters
- both are normalized into the same internal SI representation
- addition works because they are the same physical type

## Example 2: Working with feet

Important limitation:

- this crate does not currently provide `Distance::from_ft()` or `Distance::to_ft()`
- I confirmed there are no built-in feet conversion helpers for `Distance`

So the safe pattern is:

1. convert feet to meters yourself at the boundary
2. store and operate as `Distance<f64>`
3. convert back to feet when presenting output

```rust
use simple_si_units::base::Distance;

const METERS_PER_FOOT: f64 = 0.3048;
const FEET_PER_METER: f64 = 1.0 / METERS_PER_FOOT;

let doorway_ft = 6.5;
let doorway = Distance::from_m(doorway_ft * METERS_PER_FOOT);

assert!((doorway.to_m() - 1.9812).abs() < 1e-12);

let doorway_mm = doorway.to_mm();
assert!((doorway_mm - 1981.2).abs() < 1e-12);

let back_to_ft = doorway.to_m() * FEET_PER_METER;
assert!((back_to_ft - 6.5).abs() < 1e-12);
```

This still gives you type safety for the rest of the program:

```rust
use simple_si_units::base::Distance;

const METERS_PER_FOOT: f64 = 0.3048;

let board = Distance::from_m(8.0 * METERS_PER_FOOT); // 8 ft board
let trim = Distance::from_mm(125.0);                 // 125 mm trim cut
let remaining = board - trim;

println!("Remaining: {} m", remaining.to_m());
println!("Remaining: {} mm", remaining.to_mm());
```

## Example 3: Distance plus time gives velocity

This library encodes relationships between quantities as operator implementations.

Relevant API:

- [Distance / Time -> Velocity](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2432)
- [Velocity::from_mps](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25739)
- [Velocity::to_mps](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25742)

```rust
use simple_si_units::base::{Distance, Time};
use simple_si_units::mechanical::Velocity;

let distance = Distance::from_m(120.0);
let elapsed = Time::from_s(10.0);

let speed: Velocity<f64> = distance / elapsed;

assert_eq!(speed.to_mps(), 12.0);
```

The key point is that the result is not another `Distance<f64>`, and not a raw `f64`. It is a different type:

```rust
let speed: Velocity<f64> = Distance::from_m(120.0) / Time::from_s(10.0);
```

That prevents mixing up “length” and “speed” in later APIs.

## Example 4: Velocity back to distance

The reverse relationship is also encoded:

- [Velocity * Time -> Distance](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:26141)

```rust
use simple_si_units::base::{Distance, Time};
use simple_si_units::mechanical::Velocity;

let speed = Velocity::from_mps(3.0);
let duration = Time::from_s(15.0);

let distance: Distance<f64> = speed * duration;

assert_eq!(distance.to_m(), 45.0);
```

This is useful when you want APIs to stay physically meaningful:

- inputs are `Velocity` and `Time`
- output is `Distance`

## Example 5: Velocity divided by time gives acceleration

Relevant API:

- [Velocity / Time -> Acceleration](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:26171)
- [Acceleration::from_mps2](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:43)
- [Acceleration::to_mps2](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:46)

```rust
use simple_si_units::base::Time;
use simple_si_units::mechanical::{Velocity, Acceleration};

let v0 = Velocity::from_mps(30.0);
let dt = Time::from_s(6.0);

let accel: Acceleration<f64> = v0 / dt;

assert_eq!(accel.to_mps2(), 5.0);
```

So the derivative chain is:

1. `Distance / Time -> Velocity`
2. `Velocity / Time -> Acceleration`

## Example 6: Full derivative chain from distance to velocity to acceleration

```rust
use simple_si_units::base::{Distance, Time};
use simple_si_units::mechanical::{Velocity, Acceleration};

let dx = Distance::from_m(100.0);
let dt1 = Time::from_s(20.0);
let dt2 = Time::from_s(4.0);

let velocity: Velocity<f64> = dx / dt1;
let acceleration: Acceleration<f64> = velocity / dt2;

assert_eq!(velocity.to_mps(), 5.0);
assert_eq!(acceleration.to_mps2(), 1.25);
```

Written as units:

- `100 m / 20 s = 5 m/s`
- `5 m/s / 4 s = 1.25 m/s²`

That is exactly the type-level model the crate is enforcing.

## Example 7: Related non-SI display units on derived types

Some derived types do include common non-SI convenience conversions even where `Distance` itself does not.

For example `Velocity` supports miles per hour:

- [Velocity::from_mph](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25844)
- [Velocity::to_mph](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25834)

```rust
use simple_si_units::mechanical::Velocity;

let highway = Velocity::from_mph(60.0);

assert!((highway.to_mps() - 26.8224).abs() < 1e-12);
assert!((highway.to_mph() - 60.0).abs() < 1e-12);
```

This is a good example of the general pattern:

- canonical SI storage internally
- alternate convenience conversions at the API edge

## Practical rules

### Rule 1: Choose the quantity type first

Pick the physical concept you mean:

- `Distance<f64>`
- `Time<f64>`
- `Velocity<f64>`
- `Acceleration<f64>`

Do not start from `f64` and try to remember what it means later.

### Rule 2: Use SI internally

Even when constructing from `mm`, `mph`, or manual `ft` conversion, the value gets normalized into canonical SI storage. That keeps arithmetic consistent.

### Rule 3: Convert at boundaries

Use:

- `from_*` when reading input
- `to_*` when presenting output

If a unit is not built in, like feet for `Distance`, do the conversion once at the boundary and keep the rest of the code typed.

### Rule 4: Let operators produce the next physical type

Examples:

- `Distance / Time -> Velocity`
- `Velocity * Time -> Distance`
- `Velocity / Time -> Acceleration`

That is the main value of the crate.

## Caveat on numeric types

Conversions like `from_mm`, `to_mm`, `from_mph`, and many other convenience helpers live on impl blocks requiring `T: NumLike + From<f64>`, for example [Distance conversions](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2078) and [Velocity conversions](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/mechanical.rs:25761).

That means:

- `Distance<f64>` works well
- `Distance<f32>` does not get every convenience conversion, because `f32` does not implement `From<f64>`

The canonical constructors like `from_m`, `from_s`, `from_mps`, and `from_mps2` remain simpler and more broadly available.
