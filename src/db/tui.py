from .backend.database import Database
from .backend.errors import DatabaseError
from .backend.file import FileDatabase
from .backend.memory import Memory
from .backend.record import Record


database: Database = Memory()


def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def _read_optional_int(prompt: str) -> int | None:
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Ошибка: введите число.")


def _read_optional_float(prompt: str) -> float | None:
    while True:
        value = input(prompt).strip().replace(",", ".")
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Ошибка: введите число или оставьте поле пустым.")


def _read_nonempty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def _print_employees(records: list[Record]) -> None:
    if not records:
        print("Сотрудники не найдены.")
        return

    print("ID - Имя - Должность - Отдел - Зарплата")
    for record in records:
        print(
            f"{record.employee_id} - {record.name} - {record.position} - "
            f"{record.department} - {record.salary:.2f}"
        )


def _add_employee() -> None:
    print("\nДобавление сотрудника")
    employee_id = _read_int("ID сотрудника: ")
    name = _read_nonempty_string("Имя: ")
    position = _read_nonempty_string("Должность: ")
    department = input("Отдел: ").strip()
    salary = _read_float("Зарплата: ")
    try:
        _print_employees(
            [
                database.create_employee(
                    employee_id, name, position, department, salary
                )
            ]
        )
    except DatabaseError as error:
        print(f"Ошибка: {error}")


def _find_employees() -> None:
    print("\nПоиск сотрудников")
    print("Пустое поле означает, что фильтр использоваться не будет.")
    employee_id = _read_optional_int("ID сотрудника: ")
    name = input("Имя: ").strip() or None
    position = input("Должность: ").strip() or None
    department = input("Отдел: ").strip() or None
    min_salary = _read_optional_float("Минимальная зарплата: ")
    max_salary = _read_optional_float("Максимальная зарплата: ")
    records = database.select_employees(
        employee_id, name, position, department, min_salary, max_salary
    )
    _print_employees(records)


def _update_employee() -> None:
    print("\nИзменение сотрудника")
    employee_id = _read_int("ID сотрудника для изменения: ")
    print("Оставьте поле пустым, если его не нужно изменять.")
    name = input("Новое имя: ").strip() or None
    position = input("Новая должность: ").strip() or None
    department = input("Новый отдел: ").strip() or None
    salary = _read_optional_float("Новая зарплата: ")
    try:
        record = database.update_employee(
            employee_id, name, position, department, salary
        )
        _print_employees([record])
    except DatabaseError as error:
        print(f"Ошибка: {error}")


def _delete_employee() -> None:
    print("\nУдаление сотрудника")
    employee_id = _read_int("ID сотрудника для удаления: ")
    try:
        _print_employees([database.delete_employee(employee_id)])
    except DatabaseError as error:
        print(f"Ошибка: {error}")


def run() -> None:
    global database

    while True:
        print("Выберите тип базы данных:")
        print("1. Оперативная память")
        print("2. Файловая база данных")
        choice = input("Введите номер: ").strip()

        if choice not in {"1", "2"}:
            print("Неверный ввод. Выберите 1 или 2.")
            continue

        try:
            if choice == "2":
                database = FileDatabase()
            else:
                database = Memory()
            break
        except DatabaseError as error:
            print(f"Ошибка: {error}")
            return

    actions = {
        "1": _add_employee,
        "2": _find_employees,
        "3": _update_employee,
        "4": _delete_employee,
        "5": lambda: _print_employees(database.select_employees()),
    }

    while True:
        print("\nБаза данных сотрудников компании")
        print("1. Добавить сотрудника")
        print("2. Найти сотрудников")
        print("3. Изменить сотрудника")
        print("4. Удалить сотрудника")
        print("5. Показать всех сотрудников")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Выход из программы.")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный ввод. Повторите попытку.")
