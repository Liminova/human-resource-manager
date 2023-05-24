import unittest

from models import BenefitPlan, Employee


class TestBenefit(unittest.TestCase):
    def test_create_benefit(self):
        benefit = (
            BenefitPlan()
            .set_name("Beds")
            .unwrap()
            .set_description("Beds for sleeping.")
            .unwrap()
            .set_cost(5000.0)
            .unwrap()
        )

        self.assertEqual(benefit.name, "Beds")
        self.assertEqual(benefit.description, "Beds for sleeping.")
        self.assertEqual(benefit.cost, 5000.0)

    def test_mutate_benefit(self):
        benefit = (
            BenefitPlan()
            .set_name("Beds")
            .unwrap()
            .set_description("Beds for sleeping.")
            .unwrap()
            .set_cost(5000.0)
            .unwrap()
        )
        rylie = Employee().set_name("Rylie").unwrap()

        benefit.enrolled_employees.append(rylie)

        self.assertEqual(benefit.enrolled_employees, [rylie])


if __name__ == "__main__":
    unittest.main()
