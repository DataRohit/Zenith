# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Local Imports
from zenith.utils.datetime_utils import get_current_datetime


# Test For get_current_datetime Function
@patch("zenith.utils.datetime_utils.datetime")
@patch("zenith.utils.datetime_utils.tz")
def test_get_current_datetime(mock_tz: MagicMock, mock_datetime: MagicMock) -> None:
    """
    Tests The get_current_datetime Function

    Args:
        mock_tz (MagicMock): The Mock For tz
        mock_datetime (MagicMock): The Mock For datetime
    """

    # Create Mock UTC Time
    mock_utc_time = MagicMock()
    mock_datetime.now.return_value = mock_utc_time

    # Create Mock Local Time
    mock_local_time = MagicMock()
    mock_utc_time.astimezone.return_value = mock_local_time

    # Set The Formatted Date And Time Strings
    expected_date = "2025-09-13"
    expected_time = "12:34:56"

    # Function To Mock strftime
    def mock_strftime(format_str: str) -> str:
        """
        Function To Mock strftime

        Args:
            format_str (str): The Format String

        Returns:
            str: The Formatted String
        """

        # If The Format String Is %Y-%m-%d
        if format_str == "%Y-%m-%d":
            # Return The Expected Date
            return expected_date

        # If The Format String Is %H:%M:%S
        elif format_str == "%H:%M:%S":
            # Return The Expected Time
            return expected_time

        # Return An Empty String
        return ""

    mock_local_time.strftime.side_effect = mock_strftime

    # Call The Function
    date_result, time_result = get_current_datetime()

    # Assert The Results Are The Expected Date And Time Strings
    assert date_result == expected_date
    assert time_result == expected_time

    # Assert datetime.now Was Called With tz.tzutc()
    mock_datetime.now.assert_called_once_with(mock_tz.tzutc.return_value)

    # Assert astimezone Was Called With tz.tzlocal()
    mock_utc_time.astimezone.assert_called_once_with(mock_tz.tzlocal.return_value)

    # Assert strftime Was Called With The Correct Formats
    assert mock_local_time.strftime.call_count == 2
    mock_local_time.strftime.assert_any_call("%Y-%m-%d")
    mock_local_time.strftime.assert_any_call("%H:%M:%S")
