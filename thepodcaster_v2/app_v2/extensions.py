from datetime import datetime

def correct_date(datetime_str) -> str:
    if isinstance(datetime_str, datetime):  
        dt = datetime_str  # If already a datetime object, use it directly
    elif isinstance(datetime_str, str):  
        try:
            dt = datetime.fromisoformat(datetime_str)  
        except ValueError:
            return "Invalid Date Format"  
    else:
        return "Invalid Date Type"

    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT') 