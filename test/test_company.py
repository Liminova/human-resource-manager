from models import Company, Department, Employee
import unittest

class TestCompany(unittest.TestCase):
    def test_create_company(self):
        company = Company("Doofenshmirtz Evil Inc.", [], [])

        self.assertEqual(company.name, "Doofenshmirtz Evil Inc.")

    # FIXME: for some reason this is failing while mutating departments is fine.
    def test_mutate_company(self):
        company = Company("Doofenshmirtz Evil Inc.", [], [])
        rylie = Employee("Rylie", "2003-08-22", "727", "0123456727", "Sleep")
        sleep = Department("Sleep", "SLP", [rylie])

        company.departments.append(sleep)
        company.employees.append(rylie)

        self.assertEqual(company.name, "Doofenshmirtz Evil Inc.")
        self.assertEqual(company.departments, [sleep])
        self.assertEqual(company.employees, [rylie])

    def test_multiple_company(self):
        company_1 = Company("Company 1", [], [])
        company_2 = Company("Company 2", [], [])

        # this should return the first instance of Company initialized
        self.assertEqual(company_1.name, company_2.name)
