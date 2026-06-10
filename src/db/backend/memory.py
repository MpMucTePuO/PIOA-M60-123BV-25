from .record import Record
from .table import Table


class Memory:
    def __init__(self):
        self.employees = Table("employees")

    def create_employee(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
    ) -> Record:
        return self.employees.create(
            employee_id, name, position, department, salary
        )

    def select_employees(
        self,
        employee_id: int | None = None,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        min_salary: float | None = None,
        max_salary: float | None = None,
    ) -> list[Record]:
        return self.employees.select(
            employee_id,
            name,
            position,
            department,
            min_salary,
            max_salary,
        )

    def update_employee(
        self,
        employee_id: int,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        salary: float | None = None,
    ) -> Record:
        return self.employees.update(
            employee_id, name, position, department, salary
        )

    def delete_employee(self, employee_id: int) -> Record:
        return self.employees.delete(employee_id)


database = Memory()
