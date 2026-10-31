"""
employee.py
-----------
Employee classes.

OOP concepts shown here:
  - Hierarchical inheritance : Person -> Customer and Person -> Employee
                               Employee -> Manager and Employee -> Mechanic
  - Multilevel inheritance   : Person -> Employee -> Manager
  - super() and constructor chaining
  - Method overriding + polymorphism : get_role(), calculate_bonus()
  - Private attribute with read-only property : __salary
  - *args (variable number of arguments) : add_skills(*skills)
"""

from person import Person


class Employee(Person):
    bonus_rate = 0.05                     # 5% bonus for a normal employee

    def __init__(self, employee_id, name, phone, salary):
        super().__init__(name, phone)     # Person constructor
        self.employee_id = employee_id
        self.__salary = salary            # private
        self.skills = []

    @property
    def salary(self):
        return self.__salary

    def get_role(self):
        return "Employee"

    def calculate_bonus(self):
        return self.salary * self.bonus_rate

    def add_skills(self, *skills):
        """*args lets us pass any number of skills:
        add_skills("Driving")  or  add_skills("Driving", "Sales", "English")
        """
        self.skills.extend(skills)

    def get_details(self):
        return (f"[{self.employee_id}] {self.name:<15} | {self.get_role():<8} "
                f"| Salary: Rs.{self.salary:,} | Bonus: Rs.{self.calculate_bonus():,.0f}")


class Manager(Employee):
    bonus_rate = 0.15

    def __init__(self, employee_id, name, phone, salary, branch):
        super().__init__(employee_id, name, phone, salary)   # Employee constructor
        self.branch = branch

    def get_role(self):
        return "Manager"

    def get_details(self):
        return super().get_details() + f" | Branch: {self.branch}"


class Mechanic(Employee):
    bonus_rate = 0.10

    def __init__(self, employee_id, name, phone, salary, speciality):
        super().__init__(employee_id, name, phone, salary)
        self.speciality = speciality

    def get_role(self):
        return "Mechanic"

    def get_details(self):
        return super().get_details() + f" | Speciality: {self.speciality}"
