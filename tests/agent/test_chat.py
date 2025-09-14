# Standard Library Imports
from collections.abc import AsyncGenerator
from unittest.mock import ANY, MagicMock
from unittest.mock import patch

# Third Party Imports
from openai import APITimeoutError, BadRequestError, NotFoundError
import httpx
import pytest
from rich.markdown import Markdown

# Local Imports
from zenith.agent.chat import display_agent_prompt
from zenith.agent.chat import display_closing_message
from zenith.agent.chat import display_error_message
from zenith.agent.chat import display_initial_message
from zenith.agent.chat import display_user_prompt
from zenith.agent.chat import process_agent_response
from zenith.agent.chat import start_chat


# Helper Async Generator
async def mock_async_generator(items: list[MagicMock]) -> AsyncGenerator[MagicMock, None]:
    """
    Mock Async Generator

    Args:
        items (list[MagicMock]): The Items To Yield
    """

    # For Each Item In The Items
    for item in items:
        # Yield The Item
        yield item


# Test For display_agent_prompt Function
@patch("zenith.agent.chat.get_current_datetime")
@patch("zenith.agent.chat.Text")
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
@patch("zenith.agent.chat.get_current_datetime")
@patch("zenith.agent.chat.Text")
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
@patch("zenith.agent.chat.input", return_value="test input")
@patch("zenith.agent.chat.get_current_datetime")
@patch("zenith.agent.chat.Text")
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


# Test For process_agent_response Function
@pytest.mark.asyncio
@patch("zenith.agent.chat.Live")
@patch("zenith.agent.chat.display_agent_prompt")
async def test_process_agent_response(mock_display_agent_prompt: MagicMock, mock_live: MagicMock) -> None:
    """
    Tests The process_agent_response Function

    Args:
        mock_display_agent_prompt (MagicMock): The Mock For display_agent_prompt
        mock_live (MagicMock): The Mock For Live
    """

    # Create Mocks
    mock_console = MagicMock()
    mock_spinner = MagicMock()
    mock_console.status.return_value = mock_spinner
    mock_agent = MagicMock()
    mock_agent.name = "test_agent"
    user_input = "test input"

    # Mock Live instance
    mock_live_instance = MagicMock()
    mock_live.return_value = mock_live_instance

    # Define Mock Messages
    streaming_chunk = MagicMock(type="ModelClientStreamingChunkEvent", content="Streaming content")
    mock_messages = [streaming_chunk]

    # Patch The Agent's run_stream Method
    mock_agent.run_stream = MagicMock(return_value=mock_async_generator(mock_messages))

    # Call The Function
    await process_agent_response(
        console=mock_console,
        agent=mock_agent,
        user_input=user_input,
    )

    # Assertions For Spinner
    mock_console.status.assert_called_once_with(status=f"{mock_agent.name} Is Thinking...", spinner="dots")
    mock_spinner.start.assert_called_once()
    mock_spinner.stop.assert_called_once()

    # Assertions For Agent Response
    mock_display_agent_prompt.assert_called_once_with(
        console=mock_console,
        agent_name=mock_agent.name,
    )
    mock_agent.run_stream.assert_called_once_with(task=user_input)

    # Check Live display was created and used properly
    mock_live.assert_called_once_with("", console=mock_console, auto_refresh=True, refresh_per_second=10)
    mock_live_instance.start.assert_called_once()

    # Verify that update was called with a Markdown instance
    mock_live_instance.update.assert_called()
    update_call_args = mock_live_instance.update.call_args[0][0]
    assert isinstance(update_call_args, Markdown)

    mock_live_instance.stop.assert_called_once()

    # Check For Newline Call At The End
    mock_console.print.assert_called_with()
    assert mock_console.print.call_count == 1


