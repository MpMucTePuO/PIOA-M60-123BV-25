import json
from pathlib import Path

from .database import Database
from .errors import EmployeeTableError, FileDatabaseError, InvalidStorageDataError
from .record import Record
from .table import Table


class FileDatabase(Database):
    def __init__(self, directory: str = "data"):
        self.directory = Path(directory)
        self.path = self.directory / "employees.json"

        try:
            self.directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise FileDatabaseError(
                "Не удалось создать каталог базы данных."
            ) from error

        if self.path.exists():
            self.employees = self._load()
        else:
            self.employees = Table("employees")
            self._save()

    def create_employee(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
    ) -> Record:
        record = self.employees.create(
            employee_id, name, position, department, salary
        )
        self._save()
        return record

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
        record = self.employees.update(
            employee_id, name, position, department, salary
        )
        self._save()
        return record

    def delete_employee(self, employee_id: int) -> Record:
        record = self.employees.delete(employee_id)
        self._save()
        return record

    def _load(self) -> Table:
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidStorageDataError(
                "Файл базы данных содержит некорректный JSON."
            ) from error
        except OSError as error:
            raise FileDatabaseError(
                "Не удалось прочитать файл базы данных."
            ) from error

        if not isinstance(data, dict):
            raise InvalidStorageDataError(
                "Файл базы данных имеет некорректную структуру."
            )
        if data.get("columns") != list(Table.columns):
            raise InvalidStorageDataError(
                "Структура таблицы в файле не соответствует программе."
            )
        if not isinstance(data.get("records"), list):
            raise InvalidStorageDataError(
                "Файл базы данных имеет некорректную структуру."
            )

        table = Table("employees")
        try:
            for record in data["records"]:
                if not isinstance(record, dict):
                    raise InvalidStorageDataError(
                        "Файл базы данных имеет некорректную структуру."
                    )
                if set(record) != set(Table.columns):
                    raise InvalidStorageDataError(
                        "Запись в файле не соответствует структуре таблицы."
                    )
                table.create(
                    record["employee_id"],
                    record["name"],
                    record["position"],
                    record["department"],
                    record["salary"],
                )
        except (EmployeeTableError, KeyError, TypeError) as error:
            raise InvalidStorageDataError(
                "Файл базы данных содержит некорректные записи."
            ) from error

        return table

    def _save(self) -> None:
        data = {
            "columns": list(Table.columns),
            "records": [
                {
                    "employee_id": record.employee_id,
                    "name": record.name,
                    "position": record.position,
                    "department": record.department,
                    "salary": record.salary,
                }
                for record in self.employees.records
            ],
        }

        try:
            with self.path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            raise FileDatabaseError(
                "Не удалось сохранить файл базы данных."
            ) from error
