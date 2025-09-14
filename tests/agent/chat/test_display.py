# Standard Library Imports
from unittest.mock import MagicMock, patch

# Local Imports
from zenith.agent.chat.display import (
    display_agent_prompt,
    display_closing_message,
    display_error_message,
    display_initial_message,
    display_user_prompt,
)


# Test For display_agent_prompt Function
@patch("zenith.agent.chat.display.get_current_datetime")
@patch("zenith.agent.chat.display.Text")
def test_display_agent_prompt(mock_text: MagicMock, mock_get_current_datetime: MagicMock) -> None:
    """
    Tests The display_agent_prompt Function

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
    agent_name = "test_agent"
    display_agent_prompt(
        console=mock_console,
        agent_name=agent_name,
    )

    # Assert get_current_datetime Was Called
    mock_get_current_datetime.assert_called_once()

    # Assert Text Was Created
    mock_text.assert_called_once()

    # Assert Text.append Was Called Multiple Times With Different Styles
    assert mock_text_instance.append.call_count == 7

    # Check Date And Time Styling
    mock_text_instance.append.assert_any_call("[", style="white")
    mock_text_instance.append.assert_any_call(mock_date, style="bold cyan")
    mock_text_instance.append.assert_any_call(" ", style="white")
    mock_text_instance.append.assert_any_call(mock_time, style="bold green")
    mock_text_instance.append.assert_any_call("] ", style="white")

    # Check Agent Name Styling
    mock_text_instance.append.assert_any_call(agent_name, style="bold purple")
    mock_text_instance.append.assert_any_call("\t: ", style="white")

    # Assert console.print Was Called With The Text Instance And end=""
    mock_console.print.assert_called_once_with(mock_text_instance, end="")


# Test For display_initial_message Function
@patch("zenith.agent.chat.display.get_current_datetime")
@patch("zenith.agent.chat.display.Text")
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
    display_initial_message(console=mock_console)

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
    mock_text_instance.append.assert_any_call("To Stop The Program Execution Enter Quit/Exit.", style="bold yellow")

    # Assert console.print Was Called Three Times (Empty Line, Message, Empty Line)
    assert mock_console.print.call_count == 3

    # Assert First Call Was With An Empty String (Line Above)
    mock_console.print.assert_any_call("")

    # Assert Second Call Was With The Text Instance
    mock_console.print.assert_any_call(mock_text_instance)

    # Assert Third Call Was With An Empty String (Line Below)
    mock_console.print.assert_any_call("")


# Test For display_closing_message Function
@patch("zenith.agent.chat.display.get_current_datetime")
@patch("zenith.agent.chat.display.Text")
def test_display_closing_message(mock_text: MagicMock, mock_get_current_datetime: MagicMock) -> None:
    """
    Tests The display_closing_message Function

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
    display_closing_message(console=mock_console)

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

    # Check Message Styling (Call 7)
    mock_text_instance.append.assert_any_call("Thank You For Using Zenith! Have A Great Day!", style="bold yellow")

    # Assert console.print Was Called Three Times (Empty Line, Message, Empty Line)
    assert mock_console.print.call_count == 3

    # Assert First Call Was With An Empty String (Line Above)
    mock_console.print.assert_any_call("")

    # Assert Second Call Was With The Text Instance
    mock_console.print.assert_any_call(mock_text_instance)

    # Assert Third Call Was With An Empty String (Line Below)
    mock_console.print.assert_any_call("")


# Test For display_user_prompt Function
@patch("zenith.agent.chat.display.input", return_value="test input")
@patch("zenith.agent.chat.display.get_current_datetime")
@patch("zenith.agent.chat.display.Text")
def test_display_user_prompt(mock_text: MagicMock, mock_get_current_datetime: MagicMock, mock_input: MagicMock) -> None:
    """
    Tests The display_user_prompt Function

    Args:
        mock_text (MagicMock): The Mock For Text
        mock_get_current_datetime (MagicMock): The Mock For get_current_datetime
        mock_input (MagicMock): The Mock For input
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
    result = display_user_prompt(console=mock_console)

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

    # Check You Label Styling (Calls 5-6)
    mock_text_instance.append.assert_any_call("You", style="bold blue")
    mock_text_instance.append.assert_any_call("\t: ", style="white")

    # Assert console.print Was Called With The Text Instance And end=""
    mock_console.print.assert_called_once_with(mock_text_instance, end="")

    # Assert input Was Called
    mock_input.assert_called_once()

    # Assert The Result Is The Mock Input Return Value
    assert result == "test input"


# Test For display_error_message Function
@patch("zenith.agent.chat.display.get_current_datetime")
@patch("zenith.agent.chat.display.Text")
def test_display_error_message(mock_text: MagicMock, mock_get_current_datetime: MagicMock) -> None:
    """
    Tests The display_error_message Function

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
    error_message = "Test Error Message"
    display_error_message(
        console=mock_console,
        error_message=error_message,
    )

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

    # Check Error Label Styling (Calls 5-6)
    mock_text_instance.append.assert_any_call("Error", style="bold red")
    mock_text_instance.append.assert_any_call("\t: ", style="white")

    # Check Message Styling (Call 7)
    mock_text_instance.append.assert_any_call(error_message, style="bold red")

    # Assert console.print Was Called Three Times (Empty Line, Message, Empty Line)
    assert mock_console.print.call_count == 3

    # Assert First Call Was With An Empty String (Line Above)
    mock_console.print.assert_any_call("")

    # Assert Second Call Was With The Text Instance
    mock_console.print.assert_any_call(mock_text_instance)

    # Assert Third Call Was With An Empty String (Line Below)
    mock_console.print.assert_any_call("")
