# Standard Library Imports
import json
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

# Third Party Imports
import pytest

# Local Imports
from zenith.utils.config_loader import load_config
from zenith.utils.config_loader import load_env_config
from zenith.utils.config_loader import load_json_config


# Test For Loading JSON Configuration
@patch("zenith.utils.config_loader.Path.open", new_callable=mock_open)
@patch("zenith.utils.config_loader.json.load")
def test_load_json_config(mock_json_load: MagicMock, mock_file: MagicMock) -> None:
    """
    Tests The load_json_config Function

    Args:
        mock_json_load (MagicMock): The Mock For json.load
        mock_file (MagicMock): The Mock For Path.open
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_json_load.return_value = {"zenith_openai_api_key": "test_key"}

    # Call The Function
    result = load_json_config(Path("config.json"))

    # Assert The Result Is Correct
    assert result == {"zenith_openai_api_key": "test_key"}

    # Assert json.load Was Called
    mock_json_load.assert_called_once()

    # Assert Path.open Was Called With The Correct Arguments
    mock_file.assert_called_once_with(Path("config.json"), "r")


# Test For Loading ENV Configuration With zenith_ Prefix
@patch("zenith.utils.config_loader.Path.open")
def test_load_env_config_with_zenith_prefix(mock_file: MagicMock) -> None:
    """
    Tests The load_env_config Function With zenith_ Prefix

    Args:
        mock_file (MagicMock): The Mock For Path.open
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_file.return_value.__enter__.return_value = [
        "zenith_openai_api_key=test_key\n",
        "zenith_model=gpt-4\n",
        "\n",  # Empty Line
    ]

    # Call The Function
    result = load_env_config(Path(".config.env"))

    # Assert The Result Is Correct
    assert result == {
        "zenith_openai_api_key": "test_key",
        "zenith_model": "gpt-4",
    }

    # Assert Path.open Was Called With The Correct Arguments
    mock_file.assert_called_once_with(Path(".config.env"), "r")


# Test For Loading ENV Configuration Without zenith_ Prefix
@patch("zenith.utils.config_loader.Path.open")
def test_load_env_config_without_zenith_prefix(mock_file: MagicMock) -> None:
    """
    Tests The load_env_config Function Without zenith_ Prefix

    Args:
        mock_file (MagicMock): The Mock For Path.open
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_file.return_value.__enter__.return_value = [
        "openai_api_key=test_key\n",
        "model=gpt-4\n",
    ]

    # Call The Function
    result = load_env_config(Path(".config.env"))

    # Assert The Result Is Correct
    assert result == {
        "zenith_openai_api_key": "test_key",
        "zenith_model": "gpt-4",
    }

    # Assert Path.open Was Called With The Correct Arguments
    mock_file.assert_called_once_with(Path(".config.env"), "r")


# Test For Loading ENV Configuration With Mixed Prefixes
@patch("zenith.utils.config_loader.Path.open")
def test_load_env_config_with_mixed_prefixes(mock_file: MagicMock) -> None:
    """
    Tests The load_env_config Function With Mixed Prefixes

    Args:
        mock_file (MagicMock): The Mock For Path.open
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_file.return_value.__enter__.return_value = [
        "zenith_openai_api_key=test_key\n",
        "model=gpt-4\n",
    ]

    # Call The Function
    result = load_env_config(Path(".config.env"))

    # Assert The Result Is Correct
    assert result == {
        "zenith_openai_api_key": "test_key",
        "zenith_model": "gpt-4",
    }

    # Assert Path.open Was Called With The Correct Arguments
    mock_file.assert_called_once_with(Path(".config.env"), "r")


# Test For Loading ENV Configuration With Invalid Line
@patch("zenith.utils.config_loader.Path.open")
def test_load_env_config_with_invalid_line(mock_file: MagicMock) -> None:
    """
    Tests The load_env_config Function With An Invalid Line

    Args:
        mock_file (MagicMock): The Mock For Path.open
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_file.return_value.__enter__.return_value = [
        "zenith_openai_api_key=test_key\n",
        "invalid_line\n",  # Invalid Line
        "model=gpt-4\n",
    ]

    # Call The Function
    result = load_env_config(Path(".config.env"))

    # Assert The Result Is Correct
    assert result == {
        "zenith_openai_api_key": "test_key",
        "zenith_model": "gpt-4",
    }

    # Assert Path.open Was Called With The Correct Arguments
    mock_file.assert_called_once_with(Path(".config.env"), "r")


# Test For Loading Configuration With JSON Extension
@patch("zenith.utils.config_loader.load_json_config")
def test_load_config_with_json_extension(mock_load_json_config: MagicMock) -> None:
    """
    Tests The load_config Function With A JSON Extension

    Args:
        mock_load_json_config (MagicMock): The Mock For load_json_config
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_load_json_config.return_value = {"zenith_openai_api_key": "test_key"}

    # Call The Function
    result = load_config(Path("config.json"))

    # Assert The Result Is Correct
    assert result == {"zenith_openai_api_key": "test_key"}

    # Assert load_json_config Was Called With The Correct Arguments
    mock_load_json_config.assert_called_once_with(Path("config.json"))


# Test For Loading Configuration With ENV Extension
@patch("zenith.utils.config_loader.load_env_config")
def test_load_config_with_env_extension(mock_load_env_config: MagicMock) -> None:
    """
    Tests The load_config Function With An ENV Extension

    Args:
        mock_load_env_config (MagicMock): The Mock For load_env_config
    """

    # Set Up The Mock To Return A Sample Configuration
    mock_load_env_config.return_value = {"zenith_openai_api_key": "test_key"}

    # Call The Function
    result = load_config(Path(".config.env"))

    # Assert The Result Is Correct
    assert result == {"zenith_openai_api_key": "test_key"}

    # Assert load_env_config Was Called With The Correct Arguments
    mock_load_env_config.assert_called_once_with(Path(".config.env"))


# Test For Loading Configuration With Unsupported Extension
def test_load_config_with_unsupported_extension() -> None:
    """
    Tests The load_config Function With An Unsupported Extension
    """

    # With pytest.raises
    with pytest.raises(ValueError) as exc_info:
        # Call The Function
        load_config(Path("config.yaml"))

    # Assert The Error Message Is Correct
    assert "Unsupported Configuration File Extension: .yaml" in str(exc_info.value)
