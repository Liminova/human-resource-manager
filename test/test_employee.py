from models import Employee 
import unittest

class TestEmployee(unittest.TestCase):
    def test_create_employee(self):
        employee = Employee("Rylie", "2003-08-22", "727", "0123456727", "Sleep")

        self.assertEqual(employee.name, "Rylie")
        self.assertEqual(employee.dob, "2003-08-22")
        self.assertEqual(employee.id, "727")
        self.assertEqual(employee.phone, "0123456727")
        self.assertEqual(employee.department, "Sleep")

    def test_mutate_employee(self):
        employee = Employee("Rylie", "2003-08-22", "727", "0123456727", "Sleep")

        self.assertEqual(employee.id, "727")

        employee.id = "420"

        self.assertEqual(employee.id, "420")

if __name__ == "__main__":
    unittest.main()
