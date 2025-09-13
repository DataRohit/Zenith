# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Local Imports
from zenith.agent.chat import display_initial_message
from zenith.agent.chat import start_chat


# Test For display_initial_message Function
@patch("zenith.agent.chat.get_current_datetime")
@patch("zenith.agent.chat.Text")
def test_display_initial_message(mock_text: MagicMock, mock_get_current_datetime: MagicMock) -> None:
    """
    Tests The display_initial_message Function

    Args:
        mock_text (MagicMock): The Mock For Text
        mock_get_current_datetime (MagicMock): The Mock For get_current_datetime
    """

    # Create A Mock Console
    mock_console = MagicMock()

    # Set The Return Value For get_current_datetime
    mock_date = "2025-09-13"
    mock_time = "12:34:56"
    mock_get_current_datetime.return_value = (mock_date, mock_time)

    # Create A Mock Text Instance
    mock_text_instance = MagicMock()
    mock_text.return_value = mock_text_instance

    # Call The Function
    display_initial_message(mock_console)

    # Assert get_current_datetime Was Called
    mock_get_current_datetime.assert_called_once()

    # Assert Text Was Created
    mock_text.assert_called_once()

    # Assert Text.append Was Called Multiple Times With Different Styles
    assert mock_text_instance.append.call_count == 8

    # Check Date Styling (Calls 0-2)
    mock_text_instance.append.assert_any_call("[", style="white")
    mock_text_instance.append.assert_any_call(mock_date, style="bold cyan")
    mock_text_instance.append.assert_any_call(" ", style="white")

    # Check Time Styling (Calls 3-4)
    mock_text_instance.append.assert_any_call(mock_time, style="bold green")
    mock_text_instance.append.assert_any_call("] ", style="white")

    # Check System Label Styling (Calls 5-6)
    mock_text_instance.append.assert_any_call("System", style="bold magenta")
    mock_text_instance.append.assert_any_call("\t: ", style="white")

    # Check Message Styling (Call 7, which is actually the 8th call)
    mock_text_instance.append.assert_any_call("To Stop The Program Execution Enter quit/exit", style="bold yellow")

    # Assert console.print Was Called Three Times (Empty Line, Message, Empty Line)
    assert mock_console.print.call_count == 3

    # Assert First Call Was With An Empty String (Line Above)
    mock_console.print.assert_any_call("")

    # Assert Second Call Was With The Text Instance
    mock_console.print.assert_any_call(mock_text_instance)

    # Assert Third Call Was With An Empty String (Line Below)
    mock_console.print.assert_any_call("")


# Test For start_chat Function
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
def test_start_chat(mock_display_initial_message: MagicMock, mock_console: MagicMock) -> None:
    """
    Tests The start_chat Function

    Args:
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Call The Function
    start_chat(mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called With The Console Instance
    mock_display_initial_message.assert_called_once_with(mock_console_instance)
