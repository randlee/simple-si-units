# Sprint A-2: Master Catalog And Codegen Reuse Plan

## Goal

Define the master catalog and isolate what can be reused from the existing project as generation inputs for the new crate.

## Status

`Not Started`

## Deliverables

1. Mapping from current CSV unit definitions to the new crate model
2. Mapping from current conversion-factor generation to the new storage-preserving model
3. Master catalog schema
4. Catalog fields covering JSON type ids, human-readable unit symbols, code-facing unit ids, binary schema ids, ABI naming inputs, reserved-word strategy, and offset-conversion metadata
5. List of codegen components to reuse, adapt, or replace
6. End-user extension workflow based on catalog edits plus regeneration

## Why

The current project contains valuable unit metadata and operator relationships, but its storage model is not the new product model. The new architecture should promote the catalog itself to the primary source of truth.

## Dependencies

- Sprint A-1

## Unblocks

- Sprint B-2
- Sprint B-3
- Sprint C-1
- Sprint C-2

## Parallelism

- Can run in parallel with Sprint A-4 after Sprint A-1

## Exit Criteria

1. Reusable data sources are identified.
2. Master catalog schema is explicit.
3. Codegen adaptation scope is explicit.
4. The end-user unit-extension workflow is documented.
