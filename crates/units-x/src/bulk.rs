use crate::generated::catalog_metadata::{CatalogJsonEncoding, DIMENSIONS};
use crate::model::UnitMarker;
use core::marker::PhantomData;

#[allow(dead_code)]
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum BulkKind {
    Array,
    Buffer,
    BufferView,
}

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum BulkClassification {
    SmallArray,
    Buffer,
}

pub trait BulkStorage: Copy + 'static {
    const STORAGE_ID: &'static str;
}

#[doc(hidden)]
pub trait BulkStorageFor<Unit>: BulkStorage
where
    Unit: UnitMarker,
{
}

impl BulkStorage for i32 {
    const STORAGE_ID: &'static str = "i32";
}

impl BulkStorage for f32 {
    const STORAGE_ID: &'static str = "f32";
}

impl BulkStorage for f64 {
    const STORAGE_ID: &'static str = "f64";
}

include!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/src/generated/bulk_storage_impls.rs"
));

#[allow(dead_code)]
pub const BULK_REVIEW_ARITIES: &[usize] = &[0, 2, 3, 4];

#[repr(transparent)]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct QuantityArray<Unit, T, const N: usize>
where
    Unit: UnitMarker,
{
    pub values: [T; N],
    _unit: PhantomData<Unit>,
}

#[repr(transparent)]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct QuantityBuffer<Unit, T>
where
    Unit: UnitMarker,
{
    pub values: Vec<T>,
    _unit: PhantomData<Unit>,
}

#[repr(transparent)]
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub struct QuantityBufferView<'a, Unit, T>
where
    Unit: UnitMarker,
{
    pub values: &'a [T],
    _unit: PhantomData<Unit>,
}

impl<Unit, T, const N: usize> QuantityArray<Unit, T, { N }>
where
    Unit: UnitMarker,
    T: BulkStorageFor<Unit>,
{
    pub const fn new(values: [T; N]) -> Self {
        Self {
            values,
            _unit: PhantomData,
        }
    }

    pub const fn unit(&self) -> &'static str {
        Unit::UNIT_SYMBOL
    }

    pub const fn unit_code_id(&self) -> &'static str {
        Unit::UNIT_CODE_ID
    }

    pub const fn public_type(&self) -> &'static str {
        Unit::PUBLIC_TYPE
    }

    pub const fn len(&self) -> usize {
        N
    }

    pub const fn is_empty(&self) -> bool {
        N == 0
    }

    pub const fn classification(&self) -> BulkClassification {
        BulkClassification::SmallArray
    }

    pub fn type_id(&self) -> String {
        render_small_array_type_id::<Unit, T>(N)
    }

    pub const fn as_slice(&self) -> &[T] {
        &self.values
    }

    pub fn into_inner(self) -> [T; N] {
        self.values
    }
}

impl<Unit, T> QuantityBuffer<Unit, T>
where
    Unit: UnitMarker,
    T: BulkStorageFor<Unit>,
{
    pub fn new(values: Vec<T>) -> Self {
        Self {
            values,
            _unit: PhantomData,
        }
    }

    pub const fn unit(&self) -> &'static str {
        Unit::UNIT_SYMBOL
    }

    pub const fn unit_code_id(&self) -> &'static str {
        Unit::UNIT_CODE_ID
    }

    pub const fn public_type(&self) -> &'static str {
        Unit::PUBLIC_TYPE
    }

    pub fn len(&self) -> usize {
        self.values.len()
    }

    pub fn is_empty(&self) -> bool {
        self.values.is_empty()
    }

    pub const fn classification(&self) -> BulkClassification {
        BulkClassification::Buffer
    }

    pub fn type_id(&self) -> String {
        render_buffer_type_id::<Unit, T>()
    }

    pub fn as_slice(&self) -> &[T] {
        &self.values
    }

    pub fn into_inner(self) -> Vec<T> {
        self.values
    }
}

impl<'a, Unit, T> QuantityBufferView<'a, Unit, T>
where
    Unit: UnitMarker,
    T: BulkStorageFor<Unit>,
{
    pub const fn new(values: &'a [T]) -> Self {
        Self {
            values,
            _unit: PhantomData,
        }
    }

    pub const fn unit(&self) -> &'static str {
        Unit::UNIT_SYMBOL
    }

    pub const fn unit_code_id(&self) -> &'static str {
        Unit::UNIT_CODE_ID
    }

    pub const fn public_type(&self) -> &'static str {
        Unit::PUBLIC_TYPE
    }

    pub const fn len(&self) -> usize {
        self.values.len()
    }

    pub const fn is_empty(&self) -> bool {
        self.values.is_empty()
    }

    pub const fn classification(&self) -> BulkClassification {
        BulkClassification::Buffer
    }

    pub fn type_id(&self) -> String {
        render_buffer_type_id::<Unit, T>()
    }

    pub const fn as_slice(&self) -> &'a [T] {
        self.values
    }
}

