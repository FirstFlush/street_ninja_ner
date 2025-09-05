from datetime import datetime, timezone


def timestamp(intraday: bool = False) -> str:
    dt = datetime.now(tz=timezone.utc)
    if intraday:
        return dt.strftime("%Y-%m-%d__%H-%M-%S")
    return dt.strftime("%Y-%m-%d")