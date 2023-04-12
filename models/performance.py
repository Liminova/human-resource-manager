import sys
import textwrap
from option import Result, Ok, Err
from datetime import datetime
from pydantic import BaseModel, Field

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Sale(BaseModel):
    sale_id: str = Field(default_factory=str)
    date: datetime = Field(default_factory=datetime.now)
    revenue: float = Field(default_factory=float)
    cost: float = Field(default_factory=float)
    profit: float = Field(default_factory=float)
    client_id: str = Field(default_factory=str)
    client_rating: float = Field(default_factory=float)
    client_comment: str = Field(default_factory=str)

    def set_sale_id(self, sale_id: str) -> Result[Self, str]:
        self.sale_id = sale_id
        return Ok(self) if sale_id != "" else Err("Sale ID cannot be empty.")

    def set_date(self, date: str) -> Result[Self, str]:
        date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        self.date = date
        return Ok(self)

    def set_revenue(self, revenue: str) -> Result[Self, str]:
        revenue = float(revenue)
        if revenue < 0:
            return Err("Revenue cannot be negative.")
        self.revenue = revenue
        return Ok(self)

    def set_cost(self, cost: str) -> Result[Self, str]:
        cost = float(cost)
        if cost < 0:
            return Err("Cost cannot be negative.")
        self.cost = cost
        return Ok(self)

    def set_profit(self, profit: str) -> Result[Self, str]:
        profit = float(profit)
        if profit < 0:
            return Err("Profit cannot be negative.")
        self.profit = profit
        return Ok(self)

    def set_client_id(self, client_id: str) -> Result[Self, str]:
        return Ok(self) if client_id != "" else Err("Client ID cannot be empty.")

    def set_client_rating(self, client_rating: str) -> Result[Self, str]:
        client_rating = float(client_rating)
        if client_rating < 1 or client_rating > 5:
            return Err("Client rating must be between 1 and 5.")
        self.client_rating = client_rating
        return Ok(self)

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
    sale_list: list[Sale] = Field(default_factory=list)
    sales_count: int = Field(default_factory=int)
    total_revenue: float = Field(default_factory=float)
    total_cost: float = Field(default_factory=float)
    total_profit: float = Field(default_factory=float)
    average_rating: float = Field(default_factory=float)

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

    def get_sales_by_date(self, date: datetime) -> list[Sale]:
        sales: list[Sale] = []
        for sale in self.sale_list:
            if sale.date == date:
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
