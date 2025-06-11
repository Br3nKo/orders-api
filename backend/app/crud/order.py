from typing import Optional

from currencies import Currency
from fastapi import HTTPException
from models.order import Order
from schemas.order import OrderCreate, OrderOut, OrderUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import modify_order_by_currency


async def create_order_db(session: AsyncSession, order_in: OrderCreate) -> OrderOut:
    """
    Create a new order in the database.
    Args:
        session (AsyncSession): SQLAlchemy async session.
        order_in (OrderCreate): Pydantic schema with order data.
    Returns:
        OrderOut: The created order as a Pydantic schema.
    """
    order_data = order_in.model_dump()
    order = Order(
        customer_name=order_data["customer_name"],
        price=order_data["price"],
        currency=(
            order_data["currency"].value
            if hasattr(order_data["currency"], "value")
            else order_data["currency"]
        ),
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    return OrderOut.model_validate(order)


async def get_order_db(
    session: AsyncSession, order_id: int, to_currency: Optional[Currency] = None
) -> OrderOut:
    """
    Retrieve a single order by ID, optionally converting its price to a target currency.
    Args:
        session (AsyncSession): SQLAlchemy async session.
        order_id (int): The ID of the order to retrieve.
        to_currency: Optional target currency for conversion.
    Returns:
        OrderOut: The order as a Pydantic schema, possibly with converted price/currency.
    """
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if to_currency:
        order = await modify_order_by_currency(order, to_currency)

    return OrderOut.model_validate(order)


async def get_all_orders_db(
    session: AsyncSession, to_currency: Optional[Currency] = None
) -> list[OrderOut]:
    """
    Retrieve all orders, optionally converting their prices to a target currency.
    Args:
        session (AsyncSession): SQLAlchemy async session.
        to_currency: Optional target currency for conversion.
    Returns:
        list[OrderOut]: List of orders as Pydantic schemas, possibly with converted prices/currencies.
    """
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    if to_currency:
        orders = [
            await modify_order_by_currency(order, to_currency) for order in orders
        ]

    print(f"Orders: {orders}")
    return [OrderOut.model_validate(order) for order in orders]


async def update_order_db(
    session: AsyncSession, order_id: int, order_in: OrderUpdate
) -> OrderOut:
    """
    Update the currency (and price) of an order by ID.
    Args:
        session (AsyncSession): SQLAlchemy async session.
        order_id (int): The ID of the order to update.
        order_in (OrderUpdate): Pydantic schema with new currency.
    Returns:
        OrderOut: The updated order as a Pydantic schema.
    Raises:
        HTTPException: If the order is not found or the currency is unchanged.
    """
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    new_currency = order_in.currency
    if order.currency == new_currency:
        raise HTTPException(
            status_code=400,
            detail="Currency is the same as the current one. Nothing to update.",
        )

    order = await modify_order_by_currency(order, new_currency)

    session.add(order)
    await session.commit()
    await session.refresh(order)

    return OrderOut.model_validate(order)


async def delete_order_db(session: AsyncSession, order_id: int) -> dict:
    """
    Delete an order by ID from the database.
    Args:
        session (AsyncSession): SQLAlchemy async session.
        order_id (int): The ID of the order to delete.
    Returns:
        dict: A message confirming deletion.
    Raises:
        HTTPException: If the order is not found.
    """
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.delete(order)
    await session.commit()
    return {"detail": f"Order {order_id} has been deleted."}
