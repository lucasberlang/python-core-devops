# Python Core Framework

A flexible and extensible core framework designed to Python application development by providing essential building blocks and utilities.

## 🌟 Features

- Configuration Management
- Logging System
- Database Abstraction Layer
- Security Utilities
- String and Date Utilities

## Project Structure

```
core/
├── database
    ├── azuretablestorage.py
    ├── __init__.py
├── logging
    ├── opentelemetrylogger.py
    ├── __init__.py
├── secrets
    ├── keyvaultmanager.py
    ├── __init__.py
├── utils
    ├── dateutils.py
    ├── stringutils.py
    ├── __init__.py
└── tests/
    ├── database
        ├── test_azuretablestorage.py
    ├── secrets
        ├── test_keyvaultmanager.py
    ├── utils
        ├── test_dateutils.py
        ├── test_stringutils.py
```

## 🚀 Installation

### Prerequisites

1. Install Python: Ensure you have Python 3.11 or newer installed on your system

    * [Download Python](https://www.python.org/downloads/)

2. Install Poetry: Poetry is required to manage dependencies and the virtual environment.

    * [Install Poetry](https://python-poetry.org/docs/)


### Clone the Repository

1. Clone the project from the repository:

```sh
    git clone framework_core
```

2. Clone the project from the repository:

```sh
    cd framework_core
```

### Install Dependencies

1. Install the project's dependencies using Poetry

```sh
    poetry install
```

This will:

* Create a virtual environment for the project.
* Install all required dependencies listed in pyproject.toml.

2. Activate the virtual environment (optional but recommended):

```sh
poetry shell
```

## Components

1. DateUtils: Handles date parsing, formatting, and calculations.

```python
from core.utils.dateutils import DateUtils

# Format date
formatted = DateUtils.format_date("2024-12-24", "%d/%m/%Y")  # "24/12/2024"

# Calculate difference
diff = DateUtils.get_date_diff("2024-12-24", "2024-12-25")  # 1 day
```

2. StringUtils: Provides string formatting and validation utilities.

```python
from core.utils.stringutils import StringUtils

# Format strings
snake = StringUtils.to_snake_case("helloWorld")  # hello_world
masked = StringUtils.mask_string("1234567890", expose_left=4)  # 1234******
```

3. AzureTableStorage: Manages Azure Table Storage operations.

```python
from core.database.azuretablestorage import AzureTableStorage

storage = AzureTableStorage("connection_string")
storage.create_table("users")

# Insert data
user = {
    "PartitionKey": "users",
    "RowKey": "1",
    "name": "John"
}
storage.insert_entity("users", user)
```

4. AzureOpenTelemetryLogger: Manages logging.

```python
from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger


logger = AzureOpenTelemetryLogger(logger_name=__name__).logger

    logger.info("This is a test of AzureOpenTelemetryLogger")
```

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request


## License

MIT License
