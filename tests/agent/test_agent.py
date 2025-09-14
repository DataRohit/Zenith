# Standard Library Imports
from unittest.mock import MagicMock
from unittest.mock import patch

# Third Party Imports
from autogen_core.models import ModelFamily

# Local Imports
from zenith.agent.agent import create_assistant_agent
from zenith.agent.agent import create_model_client
from zenith.agent.tools.list_files import list_files
from zenith.agent.tools.make_directory import make_directory
from zenith.agent.tools.read_file import read_file
from zenith.agent.tools.read_multiple_files import read_multiple_files
from zenith.agent.tools.search_files import search_files
from zenith.agent.tools.write_file import write_file


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
        model="",
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
@patch("zenith.agent.agent.FunctionTool")
@patch("zenith.agent.agent.AssistantAgent")
@patch("zenith.agent.agent.BufferedChatCompletionContext")
@patch("zenith.agent.agent.ListMemory")
@patch("zenith.agent.agent.create_model_client")
def test_create_assistant_agent(
    mock_create_model_client: MagicMock,
    mock_list_memory: MagicMock,
    mock_buffered_context: MagicMock,
    mock_assistant: MagicMock,
    mock_function_tool: MagicMock
) -> None:
    """
    Tests The create_assistant_agent Function

    Args:
        mock_assistant (MagicMock): The Mock For AssistantAgent
        mock_buffered_context (MagicMock): The Mock For BufferedChatCompletionContext
        mock_list_memory (MagicMock): The Mock For ListMemory
        mock_create_model_client (MagicMock): The Mock For create_model_client
    """

    # Create A Sample Configuration
    config = {"zenith_openai_api_key": "test_key"}

    # Mock Configuration Values
    mock_description = "Test Description"
    mock_system_message = "Test System Message"

    # Create A Mock Config Dictionary With get Method
    mock_config = MagicMock()
    mock_config.get.side_effect = lambda key, default: {
        "zenith_assistant_description": mock_description,
        "zenith_assistant_system_message": mock_system_message,
    }.get(key, default)

    # Patch The Config Dictionary
    with patch.dict(config, mock_config, clear=True):
        # Call The Function With The Mock Config
        result = create_assistant_agent(mock_config)

    # Assert The Result Is The Mock Assistant Instance
    assert result == mock_assistant.return_value

    # Assert create_model_client Was Called With The Correct Arguments
    mock_create_model_client.assert_called_once_with(mock_config)

    # Assert ListMemory Was Called
    mock_list_memory.assert_called_once()

    # Assert BufferedChatCompletionContext Was Called With The Correct Arguments
    mock_buffered_context.assert_called_once_with(buffer_size=16)

    # Assert AssistantAgent Was Called With The Correct Arguments
    mock_assistant.assert_called_once_with(
        name="Zenith",
        description=mock_description,
        system_message=mock_system_message,
        model_client=mock_create_model_client.return_value,
        model_client_stream=True,
        memory=[mock_list_memory.return_value],
        model_context=mock_buffered_context.return_value,
        tools=[mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value],
        max_tool_iterations=16,
    )

    # Assert FunctionTool Was Called With The Correct Arguments
    mock_function_tool.assert_any_call(
        func=list_files,
        name="list_files",
        description=(
            "List All Files and Folders with Metadata in a Tree-Like Structure, Respecting .gitignore Patterns."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For make_directory
    mock_function_tool.assert_any_call(
        func=make_directory,
        name="make_directory",
        description=(
            "Create A Directory At The Specified Path, "
            "With Options For Creating Parent Directories "
            "And Handling Existing Directories."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For read_file
    mock_function_tool.assert_any_call(
        func=read_file,
        name="read_file",
        description=(
            "Read The Contents Of A File, With Options For Specifying Line Ranges "
            "And File Encoding."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For read_multiple_files
    mock_function_tool.assert_any_call(
        func=read_multiple_files,
        name="read_multiple_files",
        description=(
            "Reads The Contents Of Multiple Files, With Options For Specifying Line Ranges And File Encoding."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For search_files
    mock_function_tool.assert_any_call(
        func=search_files,
        name="search_files",
        description=(
            "Search For Files Matching A Pattern In The Specified Directory, "
            "With Options For Case Sensitivity And File Type Filtering."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For write_file
    mock_function_tool.assert_any_call(
        func=write_file,
        name="write_file",
        description=(
            "Write Content To A File At The Specified Path, "
            "With Options For Appending, Creating Parent Directories, "
            "And Specifying File Encoding."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For write_file
    mock_function_tool.assert_any_call(
        func=write_file,
        name="write_file",
        description=(
            "Write Content To A File At The Specified Path, "
            "With Options For Appending, Creating Parent Directories, "
            "And Specifying File Encoding."
        ),
    )


# Test For create_assistant_agent Function With Custom Values From Config
@patch("zenith.agent.agent.FunctionTool")
@patch("zenith.agent.agent.AssistantAgent")
@patch("zenith.agent.agent.BufferedChatCompletionContext")
@patch("zenith.agent.agent.ListMemory")
@patch("zenith.agent.agent.create_model_client")
def test_create_assistant_agent_with_custom_values(
    mock_create_model_client: MagicMock,
    mock_list_memory: MagicMock,
    mock_buffered_context: MagicMock,
    mock_assistant: MagicMock,
    mock_function_tool: MagicMock
) -> None:
    """
    Tests The create_assistant_agent Function With Custom Values From Config

    Args:
        mock_assistant (MagicMock): The Mock For AssistantAgent
        mock_buffered_context (MagicMock): The Mock For BufferedChatCompletionContext
        mock_list_memory (MagicMock): The Mock For ListMemory
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

    # Assert ListMemory Was Called
    mock_list_memory.assert_called_once()

    # Assert BufferedChatCompletionContext Was Called With The Correct Arguments
    mock_buffered_context.assert_called_once_with(buffer_size=16)

    # Assert AssistantAgent Was Called With The Correct Arguments
    mock_assistant.assert_called_once_with(
        name="custom_assistant",
        description="Custom Description",
        system_message="Custom System Message",
        model_client=mock_create_model_client.return_value,
        model_client_stream=True,
        memory=[mock_list_memory.return_value],
        model_context=mock_buffered_context.return_value,
        tools=[mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value, mock_function_tool.return_value],
        max_tool_iterations=16,
    )

    # Assert FunctionTool Was Called With The Correct Arguments
    mock_function_tool.assert_any_call(
        func=list_files,
        name="list_files",
        description=(
            "List All Files and Folders with Metadata in a Tree-Like Structure, Respecting .gitignore Patterns."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For make_directory
    mock_function_tool.assert_any_call(
        func=make_directory,
        name="make_directory",
        description=(
            "Create A Directory At The Specified Path, "
            "With Options For Creating Parent Directories "
            "And Handling Existing Directories."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For read_file
    mock_function_tool.assert_any_call(
        func=read_file,
        name="read_file",
        description=(
            "Read The Contents Of A File, With Options For Specifying Line Ranges "
            "And File Encoding."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For read_multiple_files
    mock_function_tool.assert_any_call(
        func=read_multiple_files,
        name="read_multiple_files",
        description=(
            "Reads The Contents Of Multiple Files, With Options For Specifying Line Ranges And File Encoding."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For search_files
    mock_function_tool.assert_any_call(
        func=search_files,
        name="search_files",
        description=(
            "Search For Files Matching A Pattern In The Specified Directory, "
            "With Options For Case Sensitivity And File Type Filtering."
        ),
    )

    # Assert FunctionTool Was Called With The Correct Arguments For write_file
    mock_function_tool.assert_any_call(
        func=write_file,
        name="write_file",
        description=(
            "Write Content To A File At The Specified Path, "
            "With Options For Appending, Creating Parent Directories, "
            "And Specifying File Encoding."
        ),
    )