# Test For process_agent_response Function With No Chunks
@pytest.mark.asyncio
@patch("zenith.agent.chat.Live")
@patch("zenith.agent.chat.display_agent_prompt")
async def test_process_agent_response_no_chunks(mock_display_agent_prompt: MagicMock, mock_live: MagicMock) -> None:
    """
    Tests The process_agent_response Function When No Chunks Are Received

    Args:
        mock_display_agent_prompt (MagicMock): The Mock For display_agent_prompt
        mock_live (MagicMock): The Mock For Live
    """

    # Create Mocks
    mock_console = MagicMock()
    mock_spinner = MagicMock()
    mock_console.status.return_value = mock_spinner
    mock_agent = MagicMock()
    mock_agent.name = "test_agent"
    user_input = "test input"

    # Define Mock Messages (Empty)
    mock_messages = []

    # Patch The Agent's run_stream Method
    mock_agent.run_stream = MagicMock(return_value=mock_async_generator(mock_messages))

    # Call The Function
    await process_agent_response(
        console=mock_console,
        agent=mock_agent,
        user_input=user_input,
    )

    # Assertions For Spinner
    mock_console.status.assert_called_once_with(status=f"{mock_agent.name} Is Thinking...", spinner="dots")
    mock_spinner.start.assert_called_once()
    mock_spinner.stop.assert_called_once()

    # Assertions For Agent Response
    mock_display_agent_prompt.assert_not_called()
    mock_agent.run_stream.assert_called_once_with(task=user_input)

    # Verify Live was not used
    mock_live.assert_not_called()

    # Assertions For Console Output
    mock_console.print.assert_called_once_with()


