import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Sale:
    def __init__(self) -> None:
        self.__sale_id = "" # YYYYMMDDHHMM_CLIEND_ID
        self.__revenue = 0.0
        self.__cost = 0.0
        self.__profit = 0.0
        self.__client_id = ""
        self.__client_rating = 0.0 # float, from 1-5
        self.__client_comment = ""

    @property
    def sale_id(self) -> str:
        return self.__sale_id

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

    @sale_id.setter
    def sale_id(self, sale_id: str) -> Self:
        self.__sale_id = sale_id
        return self

    @revenue.setter
    def revenue(self, revenue: float) -> Self:
        self.__revenue = revenue
        return self

    @cost.setter
    def cost(self, cost: float) -> Self:
        self.__cost = cost
        return self

    @profit.setter
    def profit(self, profit: float) -> Self:
        self.__profit = profit
        return self

    @client_id.setter
    def client_id(self, client_id: str) -> Self:
        self.__client_id = client_id
        return self

    @client_rating.setter
    def client_rating(self, client_rating: float) -> Self:
        self.__client_rating = client_rating
        return self

    @client_comment.setter
    def client_comment(self, client_comment: str) -> Self:
        self.__client_comment = client_comment
        return self

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

    def get_sale_by_id(self, sale_id: str) -> Sale:
        for sale in self.__sale_list:
            if sale.sale_id == sale_id:
                return sale
        return None

    def get_sales_by_client_id(self, client_id: str) -> list:
        sales = []
        for sale in self.__sale_list:
            if sale.client_id == client_id:
                sales.append(sale)
        return sales

    def get_sales_by_rating(self, rating: int) -> list:
        sales = []
        if rating == 0:
            return self.__sale_list
        else:
            for sale in self.__sale_list:
                if sale.client_rating >= rating and sale.client_rating < rating + 1:
                    sales.append(sale)
            return sales

    def get_sales_by_date(self, date: str) -> list:
        sales = []
        for sale in self.__sale_list:
            if sale.sale_id.startswith(date):
                sales.append(sale)
        return sales