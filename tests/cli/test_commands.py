# Standard Library Imports
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

# Third Party Imports
import pytest
import typer
from typer.testing import CliRunner

# Local Imports
from zenith.cli.app import app
from zenith.cli.commands import chat
from zenith.utils.errors import show_error_and_exit

# Create A Runner
runner = CliRunner()


# Test For The Show Error And Exit Function
@patch("zenith.utils.errors.Panel")
def test_show_error_and_exit(mock_panel: MagicMock) -> None:
    """
    Tests The Show Error And Exit Function

    Args:
        mock_panel (MagicMock): The Mock Panel
    """

    # Create A Mock Console
    mock_console = MagicMock()

    # With pytest.raises
    with pytest.raises(typer.Exit) as exc_info:
        # Call The Function
        show_error_and_exit(mock_console, "Test Error")

    # Assert The Exit Code
    assert exc_info.value.exit_code == 1

    # Assert The Panel Was Created With The Correct Arguments
    mock_panel.assert_called_once()

    # Assert The Console Print Was Called
    mock_console.print.assert_called_once_with(mock_panel.return_value)


# Test For Main Command With No Config
@patch("zenith.cli.commands.Path.cwd")
def test_main_no_config(mock_cwd: MagicMock) -> None:
    """
    Tests The Main Command With No Config

    Args:
        mock_cwd (MagicMock): The Mock For Path.cwd
    """

    # Set Up The Mock To Return A Path That Doesn't Have .zenith Directory
    mock_cwd.return_value = Path("/non_existent_path")

    # Invoke The App
    result = runner.invoke(app, [])

    # Assert The Exit Code
    assert result.exit_code == 1

    # Assert The Output Contains The Error Message
    assert "Configuration File Not Found!" in result.stdout


