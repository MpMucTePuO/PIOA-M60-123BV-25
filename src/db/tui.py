from .backend.memory import (
    create_employee,
    select_employees,
    update_employee,
    delete_employee,
)


def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
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
        raw = input(prompt).strip().replace(",", ".")
        if raw == "":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число или оставьте поле пустым.")


def _read_nonempty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def _print_employees(records: list) -> None:
    if not records:
        print("Сотрудники не найдены.")
        return
    print(f"{'ID'} - {'Имя'} - {'Должность'} - {'Отдел'} - {'Зарплата'}")
    for r in records:
        print(f"{r[0]} - {r[1]} - {r[2]} - {r[3]} - {r[4]:.2f}")


def _add_employee() -> None:
    print("\n  Добавление сотрудника  ")
    employee_id = _read_int("ID сотрудника: ")
    name = _read_nonempty_string("Имя: ")
    position = _read_nonempty_string("Должность: ")
    department = input("Отдел: ").strip()
    salary = _read_float("Зарплата: ")
    try:
        _print_employees([create_employee(employee_id, name, position, department, salary)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _find_employees() -> None:
    print("\n  Поиск сотрудников  ")
    print("Введите критерии поиска (пустое поле = пропустить фильтр):")
    employee_id = _read_optional_int("ID сотрудника: ")
    name = input("Имя: ").strip() or None
    position = input("Должность: ").strip() or None
    department = input("Отдел: ").strip() or None
    min_salary = _read_optional_float("Минимальная зарплата: ")
    max_salary = _read_optional_float("Максимальная зарплата: ")
    _print_employees(
        select_employees(employee_id, name, position, department, min_salary, max_salary)
    )


def _update_employee() -> None:
    print("\n   Обновление сотрудника   ")
    employee_id = _read_int("ID сотрудника для обновления: ")
    print("Введите новые значения (пустое поле — без изменений):")
    name = input("Новое имя: ").strip() or None
    position = input("Новая должность: ").strip() or None
    department = input("Новый отдел: ").strip() or None
    salary = _read_optional_float("Новая зарплата: ")
    try:
        _print_employees([update_employee(employee_id, name, position, department, salary)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _delete_employee() -> None:
    print("\n   Удаление сотрудника  ")
    employee_id = _read_int("ID сотрудника для удаления: ")
    try:
        _print_employees([delete_employee(employee_id)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def run() -> None:
    actions = {
        "1": _add_employee,
        "2": _find_employees,
        "3": _update_employee,
        "4": _delete_employee,
        "5": lambda: _print_employees(select_employees()),
    }
    while True:
        print("\nБаза данных 'Сотрудники компании' (in-memory)")
        print("1. Добавить сотрудника")
        print("2. Найти сотрудников")
        print("3. Обновить сотрудника")
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
            print("Неверный ввод. Повторите.")