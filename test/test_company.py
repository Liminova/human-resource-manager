from models import Company, Department, Employee
import unittest

class TestCompany(unittest.TestCase):
    def test_create_company(self):
        company = Company() \
            .set_name("Doofenshmirtz Evil Inc.").unwrap()

        self.assertEqual(company.name, "Doofenshmirtz Evil Inc.")

    # FIXME: for some reason this is failing while mutating departments is fine.
    def test_mutate_company(self):
        company = Company() \
            .set_name("Doofenshmirtz Evil Inc.").unwrap()

        sleep = Department() \
            .set_name("Sleep").unwrap() \
            .set_id("SLP").unwrap()

        rylie = Employee() \
            .set_name("Rylie").unwrap() \

        company.departments.append(sleep)
        company.employees.append(rylie)

        self.assertEqual(company.name, "Doofenshmirtz Evil Inc.")
        self.assertEqual(company.departments, [sleep])
        self.assertEqual(company.employees, [rylie])

    def test_multiple_company(self):
        company_1 = Company()
        company_2 = Company()

        # this should return the first instance of Company initialized
        self.assertEqual(company_1, company_2)
