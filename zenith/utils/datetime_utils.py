# Standard Library Imports
from datetime import datetime

# Third Party Imports
from dateutil import tz


# Function To Get Current Local Datetime
def get_current_datetime() -> tuple[str, str]:
    """
    Gets The Current Local Datetime As Separate Date And Time Strings

    Returns:
        tuple[str, str]: A Tuple Containing The Date And Time Strings
    """

    # Get The Current UTC Time
    now_utc: datetime = datetime.now(tz.tzutc())

    # Convert To Local Time
    now_local: datetime = now_utc.astimezone(tz.tzlocal())

    # Format The Date And Time Separately
    date_str: str = now_local.strftime("%Y-%m-%d")
    time_str: str = now_local.strftime("%H:%M:%S")

    # Return The Date And Time Strings
    return date_str, time_str


# Exports
__all__: list[str] = ["get_current_datetime"]