# Test For start_chat Function With Normal Input
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_closing_message")
def test_start_chat_normal_input(
    mock_display_closing_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With Normal Input

    Args:
        mock_display_closing_message (MagicMock): The Mock For display_closing_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set Up The Side Effect For display_user_prompt To Return Normal Input Then Exit
    mock_display_user_prompt.side_effect = ["test input", "exit"]

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Call The Function
    start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called With The Console Instance
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called Twice With The Console Instance
    assert mock_display_user_prompt.call_count == 2
    mock_display_user_prompt.assert_called_with(console=mock_console_instance)

    # Assert That A Newline Was Printed For Spacing
    mock_console_instance.print.assert_any_call("")

    # Assert display_closing_message Was Called With The Console Instance
    mock_display_closing_message.assert_called_once_with(console=mock_console_instance)


# Test For start_chat Function With Immediate Exit
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_closing_message")
def test_start_chat_immediate_exit(
    mock_display_closing_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With Immediate Exit

    Args:
        mock_display_closing_message (MagicMock): The Mock For display_closing_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set The Return Value For display_user_prompt To Exit Immediately
    mock_display_user_prompt.return_value = "quit"

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Call The Function
    start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called With The Console Instance
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called Once With The Console Instance
    mock_display_user_prompt.assert_called_once_with(console=mock_console_instance)

    # Assert display_closing_message Was Called With The Console Instance
    mock_display_closing_message.assert_called_once_with(console=mock_console_instance)


# Test For display_error_message Function
@patch("zenith.agent.chat.get_current_datetime")
@patch("zenith.agent.chat.Text")
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


# Test For start_chat Function With BadRequestError
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_error_message")
def test_start_chat_bad_request_error(
    mock_display_error_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With BadRequestError

    Args:
        mock_display_error_message (MagicMock): The Mock For display_error_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set Up The Side Effect For display_user_prompt To Return Normal Input
    mock_display_user_prompt.return_value = "test input"

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Set Up The Side Effect For asyncio.run To Raise BadRequestError
    with patch("zenith.agent.chat.asyncio.run") as mock_asyncio_run:
        # Set Up The Side Effect For asyncio.run To Raise BadRequestError
        mock_asyncio_run.side_effect = BadRequestError(
            message="Invalid API Key! Please Pass A Valid API Key!",
            response=MagicMock(),
            body=MagicMock(),
        )

        # Call The Function
        start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called
    mock_display_user_prompt.assert_called_once_with(console=mock_console_instance)

    # Assert console.print Was Called For Newline In Exception Handler
    mock_console_instance.print.assert_called_with("")

    # Assert display_error_message Was Called With The Correct Error Message
    mock_display_error_message.assert_called_once_with(
        console=mock_console_instance,
        error_message="Invalid API Key! Please Pass A Valid API Key!",
    )


# Test For start_chat Function With APITimeoutError
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_error_message")
def test_start_chat_api_timeout_error(
    mock_display_error_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With APITimeoutError

    Args:
        mock_display_error_message (MagicMock): The Mock For display_error_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set Up The Side Effect For display_user_prompt To Return Normal Input
    mock_display_user_prompt.return_value = "test input"

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Set Up The Side Effect For asyncio.run To Raise APITimeoutError
    with patch("zenith.agent.chat.asyncio.run") as mock_asyncio_run:
        # Set Up The Side Effect For asyncio.run To Raise APITimeoutError
        mock_request = MagicMock(spec=httpx.Request)
        mock_asyncio_run.side_effect = APITimeoutError(request=mock_request)

        # Call The Function
        start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called
    mock_display_user_prompt.assert_called_once_with(console=mock_console_instance)

    # Assert console.print Was Called For Newline In Exception Handler
    mock_console_instance.print.assert_called_with("")

    # Assert display_error_message Was Called With The Correct Error Message
    mock_display_error_message.assert_called_once_with(
        console=mock_console_instance,
        error_message="API Timeout! Please Check API Base URL And API Key!",
    )


# Test For start_chat Function With NotFoundError
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_error_message")
def test_start_chat_not_found_error(
    mock_display_error_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With NotFoundError

    Args:
        mock_display_error_message (MagicMock): The Mock For display_error_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set Up The Side Effect For display_user_prompt To Return Normal Input
    mock_display_user_prompt.return_value = "test input"

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Set Up The Side Effect For asyncio.run To Raise NotFoundError
    with patch("zenith.agent.chat.asyncio.run") as mock_asyncio_run:
        # Set Up The Side Effect For asyncio.run To Raise NotFoundError
        mock_asyncio_run.side_effect = NotFoundError(
            message="Invalid Model! Please Check Model Name!",
            response=MagicMock(),
            body=MagicMock(),
        )

        # Call The Function
        start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called
    mock_display_user_prompt.assert_called_once_with(console=mock_console_instance)

    # Assert console.print Was Called For Newline In Exception Handler
    mock_console_instance.print.assert_called_with("")

    # Assert display_error_message Was Called With The Correct Error Message
    mock_display_error_message.assert_called_once_with(
        console=mock_console_instance,
        error_message="Invalid Model! Please Check Model Name!",
    )


# Test For start_chat Function With KeyboardInterrupt
@patch("zenith.agent.chat.display_user_prompt")
@patch("zenith.agent.chat.Console")
@patch("zenith.agent.chat.display_initial_message")
@patch("zenith.agent.chat.display_closing_message")
def test_start_chat_keyboard_interrupt(
    mock_display_closing_message: MagicMock,
    mock_display_initial_message: MagicMock,
    mock_console: MagicMock,
    mock_display_user_prompt: MagicMock,
) -> None:
    """
    Tests The start_chat Function With KeyboardInterrupt

    Args:
        mock_display_closing_message (MagicMock): The Mock For display_closing_message
        mock_display_initial_message (MagicMock): The Mock For display_initial_message
        mock_console (MagicMock): The Mock For Console
        mock_display_user_prompt (MagicMock): The Mock For display_user_prompt
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Set Up The Side Effect For display_user_prompt To Raise KeyboardInterrupt
    mock_display_user_prompt.side_effect = KeyboardInterrupt

    # Create A Mock Agent
    mock_agent = MagicMock()

    # Call The Function
    start_chat(agent=mock_agent)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert display_initial_message Was Called
    mock_display_initial_message.assert_called_once_with(console=mock_console_instance)

    # Assert display_user_prompt Was Called
    mock_display_user_prompt.assert_called_once_with(console=mock_console_instance)

    # Assert console.print Was Called For Newline In Exception Handler
    mock_console_instance.print.assert_called_with("")

    # Assert display_closing_message Was Called
    mock_display_closing_message.assert_called_once_with(console=mock_console_instance)
