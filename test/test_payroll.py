from models import Payroll
import unittest

class TestPayroll(unittest.TestCase):
    def test_create_payroll(self):
        payroll = Payroll() \
            .set_salary(5000).unwrap() \
            .set_tax(500).unwrap()
        payroll.calculate_total()

        self.assertEqual(payroll.salary, 5000)
        self.assertEqual(payroll.tax, 500)
        self.assertEqual(payroll.total, 4500)

    def test_mutate_payroll(self):
        payroll = Payroll() \
            .set_salary(5000).unwrap() \
            .set_tax(500).unwrap()
        payroll.calculate_total()

        self.assertEqual(payroll.total, 4500)

        payroll.set_bonus(300).unwrap()

        self.assertEqual(payroll.total, 4800)
