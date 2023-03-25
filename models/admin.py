from .employee import Employee
from .benefits import BenefitPlan

class Admin(Employee):
    def __init__(self) -> None:
        super().__init__

    def accept_benefit_enrollment(
        self, employee: Employee, benefit: BenefitPlan
    ) -> str:
        # add employee to benefit plan
        benefit.enrolled_employees.append(employee)
        # add benefit plan to employee
        employee.benefits.append(benefit)
        # return success message
        return "You are accepted into this benefit plan."

    def decline_benefit_enrollment(
        self, employee: Employee, benefit: BenefitPlan
    ) -> str:
        return "You are declined from this benefit plan."
