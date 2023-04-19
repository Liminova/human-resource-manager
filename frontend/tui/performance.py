from datetime import datetime
from ..helpers import *
from models import Sale, Company
from option import Result, Ok
from database.mongo import employee_repo

import os

the_company: Company = Company()


class MenuPerformance:
    def __init__(self) -> None:
        self.mainloop = self.admin if the_company.logged_in_employee.is_admin else self.employee

    def admin(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            performance_menu = [
                "[1] Add sale",
                "[2] Remove sale",
                "[3] View info about a sale",
                "[4] Find sale(s) by...",
                "[5] View sales performance of all employees",
                "[6] Back",
            ]
            choice = get_user_option_from_menu("Performance management", performance_menu)
            match choice:
                case 1:
                    last_msg = self.__add()
                case 2:
                    last_msg = self.__remove()
                case 3:
                    last_msg = self.__get_info()
                case 4:
                    last_msg = self.__find_submenu_admin()
                case 5:
                    last_msg = self.__view_all()
                case 6:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def employee(self) -> Result[None, str]:
        last_msg = ""
        while True:
            performance_menu = ["[1] View sales performance", "[2] View info about a sale", "[3] Find sale(s) by...", "[4] Back"]
            choice = get_user_option_from_menu("Performance management", performance_menu)
            match choice:
                case 1:
                    last_msg = self.__view_all()
                case 2:
                    last_msg = self.__get_info()
                case 3:
                    last_msg = self.__find_submenu_employee()
                case 4:
                    return Ok(None)
                case _:
                    last_msg = FCOLORS.RED + "Invalid option!" + FCOLORS.END

    def __add(self) -> str:
        empl_items = [f"{employee.name} ({employee.employee_id})" for employee in the_company.employees]
        empl_selected_index = get_user_option_from_list("Select an employee to add a sale for", empl_items)
        if empl_selected_index == -1:
            return NO_EMPLOYEE_MSG
        elif empl_selected_index == -2:
            return ""
        selected_empl = the_company.employees[empl_selected_index]

        if selected_empl.is_admin:
            return "An admin doesn't sell anything!"

        # create a new, empty sale object
        sale = Sale()
        sale.employee_id = selected_empl.employee_id
        sale.employee_name = selected_empl.name

        # enter the sale data
        fields_data = [
            ("Enter sale ID", sale.set_sale_id),
            ("Enter revenue", sale.set_revenue),
            ("Enter cost", sale.set_cost),
            ("Enter profit", sale.set_profit),
            ("Enter client ID", sale.set_client_id),
            ("Enter client rating", sale.set_client_rating),
            ("Enter client comment", sale.set_client_comment),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg

        while True:
            # sale date has a default value, can't use the loop_til_valid_input function
            sale_date = input("Enter sale date (YYYY-MM-DD, 't' for today, leave blank to cancel): ")
            if sale_date == "":
                confirm = input("Are you sure you want to cancel? (Y/n): ")
                if confirm.lower() != "n":
                    return "Input cancelled!"
            elif sale_date == "t":
                sale_date = datetime.now()
                sale.set_date(datetime.strftime(sale_date, "%Y-%m-%d")).unwrap()
                break
            try:
                sale_date = datetime.strptime(sale_date, "%Y-%m-%d") if sale_date else datetime.now()
                sale.set_date(datetime.strftime(sale_date, "%Y-%m-%d")).unwrap()
                break
            except (ValueError, TypeError) as e:
                return str(e)

        # add the sale to the employee's performance
        selected_empl.performance.sale_list.append(sale)
        selected_empl.performance.sales_count += 1
        selected_empl.performance.total_revenue += sale.revenue
        selected_empl.performance.total_cost += sale.cost
        selected_empl.performance.total_profit += sale.profit

        rating_sum = sum([sale.client_rating for sale in selected_empl.performance.sale_list])
        selected_empl.performance.average_rating = rating_sum / len(selected_empl.performance.sale_list)

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"performance"})}, upsert=True)

        return f"Sale for employee {FCOLORS.GREEN}{selected_empl.name}{FCOLORS.END} added successfully!"

    def __view_all(self) -> str:
        if not the_company.logged_in_employee.is_admin:
            sales = the_company.logged_in_employee.performance.sale_list
        else:
            sales = [sale for employee in the_company.employees for sale in employee.performance.sale_list]
        if not sales:
            return NO_SALES_MSG

        # a list containing the string representation of each sale
        sale_items = [sale.one_line_str() for sale in sales]
        listing("All sales", sale_items)
        return ""

    def __remove(self) -> str:
        empl_items = [f"{employee.name} ({employee.employee_id})" for employee in the_company.employees]
        empl_selected_index = get_user_option_from_list("Select an employee to remove a sale for", empl_items)
        if empl_selected_index == -1:
            return NO_EMPLOYEE_MSG
        elif empl_selected_index == -2:
            return ""
        selected_empl = the_company.employees[empl_selected_index]

        if selected_empl.is_admin:
            return "An admin don't sell anything!"

        # a list containing the string representation of each sale
        sale_items = [f"{sale.sale_id} ({sale.client_id})" for sale in selected_empl.performance.sale_list]

        # get the index of the sale to remove
        selected_sale_index = get_user_option_from_list("Select a sale to remove", sale_items)
        if selected_sale_index == -1:
            return NO_SALES_MSG
        elif selected_sale_index == -2:
            return ""

        sale = selected_empl.performance.sale_list[selected_sale_index]

        # remove the sale
        del selected_empl.performance.sale_list[selected_sale_index]
        selected_empl.performance.sales_count -= 1
        selected_empl.performance.total_revenue -= sale.revenue
        selected_empl.performance.total_cost -= sale.cost
        selected_empl.performance.total_profit -= sale.profit

        rating_sum = sum([sale.client_rating for sale in selected_empl.performance.sale_list])
        selected_empl.performance.average_rating = rating_sum / len(selected_empl.performance.sale_list)

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": selected_empl.id}, {"$set": selected_empl.dict(include={"performance"})}, upsert=True)
        return ""

    def __get_info(self) -> str:
        if not the_company.logged_in_employee.is_admin:
            all_sales = the_company.logged_in_employee.performance.sale_list
        else:
            all_sales = [sale for employee in the_company.employees for sale in employee.performance.sale_list]
        sale_items = [sale.one_line_str() for sale in all_sales]
        selected_sale_index = get_user_option_from_list("Select a sale to view info", sale_items)
        if selected_sale_index == -1:
            return NO_SALES_MSG
        elif selected_sale_index == -2:
            return ""

        sale = all_sales[selected_sale_index]
        print(sale)
        input(ENTER_TO_CONTINUE_MSG)
        return ""

    def __find_submenu_admin(self) -> str:
        search_fields = ["[1] Sale ID", "[2] Client ID", "[3] Client rating", "[4] Date", "[5] Employee", "[else] Back"]
        search_selection = get_user_option_from_menu("Find all sales by...", search_fields)
        all_sales: list[Sale] = [sale for employee in the_company.employees for sale in employee.performance.sale_list]
        match search_selection:
            case 1:
                self.__find__by_sale_id(all_sales)
            case 2:
                self.__find__by_client_id(all_sales)
            case 3:
                self.__find__by_client_rating(all_sales)
            case 4:
                self.__find__by_date(all_sales)
            case 5:
                self.__find__by_employee(all_sales)
            case _:
                return ""

        return ""

    def __find_submenu_employee(self) -> str:
        if the_company.logged_in_employee.is_admin:
            return "An admin don't sell anything!"
        search_fields = ["[1] Sale ID", "[2] Client ID", "[3] Client rating", "[4] Date", "[else] Back"]
        search_selection = get_user_option_from_menu("Find all sales by...", search_fields)
        all_sales: list[Sale] = the_company.logged_in_employee.performance.sale_list
        match search_selection:
            case 1:
                self.__find__by_sale_id(all_sales)
            case 2:
                self.__find__by_client_id(all_sales)
            case 3:
                self.__find__by_client_rating(all_sales)
            case 4:
                self.__find__by_date(all_sales)
            case _:
                return ""

        return ""

    def __find__by_sale_id(self, sales: list[Sale]) -> None:
        sale_id = input("Enter sale ID: ")
        sale = [sale for sale in sales if sale.sale_id == sale_id][0]
        if not sale:
            return None
        print(sale)
        input(ENTER_TO_CONTINUE_MSG)

    def __find__by_client_id(self, sales: list[Sale]) -> None:
        client_id = input("Enter client ID: ")
        found_sales = [sale.one_line_str() for sale in sales if sale.client_id == client_id]
        if not found_sales:
            return None

        listing("All sales for client " + client_id, found_sales)

    def __find__by_client_rating(self, sales: list[Sale]) -> None:
        rating = input("Enter client rating (integer 1-5): ")
        try:
            rating = int(rating)
        except:
            return None

        found_sales = [sale.one_line_str() for sale in sales if sale.client_rating == rating]
        if not found_sales:
            return None

        for sale in found_sales:
            print(sale, end="\n\n")

    def __find__by_date(self, sales: list[Sale]) -> None:
        date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        except:
            return None

        found_sales = [sale for sale in sales if datetime.strftime(sale.date, "%Y-%m-%d") == date]
        if not sales:
            return None

        display_sales = [sale.one_line_str() for sale in found_sales]
        listing("All sales for date " + datetime.strftime(date, "%Y-%m-%d"), display_sales)

    def __find__by_employee(self, sales: list[Sale]) -> None:
        empl_items = [f"{employee.name} ({employee.employee_id})" for employee in the_company.employees]
        empl_selected_index = get_user_option_from_list("Select an employee to view sales for", empl_items)
        if empl_selected_index == -1:
            return None
        elif empl_selected_index == -2:
            return None
        selected_empl = the_company.employees[empl_selected_index]

        found_sales = [sale.one_line_str() for sale in selected_empl.performance.sale_list]

        listing("Sales of employee " + selected_empl.name, found_sales)
