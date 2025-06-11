from enum import Enum


class Currency(str, Enum):
    CZK = "CZK"
    USD = "USD"
    EUR = "EUR"
