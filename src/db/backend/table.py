from .errors import (
    DuplicateEmployeeError,
    EmployeeNotFoundError,
    InvalidEmployeeDataError,
)
from .record import Record


class Table:
    def __init__(self, name: str):
        self.name = name
        self.records: list[Record] = []

    def create(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
    ) -> Record:
        if employee_id < 0:
            raise InvalidEmployeeDataError(
                "ID должен быть неотрицательным числом."
            )
        if any(record.employee_id == employee_id for record in self.records):
            raise DuplicateEmployeeError(
                f"Сотрудник с ID = {employee_id} уже существует."
            )

        name = name.strip()
        position = position.strip()
        department = department.strip()
        try:
            salary = float(salary)
        except (TypeError, ValueError):
            raise InvalidEmployeeDataError("Зарплата должна быть числом.")

        if not name:
            raise InvalidEmployeeDataError(
                "Имя сотрудника не может быть пустым."
            )
        if not position:
            raise InvalidEmployeeDataError("Должность не может быть пустой.")
        if salary < 0:
            raise InvalidEmployeeDataError(
                "Зарплата не может быть отрицательной."
            )

        record = Record(employee_id, name, position, department, salary)
        self.records.append(record)
        return record

    def select(
        self,
        employee_id: int | None = None,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        min_salary: float | None = None,
        max_salary: float | None = None,
    ) -> list[Record]:
        result = []
        for record in self.records:
            if employee_id is not None and record.employee_id != employee_id:
                continue
            if name is not None and record.name != name:
                continue
            if position is not None and record.position != position:
                continue
            if department is not None and record.department != department:
                continue
            if min_salary is not None and record.salary < min_salary:
                continue
            if max_salary is not None and record.salary > max_salary:
                continue
            result.append(record)
        return result

    def update(
        self,
        employee_id: int,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        salary: float | None = None,
    ) -> Record:
        for record in self.records:
            if record.employee_id != employee_id:
                continue

            if name is not None:
                name = name.strip()
                if not name:
                    raise InvalidEmployeeDataError(
                        "Имя сотрудника не может быть пустым."
                    )
                record.name = name

            if position is not None:
                position = position.strip()
                if not position:
                    raise InvalidEmployeeDataError(
                        "Должность не может быть пустой."
                    )
                record.position = position

            if department is not None:
                record.department = department.strip()

            if salary is not None:
                try:
                    salary = float(salary)
                except (TypeError, ValueError):
                    raise InvalidEmployeeDataError(
                        "Зарплата должна быть числом."
                    )
                if salary < 0:
                    raise InvalidEmployeeDataError(
                        "Зарплата не может быть отрицательной."
                    )
                record.salary = salary

            return record

        raise EmployeeNotFoundError(
            f"Сотрудник с ID = {employee_id} не найден."
        )

    def delete(self, employee_id: int) -> Record:
        for record in self.records:
            if record.employee_id == employee_id:
                self.records.remove(record)
                return record
        raise EmployeeNotFoundError(
            f"Сотрудник с ID = {employee_id} не найден."
        )
