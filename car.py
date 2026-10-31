"""
car.py
------
All car classes, extra-feature mixins and the vehicle factory.

OOP concepts shown here:
  - Single inheritance     : Vehicle -> Car
  - Multilevel inheritance : Vehicle -> Car -> LuxuryCar
  - Multiple inheritance   : SUV(Car, GPSMixin)
  - Hybrid inheritance     : PremiumCar(LuxuryCar, GPSMixin, MusicSystemMixin)
                             (multilevel + multiple together)
  - Method overriding      : every class writes its own calculate_rent()
  - Polymorphism           : same method name, different result for each class
  - super()                : call the parent version of a method
  - Constructor inheritance: SUV has no __init__, so it uses Car's __init__
  - MRO                    : the order Python searches classes (PremiumCar.__mro__)
  - Factory method         : VehicleFactory.create_vehicle()
"""

from vehicle import Vehicle, Motorcycle


# ---------------------------------------------------------------
#  Mixins: small classes that only ADD extra features
# ---------------------------------------------------------------
class GPSMixin:
    gps_fee_per_day = 500

    def gps_info(self):
        return "GPS Navigation installed"

    def gps_charges(self, days):
        return self.gps_fee_per_day * days


class MusicSystemMixin:
    def music_info(self):
        return "Premium Music System installed"


# ---------------------------------------------------------------
#  Car classes
# ---------------------------------------------------------------
class Car(Vehicle):
    """Normal car. Rent = daily rate x days."""

    def __init__(self, vehicle_id, brand, model, year, daily_rate, seats=5, fuel_type="Petrol"):
        super().__init__(vehicle_id, brand, model, year, daily_rate)   # call parent constructor
        self.seats = seats
        self.fuel_type = fuel_type

    def calculate_rent(self, days):
        return self.daily_rate * days

    def get_details(self):
        return super().get_details() + f" | {self.seats} seats | {self.fuel_type}"


class LuxuryCar(Car):
    """Multilevel inheritance: Vehicle -> Car -> LuxuryCar.
    Rent = normal car rent + 20% luxury tax."""

    luxury_tax = 0.20

    def calculate_rent(self, days):
        base_rent = super().calculate_rent(days)       # Car's version
        return base_rent + base_rent * self.luxury_tax


class SUV(Car, GPSMixin):
    """Multiple inheritance: SUV gets features from Car AND GPSMixin.
    No __init__ here -> the constructor of Car is inherited.
    Rent = normal car rent + GPS fee."""

    def calculate_rent(self, days):
        return super().calculate_rent(days) + self.gps_charges(days)


class PremiumCar(LuxuryCar, GPSMixin, MusicSystemMixin):
    """Hybrid inheritance: multilevel (Vehicle -> Car -> LuxuryCar)
    + multiple (GPSMixin, MusicSystemMixin).
    Rent = luxury car rent + GPS fee."""

    def calculate_rent(self, days):
        return super().calculate_rent(days) + self.gps_charges(days)

    def get_details(self):
        return super().get_details() + " | GPS + Music"


# ---------------------------------------------------------------
#  Factory: creates the right object from a simple text name
# ---------------------------------------------------------------
class VehicleFactory:
    vehicle_types = ["car", "luxury", "suv", "premium", "motorcycle"]

    @staticmethod
    def create_vehicle(vehicle_type, vehicle_id, brand, model, year, daily_rate):
        vehicle_type = vehicle_type.lower()
        if vehicle_type == "car":
            return Car(vehicle_id, brand, model, year, daily_rate)
        elif vehicle_type == "luxury":
            return LuxuryCar(vehicle_id, brand, model, year, daily_rate)
        elif vehicle_type == "suv":
            return SUV(vehicle_id, brand, model, year, daily_rate, seats=7)
        elif vehicle_type == "premium":
            return PremiumCar(vehicle_id, brand, model, year, daily_rate)
        elif vehicle_type == "motorcycle":
            return Motorcycle(vehicle_id, brand, model, year, daily_rate)
        else:
            raise ValueError(f"Unknown vehicle type '{vehicle_type}'.")
