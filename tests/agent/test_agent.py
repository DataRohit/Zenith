# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Third Party Imports
import pytest
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Local Imports
from zenith.agent.agent import create_assistant_agent
from zenith.agent.agent import create_model_client


# Test For create_model_client Function
@patch("zenith.agent.agent.OpenAIChatCompletionClient")
def test_create_model_client(mock_client: MagicMock) -> None:
    """
    Tests The create_model_client Function

    Args:
        mock_client (MagicMock): The Mock For OpenAIChatCompletionClient
    """

    # Create A Sample Configuration
    config = {
        "zenith_openai_api_key": "test_key",
        "zenith_openai_api_base": "https://api.openai.com/v1",
        "zenith_model": "gpt-4",
    }

    # Call The Function
    result = create_model_client(config)

    # Assert The Result Is The Mock Client Instance
    assert result == mock_client.return_value

    # Assert OpenAIChatCompletionClient Was Called With The Correct Arguments
    mock_client.assert_called_once_with(
        model="gpt-4",
        base_url="https://api.openai.com/v1",
        api_key="test_key",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": ModelFamily.ANY,
            "structured_output": False,
        },
    )


# Test For create_model_client Function With Default Values
@patch("zenith.agent.agent.OpenAIChatCompletionClient")
def test_create_model_client_with_defaults(mock_client: MagicMock) -> None:
    """
    Tests The create_model_client Function With Default Values

    Args:
        mock_client (MagicMock): The Mock For OpenAIChatCompletionClient
    """

    # Create An Empty Configuration
    config = {}

    # Call The Function
    result = create_model_client(config)

    # Assert The Result Is The Mock Client Instance
    assert result == mock_client.return_value

    # Assert OpenAIChatCompletionClient Was Called With The Correct Arguments
    mock_client.assert_called_once_with(
        model="gpt-4",
        base_url="",
        api_key="",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": ModelFamily.ANY,
            "structured_output": False,
        },
    )


# Test For create_assistant_agent Function
@patch("zenith.agent.agent.create_model_client")
@patch("zenith.agent.agent.AssistantAgent")
def test_create_assistant_agent(
    mock_assistant: MagicMock, mock_create_model_client: MagicMock
) -> None:
    """
    Tests The create_assistant_agent Function

    Args:
        mock_assistant (MagicMock): The Mock For AssistantAgent
        mock_create_model_client (MagicMock): The Mock For create_model_client
    """

    # Create A Sample Configuration
    config = {"zenith_openai_api_key": "test_key"}

    # Call The Function
    result = create_assistant_agent(config)

    # Assert The Result Is The Mock Assistant Instance
    assert result == mock_assistant.return_value

    # Assert create_model_client Was Called With The Correct Arguments
    mock_create_model_client.assert_called_once_with(config)

    # Assert AssistantAgent Was Called With The Correct Arguments
    mock_assistant.assert_called_once_with(
        name="Zenith",
        description="You Are Zenith, A CLI-Based AI Coding Agent That Transforms Natural Language Into Efficient, Production-Ready Code!",
        system_message="You Are Zenith, A CLI-Based AI Coding Agent That Transforms Natural Language Into Efficient, Production-Ready Code!",
        model_client=mock_create_model_client.return_value,
        model_client_stream=True,
    )


# Test For create_assistant_agent Function With Custom Values From Config
@patch("zenith.agent.agent.create_model_client")
@patch("zenith.agent.agent.AssistantAgent")
def test_create_assistant_agent_with_custom_values(
    mock_assistant: MagicMock, mock_create_model_client: MagicMock
) -> None:
    """
    Tests The create_assistant_agent Function With Custom Values From Config

    Args:
        mock_assistant (MagicMock): The Mock For AssistantAgent
        mock_create_model_client (MagicMock): The Mock For create_model_client
    """

    # Create A Sample Configuration With Custom Values
    config = {
        "zenith_openai_api_key": "test_key",
        "zenith_assistant_description": "Custom Description",
        "zenith_assistant_system_message": "Custom System Message"
    }

    # Call The Function
    result = create_assistant_agent(config, name="custom_assistant")

    # Assert The Result Is The Mock Assistant Instance
    assert result == mock_assistant.return_value

    # Assert create_model_client Was Called With The Correct Arguments
    mock_create_model_client.assert_called_once_with(config)

    # Assert AssistantAgent Was Called With The Correct Arguments
    mock_assistant.assert_called_once_with(
        name="custom_assistant",
        description="Custom Description",
        system_message="Custom System Message",
        model_client=mock_create_model_client.return_value,
        model_client_stream=True,
    )
