type EmployeeRecord = tuple[int, str, str, str, float]

Employees: list[EmployeeRecord] = []


def _employee_exists(employee_id: int) -> bool:
    return any(r[0] == employee_id for r in Employees)


def create_employee(
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: float,
) -> EmployeeRecord:
    if employee_id < 0:
        raise ValueError("ID должен быть неотрицательным числом.")
    if _employee_exists(employee_id):
        raise ValueError(f"Сотрудник с ID = {employee_id} уже существует.")
    if not name.strip():
        raise ValueError("Имя сотрудника не может быть пустым.")
    if not position.strip():
        raise ValueError("Должность не может быть пустой.")
    if salary < 0:
        raise ValueError("Зарплата не может быть отрицательной.")

    record: EmployeeRecord = (
        employee_id,
        name.strip(),
        position.strip(),
        department.strip(),
        float(salary),
    )
    Employees.append(record)
    return record


def select_employees(
        employee_id: int | None = None,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        min_salary: float | None = None,
        max_salary: float | None = None,
) -> list[EmployeeRecord]:
    return [
        r for r in Employees
        if (employee_id is None or r[0] == employee_id)
           and (name is None or r[1] == name)
           and (position is None or r[2] == position)
           and (department is None or r[3] == department)
           and (min_salary is None or r[4] >= min_salary)
           and (max_salary is None or r[4] <= max_salary)
    ]


def update_employee(
        employee_id: int,
        name: str | None = None,
        position: str | None = None,
        department: str | None = None,
        salary: float | None = None,
) -> EmployeeRecord:
    for i, record in enumerate(Employees):
        if record[0] == employee_id:
            new_name = name.strip() if name is not None else record[1]
            new_position = position.strip() if position is not None else record[2]
            new_department = department.strip() if department is not None else record[3]
            new_salary = float(salary) if salary is not None else record[4]

            if name is not None and not new_name:
                raise ValueError("Имя сотрудника не может быть пустым.")
            if position is not None and not new_position:
                raise ValueError("Должность не может быть пустой.")
            if salary is not None and new_salary < 0:
                raise ValueError("Зарплата не может быть отрицательной.")

            updated: EmployeeRecord = (
                employee_id, new_name, new_position, new_department, new_salary,
            )
            Employees[i] = updated
            return updated

    raise ValueError(f"Сотрудник с ID = {employee_id} не найден.")


def delete_employee(employee_id: int) -> EmployeeRecord:
    for i, record in enumerate(Employees):
        if record[0] == employee_id:
            return Employees.pop(i)
    raise ValueError(f"Сотрудник с ID = {employee_id} не найден.")
