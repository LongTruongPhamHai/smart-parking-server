from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Bangkok")


def now_gmt7() -> datetime:
    """Trả về datetime hiện tại theo GMT+7 (timezone aware)"""
    return datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)


def timedelta_to_hms(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
