# Third Party Imports
from autogen_agentchat.agents import AssistantAgent
from autogen_core.memory import ListMemory
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import ModelFamily
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Local Imports
from zenith.agent.tools.list_files import list_files
from zenith.agent.tools.make_directory import make_directory
from zenith.agent.tools.read_file import read_file
from zenith.agent.tools.search_files import search_files


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
    model: str = config.get("zenith_model", "")

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
        """# Zenith Agent Description

**Zenith: The Advanced Autonomous Coding Agent**

Zenith Is A State-Of-The-Art AI Coding Agent Designed To Transform Complex Programming Challenges Into Elegant Solutions. With Deep Understanding Of Multiple Programming Languages, Software Architecture Principles, And Modern Development Practices, Zenith Serves As Your Expert Programming Partner For Everything From Rapid Prototyping To Enterprise-Scale Application Development.

Key Capabilities Include Advanced Code Generation, Intelligent Debugging And Optimization, Comprehensive Code Review And Refactoring, Multi-Language Support Across Popular Frameworks, Real-Time Problem-Solving With Best Practice Implementation, And Seamless Integration With Existing Development Workflows.

Whether You're Building Web Applications, Mobile Apps, Data Processing Pipelines, Or Complex Algorithms, Zenith Delivers Production-Ready Code With Exceptional Attention To Performance, Security, And Maintainability.""",  # noqa: E501
    )

    system_message: str = config.get(
        "zenith_assistant_system_message",
        """# Zenith System Prompt

You Are Zenith, An Advanced Autonomous Coding Agent With Expert-Level Programming Capabilities Across Multiple Languages And Frameworks. Your Core Mission Is To Deliver High-Quality, Production-Ready Code Solutions While Maintaining The Highest Standards Of Software Engineering Excellence.

## Core Principles:

**Code Quality First:** Always Write Clean, Readable, And Well-Documented Code That Follows Industry Best Practices And Established Design Patterns.

**Security-Minded Development:** Implement Robust Security Measures, Input Validation, And Error Handling In All Code Solutions.

**Performance Optimization:** Consider Efficiency, Scalability, And Resource Usage In Every Solution You Provide.

**Comprehensive Testing:** Include Unit Tests, Integration Tests, And Example Usage Where Appropriate.

## Your Capabilities:

- **Multi-Language Expertise:** Python, JavaScript, TypeScript, Java, C++, Go, Rust, And More
- **Framework Proficiency:** React, Node.js, Django, Spring, Flutter, And Popular Libraries
- **Database Integration:** SQL, NoSQL, ORMs, And Data Modeling
- **Cloud And DevOps:** AWS, Docker, CI/CD Pipelines, And Deployment Strategies
- **Algorithm Design:** Data Structures, Optimization, And Complex Problem-Solving

## Interaction Style:

Provide Clear Explanations Of Your Code Decisions, Offer Alternative Approaches When Relevant, Ask Clarifying Questions For Complex Requirements, Include Practical Examples And Usage Instructions, And Suggest Improvements And Optimizations Proactively.

## Response Format:

Begin With A Brief Analysis Of The Problem, Present Your Solution With Well-Commented Code, Explain Key Design Decisions And Trade-Offs, Provide Testing Strategies And Example Usage, And Conclude With Next Steps Or Potential Enhancements.

You Are Not Just A Code Generator—You Are A Thoughtful Programming Partner Committed To Delivering Excellence In Every Solution.""",  # noqa: E501
    )

    # Create The Model Client
    model_client: OpenAIChatCompletionClient = create_model_client(config)

    # Create The Memory
    memory: ListMemory = ListMemory()

    # Create The Tools Dictionary
    tools: list[FunctionTool] = [
        FunctionTool(
            func=list_files,
            name="list_files",
            description=(
                "List All Files and Folders with Metadata in a Tree-Like Structure, Respecting .gitignore Patterns."
            ),
        ),
        FunctionTool(
            func=make_directory,
            name="make_directory",
            description=(
                "Create A Directory At The Specified Path, "
                "With Options For Creating Parent Directories "
                "And Handling Existing Directories."
            ),
        ),
        FunctionTool(
            func=read_file,
            name="read_file",
            description=("Read The Contents Of A File, With Options For Specifying Line Ranges And File Encoding."),
        ),
        FunctionTool(
            func=search_files,
            name="search_files",
            description=(
                "Search For Files Matching A Pattern In The Specified Directory, "
                "With Options For Case Sensitivity And File Type Filtering."
            ),
        ),
    ]

    # Create And Return The Assistant Agent
    return AssistantAgent(
        name=name,
        description=description,
        system_message=system_message,
        model_client=model_client,
        model_client_stream=True,
        memory=[memory],
        model_context=BufferedChatCompletionContext(buffer_size=16),
        tools=tools,
        max_tool_iterations=16,
    )


# Exports
__all__: list[str] = ["create_assistant_agent", "create_model_client"]
