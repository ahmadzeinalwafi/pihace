# pihace

**Python Integrated Health Check (pihace)** is a modular and extensible Python library for system and service health monitoring. It helps you build consistent, informative, and developer-friendly health check endpoints or tools across your applications and infrastructure.

![PyPI](https://img.shields.io/pypi/v/pihace)
![Python Version](https://img.shields.io/pypi/pyversions/pihace)
![License](https://img.shields.io/pypi/l/pihace)

---

## ✨ Features

- ✅ Built-in system checks: CPU, memory, disk usage, Python version, OS
- 📦 Modular service checks: MySQL, MongoDB, InfluxDB, and more
- 🧩 Custom check functions
- 🧾 Unified health output format
- 🐍 Pythonic API design
- 🔧 Extensible with easy `register()` method

---

## 📦 Installation

```bash
pip install pihace
```

🚀 Quick Start
--------------

```python

import pihace
from pihace.checkers import MySQL, MongoDB, InfluxDB

healthcheck = pihace.HealthCheck(
    with_system=True,
    component_name="something-api",
    component_version="v1.0.0"
)

healthcheck.register("MySQL A", MySQL(dsn="mysql://root:root@127.0.0.1:3306/testdb"))
healthcheck.register("MongoDB B", MongoDB(dsn="mongodb://localhost:27017/test"))
healthcheck.register("InfluxDB C", InfluxDB(url="http://localhost:8086/health"))

print(healthcheck.check())
print(healthcheck.check(output="str"))
print(healthcheck.check(output="json", pretty=True))
```

* * * * *

🧪 Custom Health Check
----------------------

```python
def function_that_mock_failure():
    return (False, "something broke")

def function_that_mock_success():
    return True

healthcheck.register("Mock Fail", function_that_mock_failure)
healthcheck.register("Mock Success", function_that_mock_success)`
```
* * * * *

📤 Example Output
-----------------

```json
{
  "status": "Partially Available",
  "timestamp": "2023-07-01T14:59:55.711Z",
  "failure": {
    "MongoDB B": "authentication failed"
  },
  "rate": "2/3",
  "system": {
    "cpu_usage": "18%",
    "memory_usage": "32%",
    "disk_usage": "47%",
    "memory_available": "512MB",
    "python_version": "3.10",
    "os": "Windows 10"
  },
  "component": {
    "name": "something-api",
    "version": "v1.0.0"
  }
}
```

* * * * *

🔌 Supported Checkers
---------------------

-   ✅ **MySQL**

-   ✅ **MongoDB**

-   ✅ **InfluxDB**

-   🧩 Custom check functions

More integrations are coming soon!

* * * * *

🧰 Development
--------------

Clone this repository:

```bash
git clone https://github.com/yourusername/pihace.git
cd pihace
pip install -e ".[dev]"`
```
Run tests:

``` bash
python -m unittest
```

* * * * *

🐳 Docker Compose Example
-------------------------

Start a testing environment:

```bash
docker-compose up
```

* * * * *

📜 License
----------

This project is licensed under the **Apache License 2.0**.

* * * * *

🤝 Contributing
---------------

Contributions are welcome! Please open an issue or PR to add new checkers, fix bugs, or suggest improvements.

* * * * *

📫 Author
---------

**Ahmad Zein Al Wafi**\
📧 ahmadzeinalwafi@outlook.com\
🔗 [LinkedIn](https://linkedin.com/in/ahmad-zein-al-wafi)\
🌍 [Website](https://ahmadzeinalwafi.my.id)

* * * * *