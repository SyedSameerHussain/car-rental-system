"""
person.py
---------
Person is the parent class of Customer and Employee.

OOP concepts shown here:
  - Class and Object
  - Constructor __init__()
  - self keyword
  - Class attribute vs Instance attribute
  - Encapsulation (protected attribute _phone + property)
  - Magic methods __str__ and __repr__
"""


class Person:
    # CLASS attribute: one value shared by every Person object
    total_persons = 0

    def __init__(self, name, phone):
        # INSTANCE attributes: every object has its own values
        self.name = name          # public attribute
        self.phone = phone        # goes through the phone setter below (validation)
        Person.total_persons += 1

    # ---------- Property (getter + setter) ----------
    @property
    def phone(self):
        return self._phone        # _phone is "protected"

    @phone.setter
    def phone(self, value):
        value = str(value).strip()
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Phone number must contain at least 10 digits only.")
        self._phone = value

    # ---------- Instance method ----------
    def get_details(self):
        return f"{self.name} | Phone: {self.phone}"

    # ---------- Magic methods ----------
    def __str__(self):
        # Used by print(person)
        return self.name

    def __repr__(self):
        # Used when the object is shown inside a list, or in the Python shell
        return f"{type(self).__name__}('{self.name}')"
