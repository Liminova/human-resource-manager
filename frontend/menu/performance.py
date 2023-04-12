from __future__ import annotations
import sys
from datetime import datetime
from ..helpers import *
from models import Sale
if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from ...models.company import Company

class MenuPerformance:
    def __init__(self, company: Company):
        self.__company = company

    def start(self) -> tuple[bool, str]:
        employees = self.__company.employees

        # a list containing the string representation of each employee
        employee_items = [f"{employee.name} ({employee.employee_id})" for employee in employees]

        # get the index of the employee to manage performance for
        employee_selected_index = get_user_option_from_list("Select an employee to manage performance", employee_items)
        if employee_selected_index == -1:
            return False, "No employee selected!"

        # get the employee object
        self.__employee = employees[employee_selected_index]

        last_msg = ""
        while True:
            clrscr()
            if last_msg:
                print(last_msg)
                last_msg = ""
            performance_menu = [
                "[1] Add sale"
                "[2] View sales performance",
                "[3] Remove sale",
                "[4] Get sale info",
                "[5] Find sale(s) by...",
                "[6] Back",
            ]
            choice = get_user_option_from_menu("Performance management", performance_menu)
            match choice:
                case 1: last_msg = self.__add()
                case 2: last_msg = self.__view()
                case 3: last_msg = self.__remove()
                case 4: last_msg = self.__get_info()
                case 5: last_msg = self.__find()

                case _:  # Back
                    return True, ""

    def __add(self) -> str:
        # create a new, empty sale object
        sale = Sale()

        # enter the sale data
        fields_data = [
            ("Enter sale ID: ", sale.set_sale_id),
            ("Enter revenue: ", sale.set_revenue),
            ("Enter cost: ", sale.set_cost),
            ("Enter profit: ", sale.set_profit),
            ("Enter client ID: ", sale.set_client_id),
            ("Enter client rating: ", sale.set_client_rating),
            ("Enter client comment: ", sale.set_client_comment)
        ]
        for (field, setter) in fields_data:
            loop_til_valid_input(field, setter)

        while True:
            # sale date has a default value, can't use the loop_til_valid_input function
            sale_date = input("Enter sale date (YYYY-MM-DD, leave blank for today): ")
            try:
                sale_date = datetime.strptime(sale_date, "%Y-%m-%d") if sale_date else datetime.now()
                sale.set_date(sale_date).unwrap()
                break
            except (ValueError, TypeError) as e:
                return str(e)

        # add the sale to the employee's performance
        self.__employee.performance.sale_list.append(sale)

        return f"Sale for employee {FCOLORS.GREEN}{self.__employee.name}{FCOLORS.END} added successfully!"

    def __view(self) -> str:
        print(self.__employee.performance)
        input("Press enter to continue...")
        return ""

    def __remove(self) -> str:
        # a list containing the string representation of each sale
        sale_items = [f"{sale.sale_id} ({sale.client_id})" for sale in self.__employee.performance.sale_list]

        # get the index of the sale to remove
        selected_sale_index = get_user_option_from_list("Select a sale to remove", sale_items)
        if selected_sale_index == -1:
            return "No sale selected!"

        # remove the sale
        del self.__employee.performance.sale_list[selected_sale_index]
        return ""

    def __get_info(self) -> str:
        pass

    def __find(self) -> str:
        search_fields = [
            "[1] Sale ID",
            "[2] Client ID",
            "[3] Client rating",
            "[4] Date"
            "[else] Back"
        ]
        search_selection = get_user_option_from_menu("Find all sales by...", search_fields)
        match search_selection:
            case 1:  # Sale ID
                sale = self.__employee.performance.get_sale_by_id(input("Enter sale ID: "))

                if not sale:
                    return "No sales found!"

                print(sale)
                input("Press enter to continue...")
                return ""

            case 2:  # Client ID
                sales = self.__employee.performance.get_sales_by_client_id(input("Enter client ID: "))

                if not sales:
                    return "No sales found!"

                for sale in sales:
                    print(sale)
            case 3:  # Client rating
                rating = input("Enter client rating (integer 1-5): ")
                try:
                    rating = int(rating)
                except:
                    return "Invalid rating!"

                sales = self.__employee.performance.get_sales_by_rating(rating)

                if not sales:
                    return "No sales found!"

                for sale in sales:
                    print(sale, end="\n\n")

            case 4:  # Date
                date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
                try:
                    date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
                except:
                    return "Invalid date!"

                sales = self.__employee.performance.get_sales_by_date(date)

                if not sales:
                    return "No sales found!"

                for sale in sales:
                    print(sale, end="\n\n")

            case _:  # Back
                return ""
