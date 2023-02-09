from datetime import datetime


def valid_timestamp(timestamp):
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False
