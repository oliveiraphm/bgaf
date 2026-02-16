from datetime import datetime

def timestamp_to_isostring(date: int) -> str:
    return datetime.fromtimestamp(date).isoformat()

print(timestamp_to_isostring(1736680773))
print(timestamp_to_isostring("12 Jan 2025 11:19:52"))