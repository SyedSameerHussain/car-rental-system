"""
main.py
-------
Start the program from here:   python main.py

This file creates the objects, shows the CMD menu and lets
all the classes work together.
"""

import os

import utilities as ut
from rental_system import RentalSystem
from vehicle import Vehicle, Motorcycle
from car import Car, LuxuryCar, SUV, PremiumCar, VehicleFactory
from customer import Customer
from employee import Manager, Mechanic
from person import Person
from payment import Payment, CashPayment, CardPayment, GiftVoucher, process_payment
from interfaces import Rentable
from exceptions import CarRentalError

REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rental_report.txt")


# ===============================================================
#  Sample data (so the program is not empty when it starts)
# ===============================================================
def load_sample_data(system):
    system.add_vehicles(
        Car("V001", "Toyota", "Corolla", 2022, 6000),
        Car("V002", "Honda", "Civic", 2023, 7500),
        LuxuryCar("V003", "Mercedes", "C-Class", 2023, 20000),
        SUV("V004", "Toyota", "Fortuner", 2022, 15000, seats=7, fuel_type="Diesel"),
        PremiumCar("V005", "BMW", "X7", 2024, 30000, seats=7),
        Motorcycle("V006", "Honda", "CG-125", 2023, 1500),
    )
    # Class method used as an alternative constructor
    system.add_customer(Customer.create_customer("C001, Ali Khan, 03001234567, DL-12345"))
    system.add_customer(Customer.create_customer("C002, Ayesha Malik, 03007654321, DL-54321"))

    system.employees.append(Manager("E001", "Sara Ahmed", "03111234567", 120000, "Main Branch"))
    system.employees.append(Mechanic("E002", "Bilal Hussain", "03221234567", 60000, "Engines"))


# ===============================================================
#  Menu actions (one function for each menu option)
# ===============================================================
def register_customer(system):
    ut.print_header("REGISTER NEW CUSTOMER")
    name = ut.get_text("Name            : ")
    phone = ut.get_text("Phone (digits)  : ")
    license_number = ut.get_text("License (DL-12345): ").upper()
    customer = system.register_customer(name, phone, license_number)
    print(f"\nCustomer registered successfully! Customer ID: {customer.customer_id}")


def show_customers(system):
    ut.print_header("ALL CUSTOMERS")
    for customer in system.customers:
        customer.display()
    print(f"\nTotal customers: {len(system.customers)}")


def add_vehicle(system):
    ut.print_header("ADD NEW VEHICLE")
    print("Types: " + ", ".join(VehicleFactory.vehicle_types))
    vehicle_type = ut.get_text("Vehicle type : ").lower()
    if vehicle_type not in VehicleFactory.vehicle_types:
        print("Unknown vehicle type.")
        return
    brand = ut.get_text("Brand        : ")
    model = ut.get_text("Model        : ")
    year = ut.get_int("Year         : ", 1990, 2030)
    rate = ut.get_float("Daily rate   : ")
    vehicle = system.add_new_vehicle(vehicle_type, brand, model, year, rate)
    print(f"\nVehicle added: {vehicle.get_details()}")


def remove_vehicle(system):
    ut.print_header("REMOVE VEHICLE")
    vehicle_id = ut.get_text("Vehicle ID to remove: ")
    vehicle = system.remove_vehicle(vehicle_id)
    print(f"Removed: {vehicle}")


def show_vehicles(system):
    ut.print_header("ALL VEHICLES")
    for vehicle in system.vehicles:
        print(vehicle.get_details())        # polymorphism: each class prints its own details


def search_vehicle(system):
    ut.print_header("SEARCH VEHICLE")
    keyword = ut.get_text("Enter brand, model or type: ")
    results = system.search_vehicles(keyword)
    if not results:
        print("No vehicle found.")
    for vehicle in results:
        print(vehicle.get_details())


def rent_vehicle(system):
    ut.print_header("RENT A VEHICLE")
    show_available(system, header=False)
    print()
    customer_id = ut.get_text("Customer ID : ")
    vehicle_id = ut.get_text("Vehicle ID  : ")
    days = ut.get_int("Days (1-30) : ", 1, 30)
    print("Payment method: 1. Cash   2. Card   3. Online")
    choice = ut.get_int("Choose      : ", 1, 3)
    method = {1: "cash", 2: "card", 3: "online"}[choice]

    rental = system.rent_vehicle(customer_id, vehicle_id, days, method)
    print("\nRental successful!")
    print(rental.invoice)


def return_vehicle(system):
    ut.print_header("RETURN A VEHICLE")
    vehicle_id = ut.get_text("Vehicle ID: ")
    rental = system.return_vehicle(vehicle_id)
    print(f"Vehicle returned. Rental {rental.rental_id} is now closed. Thank you, {rental.customer.name}!")


