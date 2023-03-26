# Create a program to track employee attendance, time off requests, and leave balances. It can also provide reports on attendance and time-off patterns.
# Use a dictionary to store the employee data. The keys are the employee names and the values are lists of the employee’s attendance and time-off data.
# Object Oriented Programming including classes, methods, and inheritance is used to create the program.
# Annotations are used to document the program.

import datetime
import os
import pickle
import sys

# Define the Employee class
class Employee:
    def __init__(self, name, start_date, leave_balance):
        self.name = name
        self.start_date = start_date
        self.leave_balance = leave_balance
        self.attendance = {}
        self.time_off = {}

    def add_attendance(self, date, status):
        self.attendance[date] = status

    def add_time_off(self, date, type):
        self.time_off[type].append(date)

    def get_attendance(self, date):
        return self.attendance[date]

    def get_time_off(self, date):
        for type in self.time_off:
            if date in self.time_off[type]:
                return type

    def get_leave_balance(self):
        return self.leave_balance

    def get_name(self):
        return self.name

    def get_start_date(self):
        return self.start_date

    def set_leave_balance(self, leave_balance):
        self.leave_balance = leave_balance

    def set_name(self, name):
        self.name = name

    def set_start_date(self, start_date):
        self.start_date = start_date

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Define the EmployeeList class
class EmployeeList:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee):
        self.employees[employee.get_name()] = employee

    def get_employee(self, name):
        return self.employees[name]

    def get_employees(self):
        return self.employees

    def remove_employee(self, name):
        del self.employees[name]

    def __str__(self):
        return str(self.employees)

    def __repr__(self):
        return str(self.employees)

# Define the AttendanceCheck class which inherits from the EmployeeList class
class AttendanceCheck(EmployeeList):
    def __init__(self):
        EmployeeList.__init__(self)
        self.attendance_file = 'attendance.pickle'
        self.employee_file = 'employees.pickle'
        self.time_off_file = 'time_off.pickle'
        self.load_data()

    def add_attendance(self, name, date, status):
        self.get_employee(name).add_attendance(date, status)

    def add_employee(self, employee):
        EmployeeList.add_employee(self, employee)
        self.save_data()

    def add_time_off(self, name, date, type):
        self.get_employee(name).add_time_off(date, type)

    def get_attendance(self, name, date):
        return self.get_employee(name).get_attendance(date)

    def get_employee(self, name):
        return EmployeeList.get_employee(self, name)

    def get_employees(self):
        return EmployeeList.get_employees(self)

    def get_time_off(self, name, date):
        return self.get_employee(name).get_time_off(date)

    def load_data(self):
        if os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'rb') as f:
                attendance = pickle.load(f)
            for name in attendance:
                for date in attendance[name]:
                    self.add_attendance(name, date, attendance[name][date])
        if os.path.exists(self.employee_file):
            with open(self.employee_file, 'rb') as f:
                employees = pickle.load(f)
            for name in employees:
                self.add_employee(employees[name])
        if os.path.exists(self.time_off_file):
            with open(self.time_off_file, 'rb') as f:
                time_off = pickle.load(f)
            for name in time_off:
                for type in time_off[name]:
                    for date in time_off[name][type]:
                        self.add_time_off(name, date, type)

    def remove_employee(self, name):
        EmployeeList.remove_employee(self, name)
        self.save_data()

    def save_data(self):
        attendance = {}
        for name in self.get_employees():
            attendance[name] = self.get_employee(name).attendance
        with open(self.attendance_file, 'wb') as f:
            pickle.dump(attendance, f)
        employees = self.get_employees()
        with open(self.employee_file, 'wb') as f:
            pickle.dump(employees, f)
        time_off = {}
        for name in self.get_employees():
            time_off[name] = self.get_employee(name).time_off

        with open(self.time_off_file, 'wb') as f:
            pickle.dump(time_off, f)

# Define the AttendanceCheckUI class which inherits from the AttendanceCheck class
class AttendanceCheckUI(AttendanceCheck):
    def __init__(self):
        AttendanceCheck.__init__(self)
        print("Welcome to the Attendance Check program! Please select an option from the menu.")
        self.menu = """
        Attendance Check
        1. Add Employee
        2. Remove Employee
        3. Add Attendance
        4. Add Time Off
        5. Get Attendance
        6. Get Time Off
        7. Get Leave Balance
        8. Get Employee List
        9. Display the list of employees and their attendance
        10. Exit
        """
        self.menu_choice = 0

    def display_menu(self):
        print(self.menu)
    
    def get_menu_choice(self):
        return self.menu_choice
    
    def set_menu_choice(self, menu_choice):
        self.menu_choice = menu_choice

    def run(self):
        while self.get_menu_choice() != 9:
            self.display_menu()
            self.set_menu_choice(int(input('Enter your choice: ')))
            if self.get_menu_choice() == 1:
                name = input('Enter the employee name: ')
                start_date = input('Enter the employee start date: ')
                leave_balance = int(input('Enter the employee leave balance: '))
                self.add_employee(Employee(name, start_date, leave_balance))
            elif self.get_menu_choice() == 2:
                name = input('Enter the employee name: ')
                self.remove_employee(name)
            elif self.get_menu_choice() == 3:
                name = input('Enter the employee name: ')
                date = input('Enter the date: ')
                status = input('Enter the status: ')
                self.add_attendance(name, date, status)
            elif self.get_menu_choice() == 4:
                name = input('Enter the employee name: ')
                date = input('Enter the date: ')
                type = input('Enter the type: ')
                self.add_time_off(name, date, type)
            elif self.get_menu_choice() == 5:
                name = input('Enter the employee name: ')
                date = input('Enter the date: ')
                print(self.get_attendance(name, date))
            elif self.get_menu_choice() == 6:
                name = input('Enter the employee name: ')
                date = input('Enter the date: ')
                print(self.get_time_off(name, date))
            elif self.get_menu_choice() == 7:
                name = input('Enter the employee name: ')
                print(self.get_employee(name).get_leave_balance())
            elif self.get_menu_choice() == 8:
                print(self.get_employees())
            elif self.get_menu_choice() == 9:
                print(self)
            elif self.get_menu_choice() == 10:
                print('Goodbye.')
                break
            else:
                print('Invalid choice.')

# Main program
def main():
    attendance_check = AttendanceCheckUI()
    attendance_check.run()

if __name__ == '__main__':
    main()
