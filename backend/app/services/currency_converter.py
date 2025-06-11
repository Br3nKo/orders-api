import os

import httpx
from fastapi import HTTPException


def get_exchange_api_url() -> str:
    """Load the exchange API URL"""
    return os.getenv("EXCHANGE_API_URL", "https://api.currencyapi.com/v3/latest")


def get_exchange_api_key() -> str:
    """Load the exchange API key"""
    return os.getenv("EXCHANGE_API_KEY", "")


BASE_URL = get_exchange_api_url()
API_KEY = get_exchange_api_key()

"""
Service for fetching currency exchange rates from an external API.
"""


async def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Get the exchange rate from base_currency to target_currency using currencyapi.com.
    Returns 1.0 if both currencies are the same.
    Raises HTTPException for network, API, or data errors.
    """
    if hasattr(base_currency, "value"):
        base_currency = base_currency.value
    if hasattr(target_currency, "value"):
        target_currency = target_currency.value
    if base_currency == target_currency:
        return 1.0

    params = {
        "apikey": API_KEY,
        "base_currency": base_currency,
        "currencies": target_currency,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
            data = response.json()
            print(data)
            if not data.get("success", True):
                raise HTTPException(
                    status_code=400,
                    detail=data.get("error", {}).get("info", "Currency API error"),
                )
            key = f"{target_currency}"
            quotes = data.get("data", {})
            if key not in quotes:
                raise HTTPException(
                    status_code=404, detail=f"Exchange rate for {key} not found."
                )
            return quotes[key]["value"]

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Currency API request failed: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during currency conversion: {str(e)}",
        )
