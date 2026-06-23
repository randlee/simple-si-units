# Sprint E-2: Python Buffer And Memoryview API

## Goal

Implement efficient Python bulk data APIs using buffers and memoryviews instead of Python object-per-element models, with the PyO3-native buffer API as the primary surface.

## Status

`Not Started`

## Scope References

- REQ-UX-003
- REQ-UX-004
- REQ-UX-013
- REQ-UX-016
- REQ-UX-021
- REQ-UX-032
- NFR-UX-002
- NFR-UX-003
- NFR-UX-007
- NFR-UX-013
- ADR-UX-004
- ADR-UX-005
- ADR-UX-014

## Deliverables

1. Buffer-oriented bulk quantity API
2. Memoryview-friendly path
3. Binary and metadata alignment with the project wire format
4. Clear distinction between the primary Python bulk API and any retained lower-level C ABI bridge for advanced use only
5. Explicit serialization relationship between Python bulk APIs and the canonical JSON/binary fixture contracts

## Dependencies

- Sprints B-4, C-2, C-3

## Unblocks

- Sprint E-3

## Acceptance Criteria

1. The primary Python bulk surface uses buffer-oriented APIs rather than Python object-per-element models.
2. Memoryview-friendly consumption is supported for the planned bulk surface.
3. The Python bulk contract is explicitly related to, but distinct from, the raw C ABI surface.
4. Bulk metadata and payload behavior align with the canonical wire rules.
5. Owned, borrowed, read-only, and mutable semantics are explicit for every shipped Python bulk API entry point.

## Required Validation

1. Dedicated tests prove no per-element Python object wrapping is required for the primary path.
2. Dedicated tests cover zero-length buffers.
3. Dedicated tests cover read-only versus mutable buffer semantics where both are exposed.
4. Dedicated tests reject non-contiguous or shape-mismatched inputs when the primary API requires contiguous typed buffers.
5. Validation ties each shipped bulk API entry point to the canonical JSON and binary fixture rules it must honor.

## Code Samples / Contracts

```python
arr = DistanceArray.mm_f32.from_buffer(memoryview(raw_values))
readonly_mv = arr.memoryview()

mutable = MutableDistanceArray.mm_f32.from_writable_buffer(memoryview(raw_mut))
mutable_mv = mutable.memoryview()

with pytest.raises(ValueError):
    DistanceArray.mm_f32.from_buffer(non_contiguous_values)
```
