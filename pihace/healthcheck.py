# -*- coding: utf-8 -*-
"""pihace.health: Core health check manager class."""

import json
from typing import Callable, Dict, Union
from time import time
import asyncio
import inspect

from .utils import get_utc_timestamp, calculate_status, format_rate
from .system_info import get_system_info

class HealthCheck:
    """
    HealthCheck manages registration and execution of system/service health checks.

    Attributes:
        with_system (bool): Whether to include system information in the result.
        component_name (str): Name of the component (e.g., service or API).
        component_version (str): Version of the component.
        checkers (dict): A mapping of checker names to their config and callable.
    """

    def __init__(self, with_system: bool = False, name: str = None, version: str = None):
        """
        Initialize a HealthCheck instance.

        Args:
            with_system (bool): Include system info in result if True.
            name (str): Name of the application/component.
            version (str): Version of the application/component.
        """
        self.with_system = with_system
        self.component_name = name
        self.component_version = version
        self.checkers: Dict[str, Callable[[], Union[bool, tuple]]] = {}

    def register(self, name: str, checker: Callable, timeout: int = 5, retries: int = 2) -> None:
        """
        Register a health check function.

        Args:
            name (str): A unique name for the checker.
            checker (Callable): A function or async function returning True or (False, message).
            timeout (int): Timeout in seconds for the checker.
            retries (int): Number of retry attempts on failure.

        Raises:
            ValueError: If the checker is not callable.
        """
        if not callable(checker):
            raise ValueError("Checker must be a callable function")
        self.checkers[name] = {
            'checker': checker,
            'timeout': timeout,
            'retries': retries
        }

    def _run_checker(self, checker, result_queue) -> None:
        """
        Run a health check and put the result in the queue.
        """
        try:
            result = checker()
            result_queue.put(result)
        except Exception as e:
            result_queue.put((False, str(e)))

    def check(self, output: str = "dict", pretty: bool = True) -> Union[dict, str]:
        """
        Execute all registered health checks and return the result.

        Args:
            output (str): Output format: "dict", "json", or "str".
            pretty (bool): Pretty-print JSON output if True.

        Returns:
            Union[dict, str]: Health check report in the requested format.
        """
        return asyncio.run(self._check_async(output, pretty))
    
    async def run_checker_with_retries(name, checker, retries, timeout):
        """
        Attempt to run a checker with retries and timeout.

        Returns:
            Union[bool, tuple]: True if healthy, or (False, reason) if failed.
        """
        for attempt in range(retries):
            try:
                if inspect.iscoroutinefunction(checker):
                    # Native async checker
                    result = await asyncio.wait_for(checker(), timeout=timeout)
                else:
                    # Synchronous checker wrapped in async thread
                    result = await asyncio.wait_for(asyncio.to_thread(checker), timeout=timeout)
                return result
            except asyncio.TimeoutError:
                if attempt == retries - 1:
                    return (False, "pihace: async timeout")
            except Exception as e:
                return (False, str(e))
        return (False, "pihace: unknown error after retries")

    async def _check_async(self, output: str = "dict", pretty: bool = True) -> Union[dict, str]:
        """
        Asynchronous internal implementation of the health check logic.

        Args:
            output (str): Output format: "dict", "json", or "str".
            pretty (bool): Pretty-print JSON output if True.

        Returns:
            Union[dict, str]: Health check report in the requested format.
        """
        start_time = time()
        failures = {}
        success_count = 0
        total_count = len(self.checkers)

        tasks = [
            self.run_checker_with_retries(name, data['checker'], data['retries'], data['timeout'])
            for name, data in self.checkers.items()
        ]

        names = list(self.checkers.keys())
        results = await asyncio.gather(*tasks)

        for name, result in zip(names, results):
            if result is True:
                success_count += 1
            elif isinstance(result, tuple) and not result[0]:
                failures[name] = result[1]
            else:
                failures[name] = "pihace: log are unavailable"

        status = calculate_status(success_count, total_count)
        end_time = time() - start_time
        response = {
            "status": status,
            "timestamp": get_utc_timestamp(),
            "failure": failures if failures else None,
            "rate": format_rate(success_count, total_count),
            "duration": end_time,
            "system": get_system_info() if self.with_system else None,
            "component": {
                "name": self.component_name,
                "version": self.component_version
            } if self.component_name and self.component_version else None
        }

        if output == "json":
            return json.dumps(response, indent=4 if pretty else None)
        elif output == "str":
            lines = [
                f"Status: {response['status']} ({response['rate']} healthy)",
                f"Timestamp: {response['timestamp']}"
            ]
            if failures:
                lines.append("Failures:")
                for k, v in failures.items():
                    lines.append(f" - {k}: {v}")
            if response.get("component"):
                lines.append(f"Component: {response['component']['name']} {response['component']['version']}")
            if self.with_system:
                sysinfo = response.get("system", {})
                lines.append("System: " + ", ".join([
                    f"CPU {sysinfo.get('cpu_usage')}",
                    f"Mem {sysinfo.get('memory_usage')}",
                    f"Disk {sysinfo.get('disk_usage')}",
                    f"Free Mem: {sysinfo.get('memory_available')}",
                    f"Python {sysinfo.get('python_version')}",
                    f"OS: {sysinfo.get('os')}"
                ]))
            return "\n".join(lines)

        return response
