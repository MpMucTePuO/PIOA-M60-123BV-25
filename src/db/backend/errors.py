class EmployeeTableError(Exception):
    pass


class InvalidEmployeeDataError(EmployeeTableError):
    pass


class DuplicateEmployeeError(EmployeeTableError):
    pass


class EmployeeNotFoundError(EmployeeTableError):
    pass
