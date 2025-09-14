# Standard Library Imports
from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

# Third Party Imports
import pytest
from rich.markdown import Markdown

# Local Imports
from zenith.agent.chat.process import process_agent_response


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


# Test For process_agent_response Function
@pytest.mark.asyncio
@patch("zenith.agent.chat.process.Live")
@patch("zenith.agent.chat.process.display_agent_prompt")
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
@patch("zenith.agent.chat.process.Live")
@patch("zenith.agent.chat.process.display_agent_prompt")
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
