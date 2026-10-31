"""
rental_system.py
----------------
The "brain" of the application. It stores all vehicles, customers,
employees and rentals, and connects them together.

OOP concepts shown here:
  - Composition / many objects : the system holds lists of objects
  - __new__()     : only ONE RentalSystem object can ever exist (singleton)
  - Class method  : change_company_name()
  - Static method : is_valid_days()
  - *args         : add_vehicles(*vehicles)
  - __len__()     : len(system)          -> number of available vehicles
  - __contains__(): "V001" in system      -> is this vehicle available?
  - __iter__()    : for v in system:      -> loop over available vehicles
  - __next__()    : used by AvailableVehicleIterator
  - __call__()    : system()              -> generates the rental report
"""

from car import VehicleFactory
from customer import Customer
from employee import Employee, Manager, Mechanic
from rental import Rental
from payment import Payment, process_payment
from utilities import format_money
from exceptions import (VehicleNotFoundError, VehicleNotAvailableError,
                        CustomerNotFoundError, CarRentalError)


class AvailableVehicleIterator:
    """A custom iterator that gives back only AVAILABLE vehicles, one by one."""

    def __init__(self, vehicles):
        self._vehicles = [v for v in vehicles if v.get_availability()]
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._vehicles):
            raise StopIteration            # tells the for loop to stop
        vehicle = self._vehicles[self._index]
        self._index += 1
        return vehicle


class RentalSystem:
    company_name = "City Car Rentals"      # class attribute
    _instance = None                       # stores the single object

    def __new__(cls):
        # __new__ CREATES the object (it runs before __init__).
        # Here we make sure only one RentalSystem is ever created.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ready = False
        return cls._instance

    def __init__(self):
        if self._ready:                    # already set up -> do not reset the data
            return
        self.vehicles = []
        self.customers = []
        self.employees = []
        self.rentals = []
        self._ready = True

    # ---------- Class method and static methods ----------
    @classmethod
    def change_company_name(cls, new_name):
        cls.company_name = new_name

    @staticmethod
    def is_valid_days(days):
        return 1 <= days <= 30

    @staticmethod
    def _make_id(prefix, existing_ids):
        """Make the next free ID, e.g. V007 or C004."""
        number = 1
        while f"{prefix}{number:03d}" in existing_ids:
            number += 1
        return f"{prefix}{number:03d}"

    # ---------- Customers ----------
    def add_customer(self, customer):
        self.customers.append(customer)

    def register_customer(self, name, phone, license_number):
        customer_id = self._make_id("C", [c.customer_id for c in self.customers])
        customer = Customer(customer_id, name, phone, license_number)
        self.add_customer(customer)
        return customer

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id.upper():
                return customer
        raise CustomerNotFoundError(customer_id)

    # ---------- Vehicles ----------
    def add_vehicles(self, *vehicles):
        """*args: add one vehicle or many vehicles in one call."""
        for vehicle in vehicles:
            self.vehicles.append(vehicle)

    def add_new_vehicle(self, vehicle_type, brand, model, year, daily_rate):
        vehicle_id = self._make_id("V", [v.vehicle_id for v in self.vehicles])
        vehicle = VehicleFactory.create_vehicle(vehicle_type, vehicle_id, brand, model, year, daily_rate)
        self.add_vehicles(vehicle)
        return vehicle

    def find_vehicle(self, vehicle_id):
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id.upper():
                return vehicle
        raise VehicleNotFoundError(vehicle_id)

    def remove_vehicle(self, vehicle_id):
        vehicle = self.find_vehicle(vehicle_id)
        if not vehicle.get_availability():
            raise CarRentalError("Cannot remove a vehicle that is currently rented.")
        self.vehicles.remove(vehicle)
        return vehicle

    def search_vehicles(self, keyword):
        keyword = keyword.lower()
        return [v for v in self.vehicles
                if keyword in v.brand.lower() or keyword in v.model.lower()
                or keyword in v.vehicle_type().lower()]

    # ---------- Employees ----------
    def add_employee(self, role, name, phone, salary, extra=""):
        employee_id = self._make_id("E", [e.employee_id for e in self.employees])
        if role == "manager":
            employee = Manager(employee_id, name, phone, salary, extra)
        elif role == "mechanic":
            employee = Mechanic(employee_id, name, phone, salary, extra)
        else:
            employee = Employee(employee_id, name, phone, salary)
        self.employees.append(employee)
        return employee

    # ---------- Renting and returning ----------
    def rent_vehicle(self, customer_id, vehicle_id, days, payment_method):
        if not RentalSystem.is_valid_days(days):
            raise CarRentalError("Rental days must be between 1 and 30.")

        customer = self.find_customer(customer_id)
        vehicle = self.find_vehicle(vehicle_id)
        if vehicle.vehicle_id not in self:          # uses __contains__
            raise VehicleNotAvailableError(vehicle.vehicle_id)

        # Loyal customers (2 or more old rentals) get 10% discount
        discount = 10 if len(customer.rental_history) >= 2 else 0

        rental = Rental(customer, vehicle, days).apply_discount(discount)   # method chaining
        invoice = rental.generate_invoice()

        payment = Payment.create(payment_method, invoice.total, customer.name)  # factory
        process_payment(payment)                                                # duck typing
        rental.payment = payment

        vehicle.set_availability(False)
        customer.add_rental(rental)
        self.rentals.append(rental)
        return rental

    def return_vehicle(self, vehicle_id):
        vehicle = self.find_vehicle(vehicle_id)
        for rental in self.rentals:
            if rental.vehicle == vehicle and rental.is_active:   # uses Vehicle.__eq__
                rental.close()
                return rental
        raise CarRentalError(f"Vehicle '{vehicle.vehicle_id}' is not rented right now.")

    def quote(self, vehicle_id, days):
        """Calculate the price without renting (polymorphism)."""
        vehicle = self.find_vehicle(vehicle_id)
        return vehicle, vehicle.calculate_rent(days)

    # ---------- Magic methods ----------
    def __len__(self):
        return len([v for v in self.vehicles if v.get_availability()])

    def __contains__(self, vehicle_id):
        return any(v.vehicle_id == vehicle_id and v.get_availability() for v in self.vehicles)

    def __iter__(self):
        return AvailableVehicleIterator(self.vehicles)

    def __call__(self):
        """Calling the object like a function makes the report."""
        payments = [r.payment for r in self.rentals if r.payment]
        total_revenue = sum(payments)              # works because of Payment.__radd__
        active = [r for r in self.rentals if r.is_active]

        lines = ["=" * 60,
                 f"RENTAL REPORT - {self.company_name}".center(60),
                 "=" * 60,
                 f"Total vehicles      : {len(self.vehicles)}",
                 f"Available vehicles  : {len(self)}",
                 f"Rented vehicles     : {len(self.vehicles) - len(self)}",
                 f"Customers           : {len(self.customers)}",
                 f"Employees           : {len(self.employees)}",
                 f"Total rentals       : {len(self.rentals)}",
                 f"Active rentals      : {len(active)}",
                 f"Total revenue       : {format_money(total_revenue)}"]
        if payments:
            lines.append(f"Biggest payment     : {max(payments)}")   # uses Payment.__gt__
        lines.append("-" * 60)
        lines.append("Rental history:")
        if not self.rentals:
            lines.append("  No rentals yet.")
        for rental in self.rentals:
            lines.append("  " + str(rental))
        lines.append("=" * 60)
        return "\n".join(lines)
