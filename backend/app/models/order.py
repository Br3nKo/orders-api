from decimal import Decimal

from currencies import Currency
from database import Base
from sqlalchemy import Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False)

    def __repr__(self):
        return f"<Order(id={self.id}, customer_name='{self.customer_name}', price={self.price}, currency='{self.currency}')>"
