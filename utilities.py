"""
utilities.py
------------
Helper functions and small demonstration classes.

OOP concepts shown here:
  - Dynamic attributes        : adding attributes to an object at run time
  - getattr / setattr / hasattr
  - __getattr__               : called when an attribute is NOT found
  - __setattr__               : called every time we assign an attribute
  - __delattr__               : called when we delete an attribute
  - __enter__ / __exit__      : context manager (used with the "with" keyword)
  - __del__                   : destructor (called when an object is destroyed)
"""


# ---------------------------------------------------------------
#  Simple helper functions for the CMD screen
# ---------------------------------------------------------------
def print_line(char="=", length=60):
    print(char * length)


def print_header(title):
    print()
    print_line()
    print(title.center(60))
    print_line()


def format_money(amount):
    """Turn 12500 into 'Rs.12,500.00'"""
    return f"Rs.{amount:,.2f}"


def get_text(prompt):
    """Keep asking until the user types something (not empty)."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty. Try again.")


def get_int(prompt, min_value=None, max_value=None):
    """Keep asking until the user types a valid whole number."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"  Number must be at least {min_value}.")
            elif max_value is not None and value > max_value:
                print(f"  Number must be at most {max_value}.")
            else:
                return value
        except ValueError:
            print("  Please enter a valid number.")


def get_float(prompt, min_value=0):
    """Keep asking until the user types a valid decimal number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= min_value:
                print(f"  Value must be greater than {min_value}.")
            else:
                return value
        except ValueError:
            print("  Please enter a valid amount.")


def pause():
    input("\nPress Enter to continue...")


# ---------------------------------------------------------------
#  Dynamic attributes with getattr / setattr / hasattr
# ---------------------------------------------------------------
def add_dynamic_attribute(obj, name, value):
    """Add a NEW attribute to any object while the program is running."""
    setattr(obj, name, value)             # same as: obj.name = value


def read_attribute(obj, name):
    """Read an attribute safely. Returns a message if it does not exist."""
    if hasattr(obj, name):                # does the object have this attribute?
        return getattr(obj, name)         # same as: obj.name
    return "Not set"


# ---------------------------------------------------------------
#  __getattr__, __setattr__, __delattr__
# ---------------------------------------------------------------
class SmartVehicleInfo:
    """Stores extra information about a vehicle and CONTROLS
    how attributes are read, changed and deleted."""

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id      # this line also goes through __setattr__

    def __getattr__(self, name):
        # Python calls this ONLY when the attribute is not found normally.
        return f"No '{name}' information available"

    def __setattr__(self, name, value):
        # Python calls this for EVERY assignment: obj.something = value
        if name == "vehicle_id" and "vehicle_id" in self.__dict__:
            print("  [__setattr__] vehicle_id is locked and cannot be changed!")
            return
        print(f"  [__setattr__] Setting {name} = {value}")
        super().__setattr__(name, value)  # actually save the value

    def __delattr__(self, name):
        # Python calls this when we write: del obj.something
        if name == "vehicle_id":
            print("  [__delattr__] vehicle_id cannot be deleted!")
            return
        print(f"  [__delattr__] Deleting {name}")
        super().__delattr__(name)


# ---------------------------------------------------------------
#  Context manager: __enter__ and __exit__
# ---------------------------------------------------------------
class ReportWriter:
    """Opens a text file, lets us write to it, and ALWAYS closes it.
    Usage:
        with ReportWriter("report.txt") as writer:
            writer.write("Hello")
    """

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        print(f"  [__enter__] Opening file '{self.filename}'")
        self.file = open(self.filename, "w", encoding="utf-8")
        return self                        # this object goes into "as writer"

    def write(self, text):
        self.file.write(text + "\n")

    def __exit__(self, exc_type, exc_value, traceback):
        # Runs at the end of the "with" block, even if an error happened.
        if self.file:
            self.file.close()
        print("  [__exit__] File closed safely")
        return False                       # False = do not hide any error


# ---------------------------------------------------------------
#  Destructor: __del__
# ---------------------------------------------------------------
class TemporaryBooking:
    """A small class only used to show when the destructor runs."""

    def __init__(self, name):
        self.name = name
        print(f"  [__init__] Temporary booking '{self.name}' created")

    def __del__(self):
        print(f"  [__del__] Temporary booking '{self.name}' destroyed, memory cleaned")
