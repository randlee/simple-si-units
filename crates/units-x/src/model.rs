use core::marker::PhantomData;

pub(crate) mod private {
    pub trait SealedUnit {}
    pub trait SealedQuantityType {}
}

#[repr(transparent)]
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub struct Quantity<Unit, Storage>
where
    Unit: UnitMarker,
{
    pub storage: Storage,
    _unit: PhantomData<Unit>,
}

impl<Unit, Storage> Quantity<Unit, Storage>
where
    Unit: UnitMarker,
{
    pub const fn new(storage: Storage) -> Self {
        Self {
            storage,
            _unit: PhantomData,
        }
    }

    pub const fn storage(&self) -> &Storage {
        &self.storage
    }

    pub fn storage_mut(&mut self) -> &mut Storage {
        &mut self.storage
    }

    pub fn into_storage(self) -> Storage {
        self.storage
    }
}

pub trait UnitMarker: private::SealedUnit + Copy + 'static {
    const UNIT_SYMBOL: &'static str;
    const UNIT_CODE_ID: &'static str;
    const DIMENSION_ID: &'static str;
    const CANONICAL_DIMENSION_ID: &'static str;
    const PUBLIC_TYPE: &'static str;
}

pub trait QuantityType: private::SealedQuantityType + Sized {
    type Storage;
    type Unit: UnitMarker;

    const PUBLIC_TYPE: &'static str;
    const DIMENSION_ID: &'static str;
    const CANONICAL_DIMENSION_ID: &'static str;

    fn from_quantity(quantity: Quantity<Self::Unit, Self::Storage>) -> Self;
    fn quantity(&self) -> &Quantity<Self::Unit, Self::Storage>;
    fn quantity_mut(&mut self) -> &mut Quantity<Self::Unit, Self::Storage>;
    fn into_quantity(self) -> Quantity<Self::Unit, Self::Storage>;
}
