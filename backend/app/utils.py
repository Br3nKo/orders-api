import os
from typing import Optional

from currencies import Currency
from services.currency_converter import get_exchange_rate


def get_url() -> Optional[str]:
    """Load the DATABASE_URL"""
    return os.getenv("DATABASE_URL")


async def modify_order_by_currency(order: object, to_currency: Currency) -> object:
    """
    Convert an order's price to a target currency using the exchange rate service.
    If the currency is unchanged, returns the order as is.
    """
    if order.currency == to_currency:
        return order

    exchange_rate = await get_exchange_rate(order.currency, to_currency)

    if exchange_rate is None:
        raise ValueError(
            f"Exchange rate for {order.currency} to {to_currency} not found."
        )

    order.price = round(float(order.price) * exchange_rate, 2)
    order.currency = to_currency

    return order
