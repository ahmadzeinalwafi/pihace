import psutil
import platform
import sys

def get_system_info():
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
