"""
exceptions.py
-------------
Custom exceptions (our own error types) for the Car Rental System.

OOP concepts shown here:
  - Inheritance       : every custom exception is a child of Exception
  - Custom exceptions : we create our own error classes with clear messages
  - super()           : we call the parent (Exception) constructor
"""


class CarRentalError(Exception):
    """Parent class of ALL errors in this project.
    In main.py we can catch every project error with: except CarRentalError"""
    pass


class VehicleNotFoundError(CarRentalError):
    """Raised when a vehicle ID does not exist."""

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        super().__init__(f"Vehicle with ID '{vehicle_id}' was not found.")


class VehicleNotAvailableError(CarRentalError):
    """Raised when someone tries to rent a vehicle that is already rented."""

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        super().__init__(f"Vehicle '{vehicle_id}' is already rented.")


class CustomerNotFoundError(CarRentalError):
    """Raised when a customer ID does not exist."""

    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"Customer with ID '{customer_id}' was not found.")


class InvalidLicenseError(CarRentalError):
    """Raised when a driving license number has the wrong format."""

    def __init__(self, license_number):
        self.license_number = license_number
        super().__init__(f"Invalid driving license '{license_number}'. "
                         f"Correct format is DL- followed by 5 digits (e.g. DL-12345).")


class PaymentError(CarRentalError):
    """Raised when a payment cannot be made."""
    pass