#[cfg_attr(not(test), allow(dead_code))]
pub fn bulk_encoding_for_unit<Unit>(bulk_kind: BulkKind) -> CatalogJsonEncoding
where
    Unit: UnitMarker,
{
    let dimension = DIMENSIONS
        .iter()
        .find(|dimension| dimension.public_type == Unit::PUBLIC_TYPE)
        .expect("generated catalog metadata must include the public type");
    match bulk_kind {
        BulkKind::Array => dimension.small_array_encoding,
        BulkKind::Buffer | BulkKind::BufferView => dimension.buffer_encoding,
    }
}

pub fn render_small_array_type_id<Unit, T>(arity: usize) -> String
where
    Unit: UnitMarker,
    T: BulkStorageFor<Unit>,
{
    let dimension = DIMENSIONS
        .iter()
        .find(|dimension| dimension.public_type == Unit::PUBLIC_TYPE)
        .expect("generated catalog metadata must include the public type");
    dimension
        .small_array_type_id_template
        .as_str()
        .replace("{arity}", &arity.to_string())
        .replace("{storage}", T::STORAGE_ID)
}

pub fn render_buffer_type_id<Unit, T>() -> String
where
    Unit: UnitMarker,
    T: BulkStorageFor<Unit>,
{
    let dimension = DIMENSIONS
        .iter()
        .find(|dimension| dimension.public_type == Unit::PUBLIC_TYPE)
        .expect("generated catalog metadata must include the public type");
    dimension
        .buffer_type_id_template
        .as_str()
        .replace("{storage}", T::STORAGE_ID)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::catalog_metadata::CatalogJsonEncoding;
    use crate::generated::public_types::{dpt, mm};
    use core::mem::{align_of, size_of};

    #[test]
    fn zero_length_bulk_forms_are_supported() {
        let array = QuantityArray::<mm, i32, 0>::new([]);
        assert!(array.is_empty());
        assert_eq!(array.len(), 0);

        let buffer = QuantityBuffer::<mm, i32>::new(Vec::new());
        assert!(buffer.is_empty());

        let view = QuantityBufferView::<mm, i32>::new(&[]);
        assert!(view.is_empty());
    }

    #[test]
    fn borrowed_and_owned_bulk_forms_expose_distinct_shapes() {
        let owned = QuantityBuffer::<mm, i32>::new(vec![1, 2, 3]);
        let view = QuantityBufferView::<mm, i32>::new(owned.as_slice());
        let array = QuantityArray::<mm, i32, 3>::new([1, 2, 3]);

        assert_eq!(owned.unit(), "mm");
        assert_eq!(view.unit_code_id(), "mm");
        assert_eq!(array.public_type(), "Distance");
        assert_eq!(view.as_slice(), &[1, 2, 3]);
    }

    #[test]
    fn wrappers_have_no_per_element_overhead() {
        assert_eq!(
            size_of::<QuantityArray<mm, i32, 4>>(),
            size_of::<[i32; 4]>()
        );
        assert_eq!(
            align_of::<QuantityArray<mm, i32, 4>>(),
            align_of::<[i32; 4]>()
        );

        assert_eq!(size_of::<QuantityBuffer<mm, i32>>(), size_of::<Vec<i32>>());
        assert_eq!(
            align_of::<QuantityBuffer<mm, i32>>(),
            align_of::<Vec<i32>>()
        );

        assert_eq!(
            size_of::<QuantityBufferView<'static, mm, i32>>(),
            size_of::<&[i32]>()
        );
        assert_eq!(
            align_of::<QuantityBufferView<'static, mm, i32>>(),
            align_of::<&[i32]>()
        );
    }

    #[test]
    fn catalog_owned_classification_is_exposed() {
        let array = QuantityArray::<mm, i32, 4>::new([1, 2, 3, 4]);
        let buffer = QuantityBuffer::<dpt, f64>::new(vec![1.0, 2.0]);

        assert_eq!(array.classification(), BulkClassification::SmallArray);
        assert_eq!(buffer.classification(), BulkClassification::Buffer);
        assert_eq!(
            bulk_encoding_for_unit::<mm>(BulkKind::Array),
            CatalogJsonEncoding::Array
        );
        assert_eq!(
            bulk_encoding_for_unit::<dpt>(BulkKind::Buffer),
            CatalogJsonEncoding::Base64Le
        );
        assert_eq!(array.type_id(), "distance4_i32");
        assert_eq!(buffer.type_id(), "diopter_buffer_f64");
    }
}
