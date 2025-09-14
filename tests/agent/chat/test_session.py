# Standard Library Imports
from unittest.mock import MagicMock, patch

# Third Party Imports
from openai import APITimeoutError, BadRequestError, NotFoundError
import httpx

# Local Imports
from zenith.agent.chat.session import start_chat


# Test For start_chat Function With Normal Input
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_closing_message")
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
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_closing_message")
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


# Test For start_chat Function With BadRequestError
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_error_message")
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
    with patch("zenith.agent.chat.session.asyncio.run") as mock_asyncio_run:
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
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_error_message")
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
    with patch("zenith.agent.chat.session.asyncio.run") as mock_asyncio_run:
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
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_error_message")
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
    with patch("zenith.agent.chat.session.asyncio.run") as mock_asyncio_run:
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
@patch("zenith.agent.chat.session.display_user_prompt")
@patch("zenith.agent.chat.session.Console")
@patch("zenith.agent.chat.session.display_initial_message")
@patch("zenith.agent.chat.session.display_closing_message")
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
