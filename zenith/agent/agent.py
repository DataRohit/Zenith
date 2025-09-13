# Third Party Imports
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Function To Create A Model Client
def create_model_client(config: dict[str, str]) -> OpenAIChatCompletionClient:
    """
    Creates An OpenAI Chat Completion Client Using Configuration Values

    Args:
        config (dict[str, str]): The Configuration Dictionary

    Returns:
        OpenAIChatCompletionClient: The OpenAI Chat Completion Client
    """

    # Get Configuration Values
    api_key: str = config.get("zenith_openai_api_key", "")
    api_base: str = config.get("zenith_openai_api_base", "")
    model: str = config.get("zenith_model", "gpt-4")

    # Create And Return The Model Client
    return OpenAIChatCompletionClient(
        model=model,
        base_url=api_base,
        api_key=api_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": ModelFamily.ANY,
            "structured_output": False,
        },
    )


# Function To Create An Assistant Agent
def create_assistant_agent(
    config: dict[str, str],
    name: str = "Zenith",
) -> AssistantAgent:
    """
    Creates An Assistant Agent Using Configuration Values

    Args:
        config (dict[str, str]): The Configuration Dictionary
        name (str): The Name Of The Agent

    Returns:
        AssistantAgent: The Assistant Agent
    """

    # Get Configuration Values
    description: str = config.get(
        "zenith_assistant_description",
        "You Are Zenith, A CLI-Based AI Coding Agent That "
        "Transforms Natural Language Into Efficient, Production-Ready Code!",
    )

    system_message: str = config.get(
        "zenith_assistant_system_message",
        "You Are Zenith, A CLI-Based AI Coding Agent That "
        "Transforms Natural Language Into Efficient, Production-Ready Code!",
    )

    # Create The Model Client
    model_client: OpenAIChatCompletionClient = create_model_client(config)

    # Create And Return The Assistant Agent
    return AssistantAgent(
        name=name,
        description=description,
        system_message=system_message,
        model_client=model_client,
        model_client_stream=True,
    )


# Exports
__all__: list[str] = ["create_assistant_agent", "create_model_client"]
