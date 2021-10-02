from dataclasses import dataclass
from typing import Optional, Union

from pandas import Series

from sheets import helpers
from sheets.errors import ColumnNotFoundError, OrderNotFound


@dataclass
class ResponseForm:
    A: str = "Timestamp"
    B: str = "Merchant"
    C: str = "Payment Status"
    D: str = "Send Credit Status"
    E: str = "Remarks"
    F: str = "Mode of Payment"
    G: str = "Sender Name"
    H: str = "Select your order"
    I: str = "Name"
    J: str = "GAME ID"
    K: str = "Mobile number"
    L: str = "Facebook Link(Optional)"
    M: str = "Cost"
    N: str = "Price"
    O: str = "Net"
    P: str = "Deduction"
    Q: str = "Upload your proof of payment"

    def reverse(self) -> dict:
        return {v: k for k, v in self.__dict__.items()}

    def get_coordinates(self, index, header: str) -> str:
        row = str(index)
        column = self.reverse().get(header)

        if not column:
            raise ColumnNotFoundError(f"Column {header} not found on google sheets!")

        return column + row


@dataclass
class GemOrder:
    gem_amount: int
    srp: Union[int, float]
    price: Union[int, float]
    cost: Union[int, float]

    @classmethod
    def from_str(cls, order: str):
        if order == "32 Force Gems(48 PHP)":
            return cls(32, 49, 48, 45.82)
        elif order == "68 Force Gems(97 PHP)":
            return cls(68, 99, 97, 92.57)
        elif order == "215 ForceGems(292 PHP)":
            return cls(215, 299, 292, 279.57)
        elif order == "368 ForceGems(487 PHP)":
            return cls(368, 499, 487, 466.57)
        elif order == "788 Diamond(974 PHP)":
            return cls(788, 999, 974, 934.07)
        elif order == "2011 ForceGems(2428 PHP)":
            return cls(2011, 2490, 2428, 2328.15)
        elif order == "4195 ForceGems(4865 PHP)":
            return cls(4195, 4990, 4865, 4666.65)

        raise OrderNotFound(f"Order '{order}' is not a valid order!")


@dataclass
class OrderDetails:
    sheet_index: int
    timestamp: str
    merchant: str
    payment_status: str
    send_credit_status: str
    remarks: str
    mode_of_payment: str
    sender_name: str
    order: GemOrder
    name: str
    uid: str
    mobile_number: str
    facebook_link: Optional[str]
    cost: float
    price: float
    net: float
    deduction: float
    proof_of_payment: str

    @classmethod
    def from_row_series(cls, sheet_index: int, row: Series):
        header = ResponseForm()
        cost = helpers.currency_to_float(row[f" {header.M} "])
        price = helpers.currency_to_float(row[f" {header.N} "])
        net = helpers.currency_to_float(row[f" {header.O} "])
        deduction = helpers.currency_to_float(row[f" {header.P} "])

        return cls(
            sheet_index=sheet_index,
            timestamp=row[header.A],
            merchant=row[header.B],
            payment_status=row[header.C],
            send_credit_status=row[header.D],
            remarks=row[header.E],
            mode_of_payment=row[header.F],
            sender_name=row[header.G],
            order=GemOrder.from_str(row[header.H]),
            name=row[header.I],
            uid=row[header.J],
            mobile_number=row[header.K],
            facebook_link=row[header.L],
            cost=cost,
            price=price,
            net=net,
            deduction=deduction,
            proof_of_payment=row[header.Q],
        )


@dataclass
class SpreadSheetInfo:
    id: str
    title: str
    range: str
    worksheet: str
