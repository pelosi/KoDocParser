from datetime import datetime, timedelta
import re

def parse_pdf_date(pdf_date: str) -> str:
    match = re.match(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})([+-]\d{2})'(\d{2})'?", pdf_date)
    if not match:
        return "Invalid date format"

    year, month, day, hour, minute, second, tz_hour, tz_minute = match.groups()
    dt = datetime(
        int(year), int(month), int(day), int(hour), int(minute), int(second)
    )
    tz_offset = timedelta(hours=int(tz_hour), minutes=int(tz_minute))
    local_time = dt + tz_offset

    return local_time.strftime(f"%Y-%m-%d %H:%M:%S (UTC{tz_hour}:{tz_minute})")
