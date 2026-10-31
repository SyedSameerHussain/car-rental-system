"""
customer.py
-----------
Customer is a child class of Person.

OOP concepts shown here:
  - Inheritance (Person -> Customer) and super()
  - Class attribute : customer_count
  - Private attribute + getter/setter : __license_number
  - Static method   : validate_license()  (does not need self or cls)
  - Class method    : create_customer()   (alternative constructor, uses cls)
  - Method overloading (Python style) : display(show_history=False)
  - Method overriding : get_details()
"""

from person import Person
from exceptions import InvalidLicenseError


class Customer(Person):
    customer_count = 0                       # class attribute

    def __init__(self, customer_id, name, phone, license_number):
        super().__init__(name, phone)        # Person sets name and phone

        if not Customer.validate_license(license_number):
            raise InvalidLicenseError(license_number)

        self.customer_id = customer_id
        self.__license_number = license_number   # private
        self.rental_history = []                  # list of Rental objects
        Customer.customer_count += 1

    # ---------- Getter and setter for a private attribute ----------
    def get_license(self):
        return self.__license_number

    def set_license(self, new_license):
        if not Customer.validate_license(new_license):
            raise InvalidLicenseError(new_license)
        self.__license_number = new_license

    # ---------- Static method ----------
    @staticmethod
    def validate_license(license_number):
        """Valid format: 'DL-' + 5 digits, for example DL-12345."""
        return (len(license_number) == 8
                and license_number.startswith("DL-")
                and license_number[3:].isdigit())

    # ---------- Class method (alternative constructor) ----------
    @classmethod
    def create_customer(cls, data):
        """Create a customer from one text line:
        "C001, Ali Khan, 03001234567, DL-12345"
        """
        customer_id, name, phone, license_number = [part.strip() for part in data.split(",")]
        return cls(customer_id, name, phone, license_number)

    # ---------- Instance methods ----------
    def add_rental(self, rental):
        self.rental_history.append(rental)

    def total_spent(self):
        return sum(rental.total_amount for rental in self.rental_history)

    def get_details(self):
        # Method overriding: Customer gives more detail than Person
        return (f"[{self.customer_id}] {self.name:<15} | Phone: {self.phone} "
                f"| License: {self.get_license()} | Rentals: {len(self.rental_history)}")

    def display(self, show_history=False):
        """'Method overloading' with a default argument:
        display()                  -> only details
        display(show_history=True) -> details + rental history
        """
        print(self.get_details())
        if show_history:
            if not self.rental_history:
                print("    No rentals yet.")
            for rental in self.rental_history:
                print("   ", rental)
