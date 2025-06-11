from decimal import Decimal

from currencies import Currency
from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    price: Decimal = Field(..., gt=0)
    currency: Currency

    @field_validator("customer_name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Customer name cannot be empty.")
        return v


class OrderOut(BaseModel):
    id: int
    customer_name: str
    price: Decimal
    currency: Currency

    model_config = ConfigDict(from_attributes=True)


class OrderUpdate(BaseModel):
    currency: Currency
