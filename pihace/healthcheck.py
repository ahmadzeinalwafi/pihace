from .utils import get_utc_timestamp, calculate_status, format_rate
from .system_info import get_system_info
from .base_checker import BaseChecker

class HealthCheck:
    def __init__(self, name="unnamed", version="v0.0.1", with_system=True):
        self.name = name
        self.version = version
        self.with_system = with_system
        self.services = {}

    def register(self, name, checker):
        self.services[name] = checker

    def check(self):
        failures = {}
        total = len(self.services)
        passed = 0

        for name, checker in self.services.items():
            try:
                result = checker() if callable(checker) else checker.check()

                if result is True:
                    passed += 1
                elif isinstance(result, tuple) and not result[0]:
                    failures[name] = result[1]
                else:
                    failures[name] = "pihace: log are unavailable"
            except Exception as e:
                failures[name] = str(e)

        status = calculate_status(total, passed)
        timestamp = get_utc_timestamp()

        result = {
            "status": status,
            "timestamp": timestamp,
            "failure": failures,
            "rate": format_rate(passed, total),
            "component": {
                "name": self.name,
                "version": self.version
            }
        }

        if self.with_system:
            result["system"] = get_system_info()

        return result
