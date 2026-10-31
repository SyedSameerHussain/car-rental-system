# Car Rental System (Python OOP Project)

A command-line (CMD) car rental application that demonstrates the full Python OOP syllabus.
Data is kept in memory (lists), so it resets when the program closes.

## How to run

1. Install Python 3.8 or newer from https://www.python.org (tick **"Add Python to PATH"** during install).
2. Open CMD in this folder and run:

```
python main.py
```

Sample data is loaded automatically:

| ID   | Vehicle                    | Type        |
|------|----------------------------|-------------|
| V001 | Toyota Corolla             | Car         |
| V002 | Honda Civic                | Car         |
| V003 | Mercedes C-Class           | LuxuryCar   |
| V004 | Toyota Fortuner            | SUV         |
| V005 | BMW X7                     | PremiumCar  |
| V006 | Honda CG-125               | Motorcycle  |

Customers: **C001** Ali Khan, **C002** Ayesha Malik. License format: `DL-12345`.

Tip: choose menu option **15** to see every OOP concept demonstrated one by one.

## Files

| File | What it contains |
|------|------------------|
| `main.py` | CMD menu, sample data, OOP demonstration (option 15) |
| `interfaces.py` | Abstract classes `Rentable` and `Payable` |
| `person.py` | `Person` parent class |
| `customer.py` | `Customer` (child of Person) |
| `employee.py` | `Employee`, `Manager`, `Mechanic` |
| `vehicle.py` | Abstract `Vehicle` parent class and `Motorcycle` |
| `car.py` | `Car`, `LuxuryCar`, `SUV`, `PremiumCar`, mixins, `VehicleFactory` |
| `rental.py` | `Rental` and `Invoice` |
| `payment.py` | `Payment` types, `GiftVoucher` (duck typing) |
| `rental_system.py` | `RentalSystem`, the class that manages everything |
| `utilities.py` | Input helpers, dynamic attributes, context manager, destructor demo |
| `exceptions.py` | Custom exceptions |

## Class diagram (inheritance)

```
Rentable (ABC)                      Person
   └── Vehicle (abstract)              ├── Customer
         ├── Motorcycle                └── Employee
         └── Car                             ├── Manager
               ├── LuxuryCar                 └── Mechanic
               │     └── PremiumCar  ◄── GPSMixin, MusicSystemMixin
               └── SUV               ◄── GPSMixin
Payable (ABC)
   └── Payment (abstract)
         ├── CashPayment
         ├── CardPayment
         └── OnlinePayment
```

## Where each OOP concept is (for your viva)

| Concept | Where to find it |
|---------|------------------|
| Class and Object | Every class; objects created in `main.py → load_sample_data()` |
| Constructor `__init__` | Every class, e.g. `Vehicle.__init__` |
| `self` | Every instance method |
| Instance attributes | `self.brand`, `self.model` in `Vehicle` |
| Class attributes | `Vehicle.total_vehicles`, `Customer.customer_count` |
| Public / Protected / Private | `brand` / `_available` / `__daily_rate` in `Vehicle` |
| Encapsulation | Private data accessed only through properties/getters |
| Getters and Setters | `get_availability()` / `set_availability()` in `Vehicle`, `get_license()` / `set_license()` in `Customer` |
| `@property` with setter | `Vehicle.daily_rate`, `Person.phone` (both validate values) |
| Read-only property | `Vehicle.vehicle_id`, `Employee.salary` |
| Abstraction / ABC | `interfaces.py`, `Vehicle`, `Payment` |
| Abstract methods | `calculate_rent()`, `get_details()`, `pay()` |
| Single inheritance | `Vehicle → Motorcycle`, `Person → Customer` |
| Multilevel inheritance | `Vehicle → Car → LuxuryCar`, `Person → Employee → Manager` |
| Hierarchical inheritance | `Vehicle → Car / Motorcycle`, `Employee → Manager / Mechanic` |
| Multiple inheritance | `SUV(Car, GPSMixin)` |
| Hybrid inheritance | `PremiumCar(LuxuryCar, GPSMixin, MusicSystemMixin)` |
| `super()` | Every child `__init__`, `LuxuryCar.calculate_rent()` |
| Constructor inheritance | `SUV` has no `__init__`, so it uses `Car.__init__` |
| MRO | `PremiumCar.__mro__` (option 15, part 4) |
| Method overriding | `calculate_rent()`, `get_details()`, `get_role()` |
| Polymorphism | Option 9: the same `calculate_rent()` call gives a different result for each vehicle |
| Method overloading | Default argument `Customer.display(show_history=False)`, `*args` in `Employee.add_skills()` and `RentalSystem.add_vehicles()` |
| Instance method | `Rental.generate_invoice()` |
| Class method | `Customer.create_customer()`, `RentalSystem.change_company_name()` |
| Static method | `Customer.validate_license()`, `RentalSystem.is_valid_days()` |
| Factory method | `VehicleFactory.create_vehicle()`, `Payment.create()` |
| Method chaining | `car.update_brand(..).update_model(..).update_rate(..)`, `Rental(..).apply_discount(..)` |
| Composition | `Rental` creates its own `Invoice` |
| Aggregation | `Rental` uses an existing `Customer` and `Vehicle` |
| `__str__` / `__repr__` | `Vehicle`, `Person`, `Payment`, `Rental` |
| `__eq__`, `__lt__`, `__gt__` | `Vehicle` (compare by ID / price), `Payment` (compare amounts) |
| `__add__` / `__radd__` | `Payment` (`p1 + p2`, `sum(payments)`) |
| `__len__` | `len(system)` → number of available vehicles |
| `__contains__` | `"V001" in system` → is the vehicle available? |
| `__iter__` / `__next__` | `for v in system:` uses `AvailableVehicleIterator` |
| `__call__` | `system()` creates the rental report |
| `__new__` | `RentalSystem` (only one object can exist) |
| `__getattr__` / `__setattr__` / `__delattr__` | `SmartVehicleInfo` in `utilities.py` |
| Dynamic attributes | `add_dynamic_attribute()` uses `setattr`, `getattr`, `hasattr` |
| `__enter__` / `__exit__` | `ReportWriter` (used by option 14) |
| Destructor `__del__` | `TemporaryBooking` in `utilities.py` |
| `isinstance()` / `issubclass()` | Option 15, part 4 |
| Duck typing | `process_payment()` works with `GiftVoucher` even though it is not a `Payment` |
| Custom exceptions | `exceptions.py`, caught in `main.py → main()` |

## Business rules

- **Car**: daily rate × days
- **LuxuryCar**: car rent + 20% luxury tax
- **SUV**: car rent + Rs.500/day GPS fee
- **PremiumCar**: luxury rent + Rs.500/day GPS fee
- **Motorcycle**: daily rate × days, 10% off for 7 or more days
- **Loyal customer**: 10% discount after 2 previous rentals
- Rentals can be from 1 to 30 days. A rented vehicle cannot be rented again or removed until it is returned.
