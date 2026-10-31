"""
payment.py
----------
Different ways to pay for a rental.

OOP concepts shown here:
  - Abstraction / ABC   : Payment is abstract (pay() has no body)
  - Abstract method     : pay() must be written by each child class
  - Polymorphism        : CashPayment, CardPayment, OnlinePayment all have pay()
  - Operator overloading: +  ==  <  >  between payments
  - Factory method      : Payment.create("cash", ...) builds the right object
  - Duck typing         : GiftVoucher is NOT a Payment, but it has pay(),
                          so process_payment() can still use it.
"""

from abc import abstractmethod
from interfaces import Payable
from exceptions import PaymentError
from utilities import format_money


class Payment(Payable):

    def __init__(self, amount):
        if amount <= 0:
            raise PaymentError("Payment amount must be greater than zero.")
        self.amount = amount
        self.status = "Pending"

    @abstractmethod
    def pay(self):
        pass

    def method_name(self):
        return type(self).__name__.replace("Payment", "")   # "CashPayment" -> "Cash"

    # ---------- Operator overloading ----------
    def __add__(self, other):
        # payment1 + payment2  -> total amount
        if isinstance(other, Payment):
            return self.amount + other.amount
        if isinstance(other, (int, float)):
            return self.amount + other
        return NotImplemented

    def __radd__(self, other):
        # Lets us write: 0 + payment  -> this makes sum(list_of_payments) work
        return self.__add__(other)

    def __eq__(self, other):
        if not isinstance(other, Payment):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __str__(self):
        return f"{self.method_name()} payment of {format_money(self.amount)} [{self.status}]"

    # ---------- Factory method ----------
    @staticmethod
    def create(method, amount, payer_name):
        """Create the correct payment object from a simple word."""
        method = method.lower()
        if method == "cash":
            return CashPayment(amount)
        elif method == "card":
            return CardPayment(amount, payer_name)
        elif method == "online":
            return OnlinePayment(amount, "Mobile Wallet")
        raise PaymentError(f"Unknown payment method '{method}'.")


class CashPayment(Payment):
    def pay(self):
        self.status = "Paid"
        print(f"  Cash received: {format_money(self.amount)}")
        return True


class CardPayment(Payment):
    def __init__(self, amount, card_holder):
        super().__init__(amount)
        self.card_holder = card_holder

    def pay(self):
        self.status = "Paid"
        print(f"  Card payment of {format_money(self.amount)} approved for {self.card_holder}")
        return True


class OnlinePayment(Payment):
    def __init__(self, amount, wallet_name):
        super().__init__(amount)
        self.wallet_name = wallet_name

    def pay(self):
        self.status = "Paid"
        print(f"  Online payment of {format_money(self.amount)} received via {self.wallet_name}")
        return True


# ---------------------------------------------------------------
#  Duck typing
# ---------------------------------------------------------------
class GiftVoucher:
    """This class does NOT inherit from Payment.
    But it has a pay() method, so it "acts like" a payment.
    "If it walks like a duck and quacks like a duck, it is a duck." """

    def __init__(self, code, amount):
        self.code = code
        self.amount = amount

    def pay(self):
        print(f"  Gift voucher {self.code} used for {format_money(self.amount)}")
        return True


def process_payment(payment_object):
    """Works with ANY object that has a pay() method (duck typing).
    We do not check the type, we just call pay()."""
    return payment_object.pay()
