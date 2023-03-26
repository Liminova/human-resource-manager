from models import Department, Employee, Payroll
import unittest

class TestDepartment(unittest.TestCase):
    def test_create_department(self):
        department = Department("Sleep", "SLP", [])

        self.assertEqual(department.name, "Sleep")
        self.assertEqual(department.id, "SLP")
        self.assertEqual(department.members, [])

    def test_mutate_department(self):
        department = Department("Sleep", "SLP", [])
        payroll = Payroll(5000, 500)
        rylie = Employee("Rylie", "2003-08-22", "727", "0123456727", "Sleep", [], payroll)
        department.members.append(rylie)

        self.assertEqual(department.members, [rylie])

if __name__ == "__main__":
    unittest.main()
