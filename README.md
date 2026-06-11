# База данных сотрудников

Степанов Михаил Витальевич

М60-123БВ-25

Python

Программа позволяет добавлять, искать, изменять и удалять сотрудников.
При запуске можно выбрать хранение данных в оперативной памяти или в
JSON-файле. Файловая база сохраняет записи после завершения программы.

## Структура проекта

```text
src/
└── db/
    ├── __main__.py
    ├── tui.py
    └── backend/
        ├── database.py
        ├── errors.py
        ├── file.py
        ├── memory.py
        ├── record.py
        └── table.py
tests/
├── test_file_database.py
└── test_memory.py
```

## Классы

- `Database` задаёт общий интерфейс базы данных.
- `Memory` хранит сотрудников в оперативной памяти.
- `FileDatabase` хранит сотрудников в файле `data/employees.json`.
- `Table` выполняет операции с записями и проверяет данные.
- `Record` хранит данные одного сотрудника.

Классы `Memory` и `FileDatabase` поддерживают одинаковые методы:
`create_employee`, `select_employees`, `update_employee` и
`delete_employee`.

При повреждённом JSON, неправильной структуре файла или ошибке чтения и
записи программа вызывает пользовательское исключение с понятным сообщением.

## Запуск программы

```bash
python -m src.db
```

После запуска необходимо выбрать тип базы данных:

- `1` — хранение в оперативной памяти;
- `2` — хранение в JSON-файле.

## Запуск тестов

```bash
python -m unittest discover -s tests -v
```

Проверка покрытия без модуля текстового интерфейса:

```bash
python -m pip install coverage
python -m coverage run --source=src.db.backend -m unittest discover -s tests
python -m coverage report
```
