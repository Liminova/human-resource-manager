from models import Department, Employee
import unittest

class TestEmployee(unittest.TestCase):
    def test_create_employee(self):
        department = Department() \
            .set_name("Sleep").unwrap() \
            .set_id("SLP").unwrap()

        employee = Employee() \
            .set_name("Rylie").unwrap() \
            .set_dob("2003-08-22").unwrap() \
            .set_id("727").unwrap() \
            .set_phone("0123456727").unwrap() \
            .set_department(department).unwrap()

        self.assertEqual(employee.name, "Rylie")
        self.assertEqual(employee.dob, "2003-08-22")
        self.assertEqual(employee.id, "727")
        self.assertEqual(employee.phone, "0123456727")
        self.assertEqual(employee.department.name, "Sleep")

    def test_mutate_employee(self):
        employee = Employee() \
            .set_name("Rylie").unwrap() \
            .set_dob("2003-08-22").unwrap() \
            .set_id("727").unwrap() \
            .set_phone("0123456727").unwrap() \

        self.assertEqual(employee.id, "727")

        employee.set_id("420").unwrap()

        self.assertEqual(employee.id, "420")

if __name__ == "__main__":
    unittest.main()
