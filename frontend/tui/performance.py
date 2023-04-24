from datetime import datetime
from ..helpers_tui import *
from models import Sale, Company
from option import Result, Ok
from database.mongo import employee_repo  # type: ignore

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
            last_msg = refresh(last_msg)
            performance_menu = [
                "[1] View sales performance",
                "[2] View info about a sale",
                "[3] Find sale(s) by...",
                "[4] Back",
            ]
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
        empls = the_company.employees
        empl_idx_select = get_user_option_from_list(
            "Select an employee to add a sale for", tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""
        _empl = empls[empl_idx_select]

        if empls[empl_idx_select].is_admin:
            return "An admin doesn't sell anything!"

        # create a new, empty sale object
        sale = Sale()
        sale.employee_id = _empl.employee_id
        sale.employee_name = _empl.name

        # enter the sale data
        fields_data = [
            ("Enter sale ID", sale.set_sale_id),
            ("Enter revenue", sale.set_revenue),
            ("Enter cost", sale.set_cost),
            ("Enter client ID", sale.set_client_id),
            ("Enter client rating", sale.set_client_rating),
            ("Enter client comment", sale.set_client_comment),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid_input(field, setter)) != "":
                return msg
        sale.profit = sale.revenue - sale.cost

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

        _perf = _empl.performance
        _perf.sale_list.append(sale)
        _perf.sales_count += 1
        _perf.total_revenue += sale.revenue
        _perf.total_cost += sale.cost
        _perf.total_profit += sale.profit

        rating_sum = sum([sale.client_rating for sale in _perf.sale_list])
        rating_count = len([sale for sale in _perf.sale_list])
        _perf.average_rating = rating_sum / rating_count if rating_count else 0

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict()}, upsert=True)

        return f"Sale for {FCOLORS.GREEN}{_empl.name}{FCOLORS.END} added successfully!"

    def __view_all(self) -> str:
        if not the_company.logged_in_employee.is_admin:
            sales = the_company.logged_in_employee.performance.sale_list
        else:
            sales = tuple(s for e in the_company.employees for s in e.performance.sale_list)
        if not sales:
            return NO_SALES_MSG

        sale_items = tuple(sale.one_line_str() for sale in sales)
        listing("All sales", sale_items)
        return ""

    def __remove(self) -> str:

        empl_idx_select = get_user_option_from_list(
            "Select an employee to remove a sale for", tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees)
        )
        if empl_idx_select in (-1, -2):
            return NO_EMPLOYEE_MSG if empl_idx_select == -1 else ""
        _empl = the_company.employees[empl_idx_select]
        _perf = _empl.performance

        if _empl.is_admin:
            return "An admin don't sell anything!"

        # get the index of the sale to remove
        sale_idx_select = get_user_option_from_list(
            "Select a sale to remove", tuple(f"{s.sale_id} ({s.client_id})" for s in _empl.performance.sale_list)
        )
        if sale_idx_select in (-1, -2):
            return NO_SALES_MSG if sale_idx_select == -1 else ""
        _sale = _perf.sale_list[sale_idx_select]

        _perf.sales_count -= 1
        _perf.total_revenue -= _sale.revenue
        _perf.total_cost -= _sale.cost
        _perf.total_profit -= _sale.profit
        _perf.sale_list.remove(_sale)

        rating_sum = sum([sale.client_rating for sale in _perf.sale_list])
        _perf.average_rating = rating_sum / len(_perf.sale_list) if len(_perf.sale_list) else 0

        if os.getenv("HRMGR_DB") == "TRUE":
            employee_repo.update_one({"_id": _empl.id}, {"$set": _empl.dict()}, upsert=True)
        return ""

    def __get_info(self) -> str:
        if not the_company.logged_in_employee.is_admin:
            all_sales = tuple(the_company.logged_in_employee.performance.sale_list)
        else:
            all_sales = tuple(sale for employee in the_company.employees for sale in employee.performance.sale_list)
        sale_idx_select = get_user_option_from_list(
            "Select a sale to view info", tuple(sale.one_line_str() for sale in all_sales)
        )
        if sale_idx_select in (-1, -2):
            return NO_SALES_MSG if sale_idx_select == -1 else ""

        print(all_sales[sale_idx_select])
        input(ENTER_TO_CONTINUE_MSG)
        return ""

    def __find_submenu_admin(self) -> str:
        # fmt: off
        search_fields = [
            "[1] Sale ID",
            "[2] Client ID",
            "[3] Client rating",
            "[4] Date",
            "[5] Employee",
            "[else] Back"
        ]
        # fmt: on
        search_selection = get_user_option_from_menu("Find all sales by...", search_fields)
        all_sales = tuple(the_company.logged_in_employee.performance.sale_list)
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
        # fmt: off
        search_fields = [
            "[1] Sale ID",
            "[2] Client ID",
            "[3] Client rating",
            "[4] Date",
            "[else] Back"
        ]
        # fmt: on
        search_selection = get_user_option_from_menu("Find all sales by...", search_fields)
        all_sales = tuple(s for e in the_company.employees for s in e.performance.sale_list)
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

    def __find__by_sale_id(self, sales: tuple[Sale]) -> None:
        sale_id = input("Enter sale ID: ")
        sale = next((sale for sale in sales if sale.sale_id == sale_id), None)
        if not sale:
            return None
        clrscr()
        print(sale)
        input(ENTER_TO_CONTINUE_MSG)

    def __find__by_client_id(self, sales: tuple[Sale]) -> None:
        client_id = input("Enter client ID: ")
        found_sales = tuple(sale.one_line_str() for sale in sales if sale.client_id == client_id)
        if not found_sales:
            return None

        listing("All sales for client " + client_id, found_sales)

    def __find__by_client_rating(self, sales: tuple[Sale]) -> None:
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

    def __find__by_date(self, sales: tuple[Sale]) -> None:
        date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        try:
            date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        except:
            return None

        found_sales = tuple(sale for sale in sales if datetime.strftime(sale.date, "%Y-%m-%d") == date)
        if not sales:
            return None

        listing("All sales for date " + datetime.strftime(date, "%Y-%m-%d"), tuple(s.one_line_str() for s in found_sales))

    def __find__by_employee(self, sales: tuple[Sale]) -> None:
        empl_idx_select = get_user_option_from_list(
            "Select an employee to view sales for", tuple(f"{e.name} ({e.employee_id})" for e in the_company.employees)
        )
        if empl_idx_select in (-1, -2):
            return None

        empl_select = the_company.employees[empl_idx_select]
        found_sales = tuple(s for s in sales if s.employee_id == empl_select.employee_id)
        if not found_sales:
            return None

        listing("Sales of employee " + empl_select.name, tuple(s.one_line_str() for s in found_sales))
