from models import BenefitPlan, Department, Employee, Payroll
import unittest

class TestBenefit(unittest.TestCase):
    def test_create_benefit(self):
        benefit = BenefitPlan("Beds", "Beds for sleeping.", 5000.0, [])

        self.assertEqual(benefit.name, "Beds")
        self.assertEqual(benefit.description, "Beds for sleeping.")
        self.assertEqual(benefit.cost, 5000.0)

    def test_mutate_benefit(self):
        benefit = BenefitPlan("Beds", "Beds for sleeping.", 5000.0, [])
        rylie = Employee() \
            .set_name("Rylie").unwrap()

        benefit.enrolled_employees.append(rylie)

        self.assertEqual(benefit.enrolled_employees, [rylie])
