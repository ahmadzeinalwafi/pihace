# -*- coding: utf-8 -*-
"""pihace.system_info: Module to gather system-level information."""

import psutil
import platform
import sys
from typing import Dict, Union

def get_system_info() -> Dict[str, Union[str, float]]:
    """
    Retrieve system resource usage and platform information.

    Returns:
        dict: A dictionary containing:
            - cpu_usage (str): CPU usage percentage (e.g., "15.3%").
            - memory_usage (str): Memory usage percentage.
            - memory_available (str): Available memory in MB.
            - disk_usage (str): Disk usage percentage.
            - disk_available (str): Available disk space in GB.
            - os (str): Operating system name (e.g., "Linux", "Windows").
            - os_version (str): Operating system version string.
            - python_version (str): Python major.minor version.
        If gathering information fails, returns a dict with a fallback message.
    """
    try:
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
            "memory_usage": f"{mem.percent}%",
            "memory_available": f"{round(mem.available / (1024 ** 2), 2)} MB",
            "disk_usage": f"{disk.percent}%",
            "disk_available": f"{round(disk.free / (1024 ** 3), 2)} GB",
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        }
    except Exception:
        return {"system_info": "pihace: log are unavailable"}
