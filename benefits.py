# features:
# Employees can:
# 1. request to enroll in benefit plan
# 2. view all benefit plans
# Admin can:
# 3. view benefit plan details (including: name of plan, description of plan, cost of plan, and enrolled employees)
# 4. accept benefit plan enrollment
# 5. decline benefit plan enrollment

# example data
class Employee:
    def __init__(self, name: str, plans: list):
        self.name = name
        self.plans = []

    # function to request to enroll in benefit plan
    def request_enroll_in_benefit_plan(self, benefit_plan):
        # check if employee is enrolled in benefit plan
        if self.is_enrolled_in_benefit_plan(benefit_plan):
            # if employee is enrolled in benefit plan
            # return error message
            return "You are already enrolled in this benefit plan."
        else:
            # if employee is not enrolled in benefit plan
            # append request to requests array
            requests.append(self.get_name() + " requested to enroll in " + benefit_plan.get_name())
            # return success message
            return("Your request to enroll in this benefit plan has been submitted.")

    # function to pick options: request to enroll / view plans / go back
    def pick_options(self):
        print("Select an action:\n1. Request to enroll in benefit plan\n2. View all benefit plans\n3. Go back")
        action = input()
        while action != "3":
            if action == "1":
                print("Select a benefit plan:\n1. Health Insurance\n2. Dental Insurance\n3. Vision Insurance")
                benefit_plan = input()
                if benefit_plan == "1":
                    print(self.request_enroll_in_benefit_plan(benefit_plans[0]))
                elif benefit_plan == "2":
                    print(self.request_enroll_in_benefit_plan(benefit_plans[1]))
                elif benefit_plan == "3":
                    print(self.request_enroll_in_benefit_plan(benefit_plans[2]))
                else:
                    print("Invalid input.")
            elif action == "2":
                print(self.get_all_plans())
            elif action == "3":
                return
            else:
                print("Invalid input.")
            print("Select an action:\n1. Request to enroll in benefit plan\n2. View all benefit plans\n3. Go back")
            action = input()

# --------------------------------------

    # function to pick options: view benefit plan details / accept benefit plan enrollment / decline benefit plan enrollment / go back
    def pick_options(self):
        print("Select an action:\n1. View benefit plan details\n2. Accept benefit plan enrollment\n3. Decline benefit plan enrollment\n4. Go back")
        action = input()
        while action != "4":
            if action == "1":
                print("Select a benefit plan:\n1. Health Insurance\n2. Dental Insurance\n3. Vision Insurance\n4. Go back")
                benefit_plan = input()
                if benefit_plan == "1":
                    print(self.view_benefit_plan_details(benefit_plans[0]))
                elif benefit_plan == "2":
                    print(self.view_benefit_plan_details(benefit_plans[1]))
                elif benefit_plan == "3":
                    print(self.view_benefit_plan_details(benefit_plans[2]))
                elif benefit_plan == "4":
                    return
                else:
                    print("Invalid input.")
            elif action == "2":
                if len(requests) == 0:
                    print("There are no requests.")
                else:
                    print("Select a request:")
                    for request in requests:
                        i = requests.index(request)
                        print(str(i+1) + ". " + request)
                    request = input()
                    # get employee name and benefit plan name from request
                    employee_name = requests[int(request)-1].split(" ")[0]
                    # benfit_plan_name is the rest of the string after the first 5 words
                    benefit_plan_name = " ".join(requests[int(request)-1].split(" ")[5:])
                    # get employee and benefit plan objects
                    for employee in employees:
                        if employee.get_name() == employee_name:
                            employee_object = employee
                    for benefit_plan in benefit_plans:
                        if benefit_plan.get_name() == benefit_plan_name:
                            benefit_plan_object = benefit_plan
                    print(self.accept_benefit_plan_enrollment(employee_object, benefit_plan_object))
                    # remove request from requests array
                    requests.remove(requests[int(request)-1])
                    return

            elif action == "3":
                if len(requests) == 0:
                    print("There are no requests.")
                else:
                    print("Select a request:")
                    for request in requests:
                        i = requests.index(request)
                        print(str(i+1) + ". " + request)
                    request = input()
                    # get employee name and benefit plan name from request
                    employee_name = requests[int(request)-1].split(" ")[0]
                    benefit_plan_name = " ".join(requests[int(request)-1].split(" ")[5:])
                    # get employee and benefit plan objects
                    for employee in employees:
                        if employee.get_name() == employee_name:
                            employee_object = employee
                    for benefit_plan in benefit_plans:
                        if benefit_plan.get_name() == benefit_plan_name:
                            benefit_plan_object = benefit_plan
                    print(self.decline_benefit_plan_enrollment(employee_object, benefit_plan_object))
                    # remove request from requests array
                    requests.remove(requests[int(request)-1])
                    return

            elif action == "4":
                return
            else:
                print("Invalid input.")
# --------------------------------------

# arrays 
employees = []
benefit_plans = []
admins = []
requests = []

# ------------------- Main -------------------

def main():
    # create employees
    employee1 = Employee("John", [])
    employee2 = Employee("Jane", [])
    employee3 = Employee("Joe", [])

    # create benefit plans
    benefit_plan1 = BenefitPlan("Health Insurance", "Health Insurance", 100, [])
    benefit_plan2 = BenefitPlan("Dental Insurance", "Dental Insurance", 50, [])
    benefit_plan3 = BenefitPlan("Vision Insurance", "Vision Insurance", 50, [])

    # create admins
    admin1 = Admin("Admin1")

    # add employees to employees array
    employees.append(employee1)
    employees.append(employee2)
    employees.append(employee3)

    # add benefit plans to benefit plans array
    benefit_plans.append(benefit_plan1)
    benefit_plans.append(benefit_plan2)
    benefit_plans.append(benefit_plan3)

    # add admins to admins array
    admins.append(admin1)

    print("HR System")
    print("Select a role:\n1. Employee\n2. Admin\n3. Exit")
    role = input()
    while role != "3":
        if role == "1":
            print("Who are you: 1. John, 2. Jane, 3. Joe")
            name = input()
            for employee in employees:
                if name == employee.get_name():
                    employee.pick_options()
                    break
            else:
                print("Invalid input.")
        elif role == "2":
            print("Who are you?")
            name = input()
            for admin in admins:
                if name == admin.get_name():
                    admin.pick_options()
                    break
            else:
                print("Invalid input.")
        elif role == "3":
            return
        else:
            print("Invalid input.")
        print("Select a role:\n1. Employee\n2. Admin\n3. Exit")
        role = input()

main()
