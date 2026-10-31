"""
vehicle.py
----------
Vehicle is the PARENT (base) class of every vehicle in the system.

OOP concepts shown here:
  - Abstraction       : Vehicle inherits the abstract class Rentable and does NOT
                        write calculate_rent(), so Vehicle is still abstract.
                        (You cannot create a plain Vehicle object.)
  - Single inheritance: Vehicle -> Motorcycle
  - Hierarchical inh. : Vehicle -> Car  and  Vehicle -> Motorcycle  (one parent, many children)
  - Encapsulation     : public, _protected and __private attributes
  - Properties        : @property, setter, read-only property
  - Getters / Setters : get_availability() / set_availability()
  - Method chaining   : update_brand().update_model().update_rate()
  - Magic methods     : __str__, __repr__, __eq__, __lt__, __gt__
  - Class attribute   : total_vehicles
"""

from interfaces import Rentable


class Vehicle(Rentable):
    # CLASS attribute: counts how many vehicle objects were created
    total_vehicles = 0

    def __init__(self, vehicle_id, brand, model, year, daily_rate):
        self.__vehicle_id = vehicle_id   # PRIVATE   -> read-only through a property
        self.brand = brand               # PUBLIC    -> anyone can read / change it
        self.model = model               # PUBLIC
        self.year = year                 # PUBLIC
        self._available = True           # PROTECTED -> use inside class and child classes
        self.__daily_rate = 0            # PRIVATE   -> changed only through the property
        self.daily_rate = daily_rate     # this calls the setter below (with validation)

        Vehicle.total_vehicles += 1

    # ---------- Read-only property ----------
    @property
    def vehicle_id(self):
        """There is a getter but NO setter, so vehicle_id cannot be changed."""
        return self.__vehicle_id

    # ---------- Property with getter and setter ----------
    @property
    def daily_rate(self):
        return self.__daily_rate

    @daily_rate.setter
    def daily_rate(self, value):
        if value <= 0:
            raise ValueError("Daily rate must be greater than zero.")
        self.__daily_rate = value

    # ---------- Traditional getter and setter ----------
    def get_availability(self):
        return self._available

    def set_availability(self, status):
        self._available = status

    # ---------- Instance methods ----------
    def vehicle_type(self):
        return type(self).__name__       # e.g. "Car", "LuxuryCar"

    def get_details(self):
        status = "Available" if self._available else "Rented"
        return (f"[{self.vehicle_id}] {self.vehicle_type():<10} {self.brand} {self.model} "
                f"({self.year}) | Rs.{self.daily_rate:,.0f}/day | {status}")

    # NOTE: calculate_rent(days) is NOT written here.
    # It is still abstract, so every child class must write its own version.

    # ---------- Method chaining (each method returns self) ----------
    def update_brand(self, brand):
        self.brand = brand
        return self

    def update_model(self, model):
        self.model = model
        return self

    def update_rate(self, rate):
        self.daily_rate = rate
        return self

    # ---------- Magic methods ----------
    def __str__(self):
        return f"{self.brand} {self.model} ({self.vehicle_id})"

    def __repr__(self):
        return f"{self.vehicle_type()}('{self.vehicle_id}', '{self.brand}', '{self.model}')"

    def __eq__(self, other):
        # Two vehicles are "equal" if they have the same ID
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.vehicle_id == other.vehicle_id

    def __hash__(self):
        # Needed because we wrote __eq__ (lets vehicles be used in sets/dicts)
        return hash(self.vehicle_id)

    def __lt__(self, other):
        # car1 < car2  -> compares daily rental prices
        return self.daily_rate < other.daily_rate

    def __gt__(self, other):
        # car1 > car2  -> compares daily rental prices
        return self.daily_rate > other.daily_rate


class Motorcycle(Vehicle):
    """Child of Vehicle (Single inheritance). Car is its "sibling"."""

    def __init__(self, vehicle_id, brand, model, year, daily_rate, engine_cc=125):
        super().__init__(vehicle_id, brand, model, year, daily_rate)   # parent constructor
        self.engine_cc = engine_cc

    def calculate_rent(self, days):
        """Motorcycles get 10% off when rented for 7 days or more."""
        total = self.daily_rate * days
        if days >= 7:
            total = total * 0.90
        return total

    def get_details(self):
        # Method overriding + reusing the parent version with super()
        return super().get_details() + f" | {self.engine_cc}cc"
