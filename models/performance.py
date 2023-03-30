import sys, textwrap
from option import Result, Ok, Err
from datetime import datetime

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Sale:
    def __init__(self) -> None:
        self.__sale_id = ""
        self.__date: datetime = datetime.now()
        self.__revenue = 0.0
        self.__cost = 0.0
        self.__profit = 0.0
        self.__client_id = ""
        self.__client_rating = 0.0  # float, from 1-5
        self.__client_comment = ""

    @property
    def sale_id(self) -> str:
        return self.__sale_id

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def revenue(self) -> float:
        return self.__revenue

    @property
    def cost(self) -> float:
        return self.__cost

    @property
    def profit(self) -> float:
        return self.__profit

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def client_rating(self) -> float:
        return self.__client_rating

    @property
    def client_comment(self) -> str:
        return self.__client_comment

    def set_sale_id(self, sale_id: str) -> Result[Self, str]:
        self.__sale_id = sale_id
        return Ok(self) if sale_id != "" else Err("Sale ID cannot be empty.")

    def set_date(self, date: datetime) -> Result[Self, str]:
        self.__date = date
        return Ok(self) if date != "" else Err("Date cannot be empty.")

    def set_revenue(self, revenue: float) -> Result[Self, str]:
        self.__revenue = revenue
        return Ok(self) if revenue >= 0 else Err("Revenue cannot be negative.")

    def set_cost(self, cost: float) -> Result[Self, str]:
        self.__cost = cost
        return Ok(self) if cost >= 0 else Err("Cost cannot be negative.")

    def set_profit(self, profit: float) -> Result[Self, str]:
        self.__profit = profit
        return Ok(self) if profit >= 0 else Err("Profit cannot be negative.")

    def set_client_id(self, client_id: str) -> Result[Self, str]:
        return Ok(self) if client_id != "" else Err("Client ID cannot be empty.")

    def set_client_rating(self, client_rating: float) -> Result[Self, str]:
        self.__client_rating = client_rating
        return Ok(self) if client_rating >= 1 and client_rating <= 5 else Err("Client rating must be between 1 and 5.")

    def set_client_comment(self, client_comment: str) -> Result[Self, str]:
        self.__client_comment = client_comment
        return Ok(self) if client_comment != "" else Err("Client comment cannot be empty.")

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Sale ID: {self.sale_id}
            - Revenue: {self.revenue}
            - Cost: {self.cost}
            - Profit: {self.profit}
            - Client ID: {self.client_id}
            - Client rating: {self.client_rating}
            - Client comment: {self.client_comment}\
            """)
        return data


class Performance:
    """Monitoring an employee's performance."""

    def __init__(self) -> None:
        self.__sale_list = []
        self.__sales_count = 0
        self.__total_revenue = 0
        self.__total_cost = 0
        self.__total_profit = 0
        self.__average_rating = 0

    @property
    def sale_list(self) -> list:
        return self.__sale_list

    @property
    def sales_count(self) -> int:
        return self.__sales_count

    @property
    def total_revenue(self) -> float:
        return self.__total_revenue

    @property
    def total_cost(self) -> float:
        return self.__total_cost

    @property
    def total_profit(self) -> float:
        return self.__total_profit

    @property
    def average_rating(self) -> float:
        return self.__average_rating

    def add_sale(self, sale: Sale) -> None:
        self.__sales_count += 1
        self.__total_revenue += sale.revenue
        self.__total_cost += sale.cost
        self.__total_profit += sale.profit
        self.__sale_list.append(sale)
        self.calculate_average_rating()

    def calculate_average_rating(self) -> None:
        total_rating = 0
        for sale in self.__sale_list:
            total_rating += sale.client_rating
        if self.__sales_count == 0:
            self.__average_rating = 0
        else:
            self.__average_rating = round(total_rating / self.__sales_count, 1)

    def get_sale_by_id(self, sale_id: str) -> Sale | None:
        for sale in self.__sale_list:
            if sale.sale_id == sale_id:
                return sale
        return None

    def get_sales_by_client_id(self, client_id: str) -> list[Sale]:
        sales = []
        for sale in self.__sale_list:
            if sale.client_id == client_id:
                sales.append(sale)
        return sales

    def get_sales_by_rating(self, rating: int) -> list[Sale]:
        sales = []
        if rating == 0:
            return self.__sale_list
        else:
            for sale in self.__sale_list:
                if sale.client_rating >= rating and sale.client_rating < rating + 1:
                    sales.append(sale)
            return sales

    def get_sales_by_date(self, date: str) -> list[Sale]:
        sales = []
        for sale in self.__sale_list:
            if sale.sale_id.date() == date:
                sales.append(sale)
        return sales

    def __str__(self) -> str:
        data = textwrap.dedent(f"""\
            - Sales count: {self.sales_count}
            - Total revenue: {self.total_revenue}
            - Total cost: {self.total_cost}
            - Total profit: {self.total_profit}
            - Average rating: {self.average_rating}\
            """)
        return data