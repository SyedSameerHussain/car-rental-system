"""
rental.py
---------
A Rental connects a Customer with a Vehicle.

OOP concepts shown here:
  - Aggregation  : a Rental USES a Customer and a Vehicle that already exist.
                   If the rental is removed, the customer and vehicle still exist.
  - Composition  : a Rental CREATES its own Invoice. The Invoice is a part of
                   the Rental and has no meaning without it.
  - Polymorphism : self.vehicle.calculate_rent() works for ANY vehicle type
  - Method chaining : Rental(...).set_days(5).apply_discount(10)
  - Class attribute : rental_counter (used to make IDs R001, R002, ...)
"""

from datetime import date
from utilities import format_money


class Invoice:
    """Part of a Rental (composition)."""

    def __init__(self, rental_id, base_amount, discount_amount):
        self.rental_id = rental_id
        self.base_amount = base_amount
        self.discount_amount = discount_amount

    @property
    def total(self):
        return self.base_amount - self.discount_amount

    def __str__(self):
        return (f"  Invoice for rental {self.rental_id}\n"
                f"  Base rent : {format_money(self.base_amount)}\n"
                f"  Discount  : -{format_money(self.discount_amount)}\n"
                f"  TOTAL     : {format_money(self.total)}")


class Rental:
    rental_counter = 0

    def __init__(self, customer, vehicle, days):
        Rental.rental_counter += 1
        self.rental_id = f"R{Rental.rental_counter:03d}"
        self.customer = customer          # aggregation
        self.vehicle = vehicle            # aggregation
        self.days = days
        self.discount_percent = 0
        self.start_date = date.today()
        self.return_date = None
        self.is_active = True
        self.payment = None
        self.invoice = None

    # ---------- Method chaining ----------
    def set_days(self, days):
        self.days = days
        return self

    def apply_discount(self, percent):
        self.discount_percent = percent
        return self

    # ---------- Composition ----------
    def generate_invoice(self):
        base = self.vehicle.calculate_rent(self.days)        # polymorphism
        discount = base * self.discount_percent / 100
        self.invoice = Invoice(self.rental_id, base, discount)  # Rental creates its Invoice
        return self.invoice

    @property
    def total_amount(self):
        if self.invoice is None:
            self.generate_invoice()
        return self.invoice.total

    def close(self):
        """Called when the vehicle is returned."""
        self.is_active = False
        self.return_date = date.today()
        self.vehicle.set_availability(True)

    def __str__(self):
        status = "Active" if self.is_active else "Returned"
        return (f"{self.rental_id} | {self.customer.name:<15} | {str(self.vehicle):<28} | "
                f"{self.days:>2} day(s) | {format_money(self.total_amount):>14} | {status}")
