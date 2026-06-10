import unittest

from src.db.backend.errors import (
    DuplicateEmployeeError,
    EmployeeNotFoundError,
    InvalidEmployeeDataError,
)
from src.db.backend.memory import Memory
from src.db.backend.record import Record
from src.db.backend.table import Table


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_record_create(self):
        record = Record(1, "Иван", "Разработчик", "ИТ", 50000)

        self.assertEqual(record.employee_id, 1)
        self.assertEqual(record.name, "Иван")
        self.assertEqual(record.position, "Разработчик")
        self.assertEqual(record.department, "ИТ")
        self.assertEqual(record.salary, 50000)

    def test_memory_create(self):
        self.assertIsInstance(self.memory.employees, Table)
        self.assertEqual(self.memory.employees.name, "employees")

    def test_create_employee(self):
        cases = [
            (1, " Иван ", " Разработчик ", " ИТ ", 50000),
            (2, "Анна", "Бухгалтер", "Финансы", 70000),
            (3, "Олег", "Менеджер", "Продажи", 60000),
        ]

        for data in cases:
            with self.subTest(data=data):
                record = self.memory.create_employee(*data)
                self.assertEqual(record.employee_id, data[0])
                self.assertEqual(record.name, data[1].strip())
                self.assertEqual(record.position, data[2].strip())
                self.assertEqual(record.department, data[3].strip())
                self.assertEqual(record.salary, float(data[4]))

    def test_create_employee_incorrect_data(self):
        cases = [
            (
                (-1, "Иван", "Разработчик", "ИТ", 50000),
                InvalidEmployeeDataError,
                "ID должен быть неотрицательным числом.",
            ),
            (
                (1, "", "Разработчик", "ИТ", 50000),
                InvalidEmployeeDataError,
                "Имя сотрудника не может быть пустым.",
            ),
            (
                (1, "Иван", " ", "ИТ", 50000),
                InvalidEmployeeDataError,
                "Должность не может быть пустой.",
            ),
            (
                (1, "Иван", "Разработчик", "ИТ", -1),
                InvalidEmployeeDataError,
                "Зарплата не может быть отрицательной.",
            ),
        ]

        for data, error, message in cases:
            with self.subTest(data=data):
                with self.assertRaises(error) as context:
                    self.memory.create_employee(*data)
                self.assertEqual(str(context.exception), message)

    def test_create_employee_duplicate_id(self):
        self.memory.create_employee(1, "Иван", "Разработчик", "ИТ", 50000)

        with self.assertRaises(DuplicateEmployeeError) as context:
            self.memory.create_employee(1, "Анна", "Бухгалтер", "Финансы", 70000)

        self.assertEqual(
            str(context.exception),
            "Сотрудник с ID = 1 уже существует.",
        )

    def test_select_employee(self):
        first = self.memory.create_employee(
            1, "Иван", "Разработчик", "ИТ", 50000
        )
        second = self.memory.create_employee(
            2, "Анна", "Бухгалтер", "Финансы", 70000
        )

        cases = [
            ({}, [first, second]),
            ({"employee_id": 1}, [first]),
            ({"name": "Анна"}, [second]),
            ({"position": "Бухгалтер"}, [second]),
            ({"department": "ИТ"}, [first]),
            ({"min_salary": 60000}, [second]),
            ({"max_salary": 60000}, [first]),
            ({"name": "Сергей"}, []),
        ]

        for filters, expected in cases:
            with self.subTest(filters=filters):
                self.assertEqual(
                    self.memory.select_employees(**filters),
                    expected,
                )

    def test_update_employee(self):
        self.memory.create_employee(1, "Иван", "Разработчик", "ИТ", 50000)
        self.memory.create_employee(2, "Анна", "Бухгалтер", "Финансы", 70000)

        record = self.memory.update_employee(
            2,
            name=" Пётр ",
            position=" Тестировщик ",
            department=" Контроль ",
            salary=80000,
        )

        self.assertEqual(record.name, "Пётр")
        self.assertEqual(record.position, "Тестировщик")
        self.assertEqual(record.department, "Контроль")
        self.assertEqual(record.salary, 80000.0)

    def test_update_employee_incorrect_data(self):
        self.memory.create_employee(1, "Иван", "Разработчик", "ИТ", 50000)

        cases = [
            ({"name": ""}, "Имя сотрудника не может быть пустым."),
            ({"position": " "}, "Должность не может быть пустой."),
            ({"salary": -100}, "Зарплата не может быть отрицательной."),
        ]

        for fields, message in cases:
            with self.subTest(fields=fields):
                with self.assertRaises(InvalidEmployeeDataError) as context:
                    self.memory.update_employee(1, **fields)
                self.assertEqual(str(context.exception), message)

    def test_update_employee_not_found(self):
        with self.assertRaises(EmployeeNotFoundError) as context:
            self.memory.update_employee(10, name="Олег")

        self.assertEqual(
            str(context.exception),
            "Сотрудник с ID = 10 не найден.",
        )

    def test_delete_employee(self):
        record = self.memory.create_employee(
            1, "Иван", "Разработчик", "ИТ", 50000
        )

        self.assertIs(self.memory.delete_employee(1), record)

    def test_delete_employee_not_found(self):
        with self.assertRaises(EmployeeNotFoundError) as context:
            self.memory.delete_employee(10)

        self.assertEqual(
            str(context.exception),
            "Сотрудник с ID = 10 не найден.",
        )


if __name__ == "__main__":
    unittest.main()
