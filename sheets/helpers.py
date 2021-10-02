from re import sub
from decimal import Decimal


def currency_to_float(money: str):

    # money = '$6,150,593.22'
    value = Decimal(sub(r'[^\d.]', '', money))

    return float(value)
