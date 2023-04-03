import sys
import textwrap
from option import Result, Ok, Err
from datetime import datetime
from pydantic import BaseModel

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Sale(BaseModel):
    sale_id = ""
    date: datetime = datetime.now()
    revenue = 0.0
    cost = 0.0
    profit = 0.0
    client_id = ""
    client_rating = 0.0
    client_comment = ""

    def set_sale_id(self, sale_id: str) -> Result[Self, str]:
        self.sale_id = sale_id
        return Ok(self) if sale_id != "" else Err("Sale ID cannot be empty.")

    def set_date(self, date: datetime) -> Result[Self, str]:
        self.date = date
        return Ok(self) if date != "" else Err("Date cannot be empty.")

    def set_revenue(self, revenue: float) -> Result[Self, str]:
        self.revenue = revenue
        return Ok(self) if revenue >= 0 else Err("Revenue cannot be negative.")

    def set_cost(self, cost: float) -> Result[Self, str]:
        self.cost = cost
        return Ok(self) if cost >= 0 else Err("Cost cannot be negative.")

    def set_profit(self, profit: float) -> Result[Self, str]:
        self.profit = profit
        return Ok(self) if profit >= 0 else Err("Profit cannot be negative.")

    def set_client_id(self, client_id: str) -> Result[Self, str]:
        return Ok(self) if client_id != "" else Err("Client ID cannot be empty.")

    def set_client_rating(self, client_rating: float) -> Result[Self, str]:
        self.client_rating = client_rating
        return Ok(self) if client_rating >= 1 and client_rating <= 5 else Err("Client rating must be between 1 and 5.")

    def set_client_comment(self, client_comment: str) -> Result[Self, str]:
        self.client_comment = client_comment
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


class Performance(BaseModel):
    """Monitoring an employee's performance."""

    sale_list: list[Sale] = []
    sale_count = 0
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    average_rating = 0

    def add_sale(self, sale: Sale) -> None:
        self.sales_count += 1
        self.total_revenue += sale.revenue
        self.total_cost += sale.cost
        self.total_profit += sale.profit
        self.sale_list.append(sale)
        self.calculate_average_rating()

    def calculate_average_rating(self) -> None:
        total_rating = 0
        for sale in self.sale_list:
            total_rating += sale.client_rating
        if self.sales_count == 0:
            self.average_rating = 0
        else:
            self.average_rating = round(total_rating / self.sales_count, 1)

    def get_sale_by_id(self, sale_id: str) -> Sale | None:
        for sale in self.sale_list:
            if sale.sale_id == sale_id:
                return sale
        return None

    def get_sales_by_client_id(self, client_id: str) -> list[Sale]:
        sales: list[Sale] = []
        for sale in self.sale_list:
            if sale.client_id == client_id:
                sales.append(sale)
        return sales

    def get_sales_by_rating(self, rating: int) -> list[Sale]:
        sales: list[Sale] = []
        if rating == 0:
            return self.sale_list
        else:
            for sale in self.sale_list:
                if sale.client_rating >= rating and sale.client_rating < rating + 1:
                    sales.append(sale)
            return sales

        sales = []
        for sale in self.sale_list:
            if sale.sale_id.date() == date:
        for sale in self.sale_list:
            if datetime.strptime(sale.date, "%Y-%m-%d") == datetime.strptime(date, "%Y-%m-%d"):
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

    class Config:
        arbitrary_types_allowed = True
