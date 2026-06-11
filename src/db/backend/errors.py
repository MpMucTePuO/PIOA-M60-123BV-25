class DatabaseError(Exception):
    pass


class EmployeeTableError(DatabaseError):
    pass


class InvalidEmployeeDataError(EmployeeTableError):
    pass


class DuplicateEmployeeError(EmployeeTableError):
    pass


class EmployeeNotFoundError(EmployeeTableError):
    pass


class FileDatabaseError(DatabaseError):
    pass


class InvalidStorageDataError(FileDatabaseError):
    pass
