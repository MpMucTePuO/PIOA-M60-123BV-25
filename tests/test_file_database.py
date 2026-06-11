import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.db.backend.database import Database
from src.db.backend.errors import FileDatabaseError, InvalidStorageDataError
from src.db.backend.file import FileDatabase
from src.db.backend.memory import Memory
from src.db.backend.table import Table


class TestFileDatabase(unittest.TestCase):
    def test_database_interface(self):
        class DummyDatabase(Database):
            def create_employee(self, *args, **kwargs):
                return super().create_employee(*args, **kwargs)

            def select_employees(self, *args, **kwargs):
                return super().select_employees(*args, **kwargs)

            def update_employee(self, *args, **kwargs):
                return super().update_employee(*args, **kwargs)

            def delete_employee(self, *args, **kwargs):
                return super().delete_employee(*args, **kwargs)

        dummy = DummyDatabase()

        self.assertIsNone(
            dummy.create_employee(1, "Иван", "Разработчик", "ИТ", 50000)
        )
        self.assertIsNone(dummy.select_employees())
        self.assertIsNone(dummy.update_employee(1, salary=60000))
        self.assertIsNone(dummy.delete_employee(1))

    def test_common_interface(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsInstance(Memory(), Database)
            self.assertIsInstance(FileDatabase(directory), Database)

    def test_file_create(self):
        with tempfile.TemporaryDirectory() as directory:
            database = FileDatabase(directory)
            path = Path(directory) / "employees.json"

            self.assertTrue(path.exists())
            self.assertIsInstance(database.employees, Table)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["columns"], list(Table.columns))
            self.assertEqual(data["records"], [])

    def test_data_is_saved_between_instances(self):
        with tempfile.TemporaryDirectory() as directory:
            first_database = FileDatabase(directory)
            first_database.create_employee(
                1, "Иван", "Разработчик", "ИТ", 50000
            )

            second_database = FileDatabase(directory)
            records = second_database.select_employees()

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].name, "Иван")

    def test_changes_are_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            database = FileDatabase(directory)
            database.create_employee(
                1, "Иван", "Разработчик", "ИТ", 50000
            )
            database.update_employee(1, position="Тестировщик", salary=60000)

            updated_database = FileDatabase(directory)
            record = updated_database.select_employees(employee_id=1)[0]
            self.assertEqual(record.position, "Тестировщик")
            self.assertEqual(record.salary, 60000.0)

            updated_database.delete_employee(1)
            empty_database = FileDatabase(directory)
            self.assertEqual(empty_database.select_employees(), [])

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "employees.json"
            path.write_text("{", encoding="utf-8")

            with self.assertRaises(InvalidStorageDataError):
                FileDatabase(directory)

    def test_invalid_structure(self):
        cases = [
            [],
            {"columns": [], "records": []},
            {"columns": list(Table.columns), "records": "не список"},
            {"columns": list(Table.columns), "records": [[]]},
            {
                "columns": list(Table.columns),
                "records": [{"employee_id": 1}],
            },
            {
                "columns": list(Table.columns),
                "records": [
                    {
                        "employee_id": 1,
                        "name": "",
                        "position": "Разработчик",
                        "department": "ИТ",
                        "salary": 50000,
                    }
                ],
            },
        ]

        for data in cases:
            with self.subTest(data=data):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "employees.json"
                    path.write_text(
                        json.dumps(data, ensure_ascii=False),
                        encoding="utf-8",
                    )

                    with self.assertRaises(InvalidStorageDataError):
                        FileDatabase(directory)

    def test_directory_create_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file"
            path.write_text("данные", encoding="utf-8")

            with self.assertRaises(FileDatabaseError):
                FileDatabase(str(path / "data"))

    def test_file_read_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "employees.json"
            path.write_text("{}", encoding="utf-8")

            with patch.object(Path, "open", side_effect=OSError):
                with self.assertRaises(FileDatabaseError):
                    FileDatabase(directory)

    def test_file_save_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(Path, "open", side_effect=OSError):
                with self.assertRaises(FileDatabaseError):
                    FileDatabase(directory)


if __name__ == "__main__":
    unittest.main()
