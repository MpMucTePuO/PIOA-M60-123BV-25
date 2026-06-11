from .errors import (
    DuplicateEmployeeError,
    EmployeeNotFoundError,
    InvalidEmployeeDataError,
)
from .record import Record


class Table:
    columns = ("employee_id", "name", "position", "department", "salary")

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
        if not isinstance(employee_id, int):
            raise InvalidEmployeeDataError("ID должен быть целым числом.")
        if employee_id < 0:
            raise InvalidEmployeeDataError(
                "ID должен быть неотрицательным числом."
            )
        if any(record.employee_id == employee_id for record in self.records):
            raise DuplicateEmployeeError(
                f"Сотрудник с ID = {employee_id} уже существует."
            )

        if not isinstance(name, str):
            raise InvalidEmployeeDataError("Имя сотрудника должно быть строкой.")
        if not isinstance(position, str):
            raise InvalidEmployeeDataError("Должность должна быть строкой.")
        if not isinstance(department, str):
            raise InvalidEmployeeDataError("Отдел должен быть строкой.")

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
        try:
            if min_salary is not None:
                min_salary = float(min_salary)
            if max_salary is not None:
                max_salary = float(max_salary)
        except (TypeError, ValueError):
            raise InvalidEmployeeDataError(
                "Значение зарплаты для поиска должно быть числом."
            )

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

            if name is not None and not isinstance(name, str):
                raise InvalidEmployeeDataError(
                    "Имя сотрудника должно быть строкой."
                )
            if position is not None and not isinstance(position, str):
                raise InvalidEmployeeDataError(
                    "Должность должна быть строкой."
                )
            if department is not None and not isinstance(department, str):
                raise InvalidEmployeeDataError("Отдел должен быть строкой.")

            new_name = record.name if name is None else name.strip()
            new_position = (
                record.position if position is None else position.strip()
            )
            new_department = (
                record.department if department is None else department.strip()
            )
            new_salary = record.salary

            if salary is not None:
                try:
                    new_salary = float(salary)
                except (TypeError, ValueError):
                    raise InvalidEmployeeDataError(
                        "Зарплата должна быть числом."
                    )

            if not new_name:
                raise InvalidEmployeeDataError(
                    "Имя сотрудника не может быть пустым."
                )
            if not new_position:
                raise InvalidEmployeeDataError(
                    "Должность не может быть пустой."
                )
            if new_salary < 0:
                raise InvalidEmployeeDataError(
                    "Зарплата не может быть отрицательной."
                )

            record.name = new_name
            record.position = new_position
            record.department = new_department
            record.salary = new_salary
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