def calculate_charges(system):
    ut.print_header("CALCULATE RENTAL CHARGES")
    vehicle_id = ut.get_text("Vehicle ID : ")
    days = ut.get_int("Days       : ", 1, 30)
    vehicle, price = system.quote(vehicle_id, days)
    print(f"\n{vehicle} for {days} day(s) = {ut.format_money(price)}")

    print(f"\nSame {days} day(s) for every vehicle (POLYMORPHISM):")
    for v in system.vehicles:
        print(f"  {v.vehicle_type():<10} {str(v):<28} -> {ut.format_money(v.calculate_rent(days))}")


def rental_history(system):
    ut.print_header("RENTAL HISTORY")
    customer_id = input("Customer ID (press Enter to see all): ").strip()
    if customer_id:
        system.find_customer(customer_id).display(show_history=True)
    elif not system.rentals:
        print("No rentals yet.")
    else:
        for rental in system.rentals:
            print(rental)


def add_employee(system):
    ut.print_header("ADD EMPLOYEE")
    role = ut.get_text("Role (manager / mechanic / employee): ").lower()
    name = ut.get_text("Name   : ")
    phone = ut.get_text("Phone  : ")
    salary = ut.get_int("Salary : ", 1)
    extra = ""
    if role == "manager":
        extra = ut.get_text("Branch : ")
    elif role == "mechanic":
        extra = ut.get_text("Speciality : ")
    employee = system.add_employee(role, name, phone, salary, extra)
    print(f"\nEmployee added: {employee.get_details()}")


def show_employees(system):
    ut.print_header("ALL EMPLOYEES")
    for employee in system.employees:
        print(employee.get_details())


def show_available(system, header=True):
    if header:
        ut.print_header("AVAILABLE VEHICLES")
    print(f"Available vehicles: {len(system)}")      # __len__
    for vehicle in system:                            # __iter__ and __next__
        print(" ", vehicle.get_details())


def generate_report(system):
    report = system()                                 # __call__
    print(report)
    with ut.ReportWriter(REPORT_FILE) as writer:      # __enter__ / __exit__
        writer.write(report)
    print(f"Report saved to {REPORT_FILE}")


