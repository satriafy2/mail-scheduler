from datetime import datetime
import re

def validate_timestamp(timestamp):
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False

def validate_email(email):
    if not email:
        return False

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if re.fullmatch(regex, email) else False
