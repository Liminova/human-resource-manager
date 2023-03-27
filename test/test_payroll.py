from models import Payroll
import unittest

class TestPayroll(unittest.TestCase):
    def test_create_payroll(self):
        payroll = Payroll(5000, 500)
        payroll.calculate_total()

        self.assertEqual(payroll.salary, 5000)
        self.assertEqual(payroll.tax, 500)
        self.assertEqual(payroll.total, 4500)

    def test_mutate_payroll(self):
        payroll = Payroll(5000, 500)
        payroll.calculate_total()

        self.assertEqual(payroll.total, 4500)

        payroll.bonus = 300

        self.assertEqual(payroll.total, 4800)