# ===============================================================
#  Option 15: demonstrate the OOP concepts one by one
# ===============================================================
def demonstrate_oop(system):
    car1 = system.vehicles[0]
    car2 = system.vehicles[1]

    ut.print_header("1. CLASS, OBJECT, CLASS vs INSTANCE ATTRIBUTES")
    print("car1 is an object of class:", type(car1).__name__)
    print("Instance attribute car1.model =", car1.model)
    print("Class attribute Vehicle.total_vehicles =", Vehicle.total_vehicles)
    print("Class attribute Person.total_persons   =", Person.total_persons)

    ut.print_header("2. ENCAPSULATION (public / protected / private)")
    print("Public    car1.brand      =", car1.brand)
    print("Protected car1._available =", car1._available)
    print("Private   car1.__daily_rate -> ", end="")
    try:
        print(car1.__daily_rate)
    except AttributeError:
        print("AttributeError (private attributes are hidden)")
    print("Through the property car1.daily_rate =", car1.daily_rate)
    try:
        car1.daily_rate = -500
    except ValueError as error:
        print("Setter validation:", error)
    try:
        car1.vehicle_id = "X999"
    except AttributeError:
        print("vehicle_id is a READ-ONLY property, it cannot be changed")

    ut.print_header("3. ABSTRACTION (ABC and abstract methods)")
    try:
        Vehicle("X001", "Test", "Test", 2020, 100)
    except TypeError:
        print("Cannot create an object of abstract class Vehicle")
    try:
        Payment(100)
    except TypeError:
        print("Cannot create an object of abstract class Payment")
    print("But a child class that writes calculate_rent() works:", car1)

    ut.print_header("4. INHERITANCE, isinstance(), issubclass(), MRO")
    premium = system.vehicles[4]
    print("issubclass(Car, Vehicle)        :", issubclass(Car, Vehicle))
    print("issubclass(LuxuryCar, Car)      :", issubclass(LuxuryCar, Car))
    print("isinstance(premium, Vehicle)    :", isinstance(premium, Vehicle))
    print("isinstance(premium, Rentable)   :", isinstance(premium, Rentable))
    print("Mixin method premium.gps_info() :", premium.gps_info())
    print("Mixin method premium.music_info():", premium.music_info())
    print("MRO of PremiumCar:")
    for cls in PremiumCar.__mro__:
        print("   ->", cls.__name__)

    ut.print_header("5. POLYMORPHISM + METHOD OVERRIDING")
    print("calculate_rent(3) on different vehicle types:")
    for v in system.vehicles:
        print(f"  {v.vehicle_type():<10} -> {ut.format_money(v.calculate_rent(3))}")
    print("get_role() on employees:", [e.get_role() for e in system.employees])

    ut.print_header("6. MAGIC METHODS + OPERATOR OVERLOADING")
    print("str(car1)  :", str(car1))
    print("repr(car1) :", repr(car1))
    same_car = Car("V001", "Toyota", "Corolla", 2022, 6000)
    print("car1 == same_car (same ID) :", car1 == same_car)
    print("car1 < car2 (cheaper?)     :", car1 < car2)
    print("car1 > car2 (expensive?)   :", car1 > car2)
    p1, p2 = CashPayment(5000), CardPayment(8000, "Ali")
    print("p1 + p2   :", p1 + p2)
    print("sum([p1, p2]) :", sum([p1, p2]))
    print("p1 > p2   :", p1 > p2)

    ut.print_header("7. METHOD CHAINING")
    demo_car = Car("D001", "Suzuki", "Alto", 2020, 3000)
    demo_car.update_brand("Suzuki").update_model("Cultus").update_rate(3500)
    print("After chaining:", demo_car.get_details())

    ut.print_header("8. STATIC METHOD, CLASS METHOD, *args")
    print("Customer.validate_license('DL-12345') :", Customer.validate_license("DL-12345"))
    print("Customer.validate_license('12345')    :", Customer.validate_license("12345"))
    new_customer = Customer.create_customer("C999, Demo User, 03000000000, DL-99999")
    print("Created with class method:", new_customer.get_details())
    print("RentalSystem.is_valid_days(45) :", RentalSystem.is_valid_days(45))
    mechanic = system.employees[1]
    mechanic.add_skills("Engine repair", "Tyres", "AC repair")
    print("add_skills(*args) ->", mechanic.skills)

    ut.print_header("9. __len__, __contains__, __iter__, __next__, __call__")
    print("len(system)       :", len(system))
    print("'V001' in system  :", "V001" in system)
    iterator = iter(system)
    print("next(iterator)    :", next(iterator))
    print("next(iterator)    :", next(iterator))
    print("system() makes the report ->", system().splitlines()[1].strip())

    ut.print_header("10. DYNAMIC ATTRIBUTES (setattr / getattr / hasattr)")
    print("hasattr(car1, 'color') :", hasattr(car1, "color"))
    ut.add_dynamic_attribute(car1, "color", "White")
    print("After setattr -> getattr(car1, 'color') :", getattr(car1, "color"))
    print("read_attribute(car1, 'sunroof') :", ut.read_attribute(car1, "sunroof"))

    ut.print_header("11. __getattr__, __setattr__, __delattr__")
    info = ut.SmartVehicleInfo("V001")
    info.insurance = "Full cover"
    print("info.insurance :", info.insurance)
    print("info.mileage   :", info.mileage)        # missing -> __getattr__
    info.vehicle_id = "V999"                       # blocked by __setattr__
    del info.insurance                             # __delattr__
    del info.vehicle_id                            # blocked by __delattr__

    ut.print_header("12. __new__ (only one RentalSystem)")
    another_system = RentalSystem()
    print("RentalSystem() is system :", another_system is system)
    RentalSystem.change_company_name("City Car Rentals")
    print("Company name (class attribute):", RentalSystem.company_name)

    ut.print_header("13. DESTRUCTOR __del__")
    temp = ut.TemporaryBooking("Test booking")
    del temp

    ut.print_header("14. CONTEXT MANAGER (with)")
    with ut.ReportWriter(REPORT_FILE) as writer:
        writer.write("Context manager demo")
    print("(Use menu option 14 to save the full report.)")

    ut.print_header("15. DUCK TYPING")
    for payer in (CashPayment(1000), GiftVoucher("GIFT50", 500)):
        print(f"{type(payer).__name__} is a Payment? {isinstance(payer, Payment)}")
        process_payment(payer)

    ut.print_header("16. CUSTOM EXCEPTIONS")
    try:
        system.find_vehicle("V404")
    except CarRentalError as error:
        print(f"{type(error).__name__}: {error}")
    try:
        Customer("C998", "Wrong License", "03000000000", "ABC")
    except CarRentalError as error:
        print(f"{type(error).__name__}: {error}")


# ===============================================================
#  Main menu
# ===============================================================
MENU = """
=========================================
           CAR RENTAL SYSTEM
=========================================
 1. Register New Customer
 2. Display All Customers
 3. Add New Car
 4. Remove Car
 5. Display All Cars
 6. Search Car
 7. Rent a Car
 8. Return a Car
 9. Calculate Rental Charges
10. Display Rental History
11. Add Employee
12. Display Employees
13. Display Available Cars
14. Generate Rental Report
15. Demonstrate OOP Concepts
 0. Exit
========================================="""

# Each menu number points to the function that handles it
ACTIONS = {
    1: register_customer, 2: show_customers, 3: add_vehicle, 4: remove_vehicle,
    5: show_vehicles, 6: search_vehicle, 7: rent_vehicle, 8: return_vehicle,
    9: calculate_charges, 10: rental_history, 11: add_employee, 12: show_employees,
    13: show_available, 14: generate_report, 15: demonstrate_oop,
}


def main():
    system = RentalSystem()
    load_sample_data(system)

    while True:
        print(MENU)
        choice = ut.get_int("Enter Your Choice: ", 0, 15)
        if choice == 0:
            print(f"\nThank you for using {RentalSystem.company_name}. Goodbye!")
            break
        try:
            ACTIONS[choice](system)
        except CarRentalError as error:          # our own exceptions
            print(f"\nError: {error}")
        except ValueError as error:              # e.g. wrong phone number
            print(f"\nInvalid input: {error}")
        ut.pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram closed.")
