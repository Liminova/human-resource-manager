# example class for employee (i.e. consider adding this to models/employee.py)
class Employee:
    """Employee class for login system."""
    def __init__(self, username: str, password: str, role: str) -> None:
        self.username = username
        self.password = password
        self.role = role
        return None

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

# example class for admin (i.e. consider adding this to models/admin.py)
class Admin(Employee):
    """Admin class for login system."""
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password, "admin")
        return None

# login system
class Login:
    """Login system for employees and managers."""
    def __init__(self) -> None:
        self.employees = []
        self.admins = []
        return None

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)
        return None

    def add_admin(self, admin: Admin) -> None:
        self.admins.append(admin)
        return None

    def login(self, username: str, password: str) -> Result[Employee | Admin, str]:
        for employee in self.employees:
            if employee.username == username and employee.password == password:
                return Ok(employee)
        for admin in self.admins:
            if admin.username == username and admin.password == password:
                return Ok(admin)
        return Err("Invalid username or password.")