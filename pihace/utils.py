from datetime import datetime

def get_utc_timestamp():
    return datetime.utcnow().isoformat() + "Z"

def calculate_status(total, passed):
    if passed == total:
        return "Available"
    elif passed == 0:
        return "Unavailable"
    else:
        return "Partially Available"

def format_rate(passed, total):
    return f"{passed}/{total}"
