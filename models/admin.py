from .company import Company
from .benefits import BenefitPlan
from .employee import Employee

company = Company()

class Admin(Employee):
    def __init__(self) -> None:
        super().__init__

    def add_benefit_plan(self, benefit: BenefitPlan) -> str:
        # add benefit plan to company
        company.benefits.append(benefit)
        # return success message
        return "Benefit plan added successfully."

    def remove_benefit_plan(self, benefit: BenefitPlan) -> str:
        # remove benefit plan from company
        company.benefits.remove(benefit)
        # return success message
        return "Benefit plan removed successfully."

    # NOTE: this is a function to view requests for a specific benefit plan only
    # tell me if you want a function to view all requests for all benefit plans - Pechy
    def view_requests(self, benefit: BenefitPlan) -> list[Employee]:
        return benefit.pending_requests

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

    def remove_benefit_enrollment(
        self, employee: Employee, benefit: BenefitPlan
    ) -> str:
        # remove employee from benefit plan
        benefit.enrolled_employees.remove(employee)
        # remove benefit plan from employee
        employee.benefits.remove(benefit)
        # return success message
        return "You are removed from this benefit plan."