# Test For Main Command With Provided Config File
@patch("zenith.cli.commands.create_panel")
@patch("zenith.cli.commands.load_config")
@patch("zenith.cli.commands.display_config")
def test_main_with_provided_config(
    mock_display_config: MagicMock,
    mock_load_config: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests The Main Command With A Provided Config File

    Args:
        mock_display_config (MagicMock): The Mock For display_config
        mock_load_config (MagicMock): The Mock For load_config
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_load_config.return_value = {"zenith_openai_api_key": "test_key"}

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A Config File
        config_path = Path(temp_dir) / "config.json"
        config_path.touch()

        # Invoke The App
        result = runner.invoke(app, ["--config", str(config_path)])

        # Assert The Exit Code
        assert result.exit_code == 0

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()

        # Assert load_config Was Called With The Config Path
        mock_load_config.assert_called_once()

        # Assert display_config Was Called
        mock_display_config.assert_called_once()


# Test For Main Command With .zenith/config.json
@patch("zenith.cli.commands.create_panel")
@patch("zenith.cli.commands.load_config")
@patch("zenith.cli.commands.display_config")
@patch("zenith.cli.commands.Path.cwd")
def test_main_with_zenith_config_json(
    mock_cwd: MagicMock,
    mock_display_config: MagicMock,
    mock_load_config: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests The Main Command With .zenith/config.json

    Args:
        mock_cwd (MagicMock): The Mock For Path.cwd
        mock_display_config (MagicMock): The Mock For display_config
        mock_load_config (MagicMock): The Mock For load_config
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_load_config.return_value = {"zenith_openai_api_key": "test_key"}

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A .zenith Directory
        zenith_dir = Path(temp_dir) / ".zenith"
        zenith_dir.mkdir()

        # Create A Config File
        config_file = zenith_dir / "config.json"
        config_file.touch()

        # Set Up The Mock To Return The Temp Directory
        mock_cwd.return_value = Path(temp_dir)

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 0

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()

        # Assert load_config Was Called With The Config Path
        mock_load_config.assert_called_once_with(config_file)

        # Assert display_config Was Called
        mock_display_config.assert_called_once()


# Test For Main Command With .zenith/.config.env
@patch("zenith.cli.commands.create_panel")
@patch("zenith.cli.commands.load_config")
@patch("zenith.cli.commands.display_config")
@patch("zenith.cli.commands.Path.cwd")
def test_main_with_zenith_config_env(
    mock_cwd: MagicMock,
    mock_display_config: MagicMock,
    mock_load_config: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests The Main Command With .zenith/.config.env

    Args:
        mock_cwd (MagicMock): The Mock For Path.cwd
        mock_display_config (MagicMock): The Mock For display_config
        mock_load_config (MagicMock): The Mock For load_config
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_load_config.return_value = {"zenith_openai_api_key": "test_key"}

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A .zenith Directory
        zenith_dir = Path(temp_dir) / ".zenith"
        zenith_dir.mkdir()

        # Create A Config File
        config_file = zenith_dir / ".config.env"
        config_file.touch()

        # Set Up The Mock To Return The Temp Directory
        mock_cwd.return_value = Path(temp_dir)

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 0

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()

        # Assert load_config Was Called With The Config Path
        mock_load_config.assert_called_once_with(config_file)

        # Assert display_config Was Called
        mock_display_config.assert_called_once()


# Test For Main Command With Both .zenith Configs
@patch("zenith.cli.commands.create_panel")
@patch("zenith.cli.commands.Path.cwd")
def test_main_with_both_zenith_configs(
    mock_cwd: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests An Error Is Raised When Both .zenith Config Files Exist

    Args:
        mock_cwd (MagicMock): The Mock For Path.cwd
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A .zenith Directory
        zenith_dir = Path(temp_dir) / ".zenith"
        zenith_dir.mkdir()

        # Create Config Files
        (zenith_dir / "config.json").touch()
        (zenith_dir / ".config.env").touch()

        # Set Up The Mock To Return The Temp Directory
        mock_cwd.return_value = Path(temp_dir)

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 1

        # Assert The Error Message Is In The Output
        assert "Both 'config.json' and '.config.env' found" in result.stdout

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()


# Test For Main Command With Config Loading Exception
@patch("zenith.cli.commands.create_panel")
@patch("zenith.cli.commands.load_config")
def test_main_with_config_loading_exception(
    mock_load_config: MagicMock,
    mock_create_panel: MagicMock,
) -> None:
    """
    Tests The Main Command When A Config Loading Exception Occurs

    Args:
        mock_load_config (MagicMock): The Mock For load_config
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # Set Up The Mock To Raise An Exception
    mock_load_config.side_effect = ValueError("Invalid JSON format")

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A Config File
        config_path = Path(temp_dir) / "config.json"
        config_path.touch()

        # Invoke The App
        result = runner.invoke(app, ["--config", str(config_path)])

        # Assert The Exit Code
        assert result.exit_code == 1

        # Assert The Error Message Is In The Output
        assert "Error Loading Configuration File: Invalid JSON format" in result.stdout

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()

        # Assert load_config Was Called With The Config Path
        mock_load_config.assert_called_once_with(config_path)


# Test For The Chat Command
@patch("zenith.cli.commands.create_assistant_agent")
@patch("zenith.cli.commands.Console")
@patch("zenith.cli.commands.Table")
@patch("zenith.cli.commands.Panel")
def test_chat_command(
    mock_panel: MagicMock,
    mock_table: MagicMock,
    mock_console: MagicMock,
    mock_create_assistant_agent: MagicMock,
) -> None:
    """
    Tests The Chat Command

    Args:
        mock_panel (MagicMock): The Mock For Panel
        mock_table (MagicMock): The Mock For Table
        mock_console (MagicMock): The Mock For Console
        mock_create_assistant_agent (MagicMock): The Mock For create_assistant_agent
    """

    # Create A Mock Console Instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    # Create A Mock Table Instance
    mock_table_instance = MagicMock()
    mock_table.grid.return_value = mock_table_instance

    # Create A Mock Panel Instance
    mock_panel_instance = MagicMock()
    mock_panel.return_value = mock_panel_instance

    # Create A Mock Agent
    mock_agent = MagicMock()
    mock_agent.name = "Zenith"
    mock_agent.description = "Test Description"
    mock_create_assistant_agent.return_value = mock_agent

    # Create Test Config
    test_config = {"zenith_openai_api_key": "test_key"}

    # Create A Test Context Object For The Command
    test_ctx = MagicMock()
    test_ctx.obj = test_config

    # Call The Function Directly
    from zenith.cli.commands import chat
    chat(test_ctx)

    # Assert Console Was Created
    mock_console.assert_called_once()

    # Assert create_assistant_agent Was Called With The Correct Arguments
    mock_create_assistant_agent.assert_called_once_with(test_config)

    # Assert Table.grid Was Called
    mock_table.grid.assert_called_once_with(expand=True)

    # Assert Table.add_column Was Called
    mock_table_instance.add_column.assert_called_once()

    # Assert Table.add_row Was Called Two Times (Name, Description)
    assert mock_table_instance.add_row.call_count == 2

    # Assert Panel Was Created
    mock_panel.assert_called_once()

    # Assert Console.print Was Called With The Panel
    mock_console_instance.print.assert_called_with(mock_panel_instance)
