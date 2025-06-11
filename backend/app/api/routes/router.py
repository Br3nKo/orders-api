from fastapi import APIRouter
from app.api.dependencies.core import DBSessionDep
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate, Currency
from typing import Optional
from app.crud.order import (
    create_order_db,
    get_order_db,
    get_all_orders_db,
    update_order_db,
    delete_order_db,
)

router = APIRouter()


@router.post("/orders", response_model=OrderOut)
async def create_order(order_in: OrderCreate, session: DBSessionDep) -> OrderOut:
    """Create a new order."""
    return await create_order_db(session, order_in)


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int, session: DBSessionDep, to_currency: Optional[Currency] = None
) -> OrderOut:
    """Get an order by ID. Optionally convert to another currency."""
    return await get_order_db(session, order_id, to_currency)


@router.get("/orders", response_model=list[OrderOut])
async def get_all_orders(
    session: DBSessionDep, to_currency: Optional[Currency] = None
) -> list[OrderOut]:
    """Get all orders. Optionally convert to another currency."""
    return await get_all_orders_db(session, to_currency)


@router.put("/orders/{order_id}", response_model=OrderOut)
async def update_order(
    order_id: int, order_in: OrderUpdate, session: DBSessionDep
) -> OrderOut:
    """Update the currency of an order."""
    return await update_order_db(session, order_id, order_in)


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, session: DBSessionDep) -> None:
    """Delete an order by ID."""
    return await delete_order_db(session, order_id)
