# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Third Party Imports
import pytest
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Local Imports
from zenith.cli.config_display import display_config
from zenith.cli.config_display import mask_api_key


# Test For mask_api_key With Empty API Key
def test_mask_api_key_empty() -> None:
    """
    Tests The mask_api_key Function With An Empty API Key
    """

    # Call The Function
    result = mask_api_key("")

    # Assert The Result Is Correct
    assert result == ""


# Test For mask_api_key With Short API Key (Less Than 4 Characters)
def test_mask_api_key_short() -> None:
    """
    Tests The mask_api_key Function With A Short API Key (Less Than 4 Characters)
    """

    # Call The Function
    result = mask_api_key("123")

    # Assert The Result Is Correct
    assert result == "****"


# Test For mask_api_key With Short API Key (4 Characters)
def test_mask_api_key_4_chars() -> None:
    """
    Tests The mask_api_key Function With A Short API Key (4 Characters)
    """

    # Call The Function
    result = mask_api_key("1234")

    # Assert The Result Is Correct
    assert result == "****1234"


# Test For mask_api_key With Short API Key (5-8 Characters)
def test_mask_api_key_5_to_8_chars() -> None:
    """
    Tests The mask_api_key Function With A Short API Key (5-8 Characters)
    """

    # Call The Function
    result = mask_api_key("12345678")

    # Assert The Result Is Correct
    assert result == "****5678"


# Test For mask_api_key With Long API Key (More Than 8 Characters)
def test_mask_api_key_long() -> None:
    """
    Tests The mask_api_key Function With A Long API Key (More Than 8 Characters)
    """

    # Call The Function
    result = mask_api_key("1234567890abcdef")

    # Assert The Result Is Correct
    assert result == "1234********cdef"


# Test For display_config Function
@patch("zenith.cli.config_display.Table")
@patch("zenith.cli.config_display.Panel")
@patch("zenith.cli.config_display.Text")
@patch("zenith.cli.config_display.mask_api_key")
def test_display_config(
    mock_mask_api_key: MagicMock,
    mock_text: MagicMock,
    mock_panel: MagicMock,
    mock_table: MagicMock,
) -> None:
    """
    Tests The display_config Function

    Args:
        mock_mask_api_key (MagicMock): The Mock For mask_api_key
        mock_text (MagicMock): The Mock For Text
        mock_panel (MagicMock): The Mock For Panel
        mock_table (MagicMock): The Mock For Table
    """

    # Set Up The Mocks
    mock_mask_api_key.return_value = "1234********cdef"
    mock_table_instance = mock_table.grid.return_value
    mock_text_instances = [MagicMock() for _ in range(6)]
    mock_text.side_effect = mock_text_instances

    # Create A Mock Console
    mock_console = MagicMock(spec=Console)

    # Create A Sample Configuration
    config = {
        "zenith_openai_api_key": "1234567890abcdef",
        "zenith_openai_api_base": "https://api.openai.com/v1",
        "zenith_model": "gpt-4",
    }

    # Call The Function
    display_config(mock_console, config)

    # Assert mask_api_key Was Called With The Correct Arguments
    mock_mask_api_key.assert_called_once_with("1234567890abcdef")

    # Assert Table.grid Was Called
    mock_table.grid.assert_called_once_with(expand=True)

    # Assert add_column Was Called With The Correct Arguments
    mock_table_instance.add_column.assert_called_once_with(justify="center")

    # Assert add_row Was Called With The Correct Arguments
    assert mock_table_instance.add_row.call_count == 3

    # Assert Panel Was Called With The Correct Arguments
    mock_panel.assert_called_once()

    # Assert console.print Was Called With The Panel
    mock_console.print.assert_called_once_with(mock_panel.return_value)


# Test For display_config Function With Empty Configuration
@patch("zenith.cli.config_display.Table")
@patch("zenith.cli.config_display.Panel")
@patch("zenith.cli.config_display.Text")
@patch("zenith.cli.config_display.mask_api_key")
def test_display_config_empty(
    mock_mask_api_key: MagicMock,
    mock_text: MagicMock,
    mock_panel: MagicMock,
    mock_table: MagicMock,
) -> None:
    """
    Tests The display_config Function With Empty Configuration

    Args:
        mock_mask_api_key (MagicMock): The Mock For mask_api_key
        mock_text (MagicMock): The Mock For Text
        mock_panel (MagicMock): The Mock For Panel
        mock_table (MagicMock): The Mock For Table
    """

    # Set Up The Mocks
    mock_mask_api_key.return_value = ""
    mock_table_instance = mock_table.grid.return_value
    mock_text_instances = [MagicMock() for _ in range(6)]
    mock_text.side_effect = mock_text_instances

    # Create A Mock Console
    mock_console = MagicMock(spec=Console)

    # Create An Empty Configuration
    config = {}

    # Call The Function
    display_config(mock_console, config)

    # Assert mask_api_key Was Called With The Correct Arguments
    mock_mask_api_key.assert_called_once_with("")

    # Assert Table.grid Was Called
    mock_table.grid.assert_called_once_with(expand=True)

    # Assert add_column Was Called With The Correct Arguments
    mock_table_instance.add_column.assert_called_once_with(justify="center")

    # Assert add_row Was Called With The Correct Arguments
    assert mock_table_instance.add_row.call_count == 3

    # Assert Panel Was Called With The Correct Arguments
    mock_panel.assert_called_once()

    # Assert console.print Was Called With The Panel
    mock_console.print.assert_called_once_with(mock_panel.return_value)
