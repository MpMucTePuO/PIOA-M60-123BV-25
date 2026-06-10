class Record:
    def __init__(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
    ):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
