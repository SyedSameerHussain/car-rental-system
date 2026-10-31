"""
interfaces.py
-------------
Abstract classes that work like "rules" (interfaces) for other classes.

OOP concepts shown here:
  - Abstraction      : we say WHAT a class must do, not HOW it does it
  - ABC              : Abstract Base Class from the abc module
  - Abstract methods : methods with no body that child classes MUST write

You can NOT create an object of an abstract class:
    Rentable()  -> TypeError
"""

from abc import ABC, abstractmethod


class Rentable(ABC):
    """Anything that can be rented MUST have these two methods."""

    @abstractmethod
    def calculate_rent(self, days):
        """Return the rent for the given number of days."""
        pass

    @abstractmethod
    def get_details(self):
        """Return a one-line description of the item."""
        pass


class Payable(ABC):
    """Anything that is a payment method MUST have a pay() method."""

    @abstractmethod
    def pay(self):
        """Perform the payment and return True if it worked."""
        pass
