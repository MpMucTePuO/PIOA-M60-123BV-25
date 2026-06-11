from abc import ABC, abstractmethod

from .record import Record


class Database(ABC):
    @abstractmethod
    def create_employee(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
    ) -> Record:
        pass

    @abstractmethod
    def select_employees(
        self,
        employee_id: int | None = None,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        min_salary: float | None = None,
        max_salary: float | None = None,
    ) -> list[Record]:
        pass

    @abstractmethod
    def update_employee(
        self,
        employee_id: int,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        salary: float | None = None,
    ) -> Record:
        pass

    @abstractmethod
    def delete_employee(self, employee_id: int) -> Record:
        pass
