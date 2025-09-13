# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Third Party Imports
import pytest
import typer

# Local Imports
from zenith.cli.callbacks import help_callback


# Test For The Help Callback With Value False
def test_help_callback_with_value_false() -> None:
    """
    Tests The Help Callback With Value False
    """

    # Create A Mock Context
    ctx = MagicMock(spec=typer.Context)

    # Call The Help Callback
    help_callback(ctx, value=False)

    # Assert That ctx.exit Was Not Called
    ctx.exit.assert_not_called()


# Test For The Help Callback With Value True
@patch("zenith.cli.callbacks.create_panel")
@patch("zenith.cli.callbacks.Console")
def test_help_callback_with_value_true(
    mock_console_class: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests The Help Callback With Value True

    Args:
        mock_console_class (MagicMock): The Mock Console Class
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # Create A Mock Context
    ctx = MagicMock(spec=typer.Context)
    ctx.get_help.return_value = "Usage: ..."

    # Create A Mock Console Instance
    mock_console_instance = mock_console_class.return_value

    # With pytest.raises
    with pytest.raises(typer.Exit):
        # Call The Help Callback
        help_callback(ctx, value=True)

    # Assert create_panel Was Called
    mock_create_panel.assert_called_once()

    # Assert console.print Was Called With The Panel
    mock_console_instance.print.assert_any_call(mock_create_panel.return_value)

    # Assert ctx.get_help Was Called
    ctx.get_help.assert_called_once()

    # Assert console.print Was Called With The Help Message
    mock_console_instance.print.assert_any_call(ctx.get_help.return_value)
