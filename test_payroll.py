class payroll:          # tính lương theo tháng của mỗi nhân viên
    def __init__(self) -> None:
        __salary = 0    #lương cứng
        __bonus = 0     #thưởng
        __tax = 0       #thuế
        __punish = 0    #phạt
        __total = 0     #tổng lương

        #punishment depends on the number of days absent
        #bonus depends on the number of days present and performance
        # so I need to import the class attendance and performance from Duc's code
        #this code is just the core of the payroll class, I will fix later after reading Duc's code

    def get_salary(self) -> int:
        return self.__salary
    
    def get_bonus(self) -> int:
        return self.__bonus
    
    def get_tax(self) -> int:
        return self.__tax
    
    def get_punish(self) -> int:
        return self.__punish
    
    def get_total(self) -> int:
        return self.__total
    
    def set_salary(self, salary: int) -> None:
        self.__salary = salary

    def set_bonus(self, bonus: int) -> None:
        self.__bonus = bonus

    def set_tax(self, tax: int) -> None:
        self.__tax = tax
    
    def set_punish(self, punish: int) -> None:
        self.__punish = punish
    
    def set_total(self, total: int) -> None:
        self.__total = total

    def calculate(self) -> None:
        self.__total = self.__salary + self.__bonus - self.__tax - self.__punish

    def set_month(self) -> None:
        while True:
            month = input("Enter month: ")
            if month >=1 and month <= 12:
                self.__month = month
                break
            else:
                print("Invalid month! Enter again!")
                
    def get_month(self) -> int:
        return self.__month
    
    def set_year(self) -> None:
        while True:
            year = input("Enter year: ")
            if year >= 2000:
                self.__year = year
                break
            else:
                print("Invalid ! Enter again!")

    def get_year(self) -> int:
        return self.__year

    def display(self) -> None:
        print(f"Month: {self.__month}")
        print(f"Salary: {self.__salary}")
        print(f"Bonus: {self.__bonus}")
        print(f"Tax: {self.__tax}")
        print(f"Punish: {self.__punish}")
        print(f"Total: {self.__total}")

    



