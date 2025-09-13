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
from zenith.cli.commands import _show_error_and_exit

# Create A Runner
runner = CliRunner()


# Test For The Show Error And Exit Function
@patch("zenith.cli.commands.Panel")
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
        _show_error_and_exit(mock_console, "Test Error")

    # Assert The Exit Code
    assert exc_info.value.exit_code == 1

    # Assert The Panel Was Created With The Correct Arguments
    mock_panel.assert_called_once()

    # Assert The Console Print Was Called
    mock_console.print.assert_called_once_with(mock_panel.return_value)


# Test For Main Command With No Config
def test_main_no_config() -> None:
    """
    Tests The Main Command With No Config
    """

    # Invoke The App
    result = runner.invoke(app, [])

    # Assert The Exit Code
    assert result.exit_code == 1

    # Assert The Output
    assert "Configuration File Not Found!" in result.stdout


# Test For Main Command With Provided Config File
@patch("zenith.cli.commands.create_panel")
def test_main_with_provided_config(mock_create_panel: MagicMock) -> None:
    """
    Tests The Main Command With A Provided Config File

    Args:
        mock_create_panel (MagicMock): The Mock Create Panel
    """

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


# Test For Main Command With .zenith/config.json
@patch("zenith.cli.commands.create_panel")
def test_main_with_zenith_config_json(mock_create_panel: MagicMock) -> None:
    """
    Tests The Main Command With .zenith/config.json

    Args:
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A .zenith Directory
        zenith_dir = Path(temp_dir) / ".zenith"
        zenith_dir.mkdir()

        # Create A Config File
        (zenith_dir / "config.json").touch()

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 0

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()


# Test For Main Command With .zenith/.config.env
@patch("zenith.cli.commands.create_panel")
def test_main_with_zenith_config_env(mock_create_panel: MagicMock) -> None:
    """
    Tests The Main Command With .zenith/.config.env

    Args:
        mock_create_panel (MagicMock): The Mock Create Panel
    """

    # With runner.isolated_filesystem
    with runner.isolated_filesystem() as temp_dir:
        # Create A .zenith Directory
        zenith_dir = Path(temp_dir) / ".zenith"
        zenith_dir.mkdir()

        # Create A Config File
        (zenith_dir / ".config.env").touch()

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 0

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()


# Test For Main Command With Both .zenith Configs
@patch("zenith.cli.commands.create_panel")
def test_main_with_both_zenith_configs(mock_create_panel: MagicMock) -> None:
    """
    Tests An Error Is Raised When Both .zenith Config Files Exist

    Args:
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

        # Invoke The App
        result = runner.invoke(app, [])

        # Assert The Exit Code
        assert result.exit_code == 1

        # Assert The Error Message Is In The Output
        assert "Both 'config.json' and '.config.env' found" in result.stdout

        # Assert create_panel Was Called
        mock_create_panel.assert_called_once()
