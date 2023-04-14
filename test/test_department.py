from models import Department, Employee
import unittest


class TestDepartment(unittest.TestCase):
    def test_create_department(self):
        department = Department().set_name("Sleep").unwrap().set_id("SLP").unwrap()

        self.assertEqual(department.name, "Sleep")
        self.assertEqual(department.dept_id, "SLP")
        self.assertEqual(department.members, [])

    def test_mutate_department(self):
        department = Department().set_name("Sleep").unwrap().set_id("SLP").unwrap()

        rylie = (
            Employee()
            .set_name("Rylie")
            .unwrap()
            .set_dob("2003-08-22")
            .unwrap()
            .set_id("727")
            .unwrap()
            .set_phone("0123456727")
            .unwrap()
        )

        department.members.append(rylie)

        self.assertEqual(department.members, [rylie])


if __name__ == "__main__":
    unittest.main()
