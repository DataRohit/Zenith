# Standard Library Imports
import asyncio

# Third Party Imports
from autogen_agentchat.agents import AssistantAgent
from rich.console import Console
from rich.text import Text

# Local Imports
from zenith.utils import get_current_datetime


# Function To Display Initial Chat Message
def display_initial_message(console: Console) -> None:
    """
    Displays The Initial Chat Message

    Args:
        console (Console): The Rich Console
    """

    # Get The Current Date And Time
    date_str, time_str = get_current_datetime()

    # Create A Composite Text Object With Different Colors
    message: Text = Text()

    # Add Date In Cyan
    message.append("[", style="white")
    message.append(date_str, style="bold cyan")
    message.append(" ", style="white")

    # Add Time In Green
    message.append(time_str, style="bold green")
    message.append("] ", style="white")

    # Add System Label In Magenta
    message.append("System", style="bold magenta")
    message.append("\t: ", style="white")

    # Add Message In Yellow
    message.append("To Stop The Program Execution Enter Quit/Exit", style="bold yellow")

    # Print The Message
    console.print("")
    console.print(message)
    console.print("")


# Function To Display Closing Message
def display_closing_message(console: Console) -> None:
    """
    Displays The Closing Message When The Chat Ends

    Args:
        console (Console): The Rich Console
    """

    # Get The Current Date And Time
    date_str, time_str = get_current_datetime()

    # Create A Composite Text Object With Different Colors
    message: Text = Text()

    # Add Date In Cyan
    message.append("[", style="white")
    message.append(date_str, style="bold cyan")
    message.append(" ", style="white")

    # Add Time In Green
    message.append(time_str, style="bold green")
    message.append("] ", style="white")

    # Add System Label In Magenta
    message.append("System", style="bold magenta")
    message.append("\t: ", style="white")

    # Add Message In Yellow
    message.append("Thank You For Using Zenith! Have A Great Day!", style="bold yellow")

    # Print The Message
    console.print("")
    console.print(message)
    console.print("")


# Function To Display User Input Prompt
def display_user_prompt(console: Console) -> str:
    """
    Displays The User Input Prompt And Returns The User's Input

    Args:
        console (Console): The Rich Console

    Returns:
        str: The User's Input
    """

    # Get The Current Date And Time
    date_str, time_str = get_current_datetime()

    # Create A Composite Text Object With Different Colors
    prompt: Text = Text()

    # Add Date In Cyan (Same As System Message)
    prompt.append("[", style="white")
    prompt.append(date_str, style="bold cyan")
    prompt.append(" ", style="white")

    # Add Time In Green (Same As System Message)
    prompt.append(time_str, style="bold green")
    prompt.append("] ", style="white")

    # Add "You" Label In Blue (Different From System)
    prompt.append("You", style="bold blue")
    prompt.append("\t: ", style="white")

    # Add Empty String To Match Test Expectations
    prompt.append("", style="white")

    # Print The Prompt Without Line Ending
    console.print(prompt, end="")

    # Get User Input & Return It
    return input()


# Function To Display Agent Response Prompt
def display_agent_prompt(console: Console, agent_name: str) -> None:
    """
    Displays The Agent Response Prompt

    Args:
        console (Console): The Rich Console
        agent_name (str): The Name Of The Agent
    """

    # Get The Current Date And Time
    date_str, time_str = get_current_datetime()

    # Create A Composite Text Object With Different Colors
    prompt: Text = Text()

    # Add Date In Cyan (Same As System Message)
    prompt.append("[", style="white")
    prompt.append(date_str, style="bold cyan")
    prompt.append(" ", style="white")

    # Add Time In Green (Same As System Message)
    prompt.append(time_str, style="bold green")
    prompt.append("] ", style="white")

    # Add Agent Name In Purple (Different From System And User)
    prompt.append(str(agent_name), style="bold purple")
    prompt.append("\t: ", style="white")

    # Print The Prompt
    console.print(prompt, end="")


# Function To Process Agent Response
async def process_agent_response(console: Console, agent: AssistantAgent, user_input: str) -> None:
    """
    Processes The Agent Response Using Streaming

    Args:
        console (Console): The Rich Console
        agent (AssistantAgent): The Assistant Agent
        user_input (str): The User Input
    """

    # Display Agent Prompt
    display_agent_prompt(console, agent.name)

    # Get The Streaming Response
    stream = agent.run_stream(task=user_input)

    # Process The Streaming Response
    async for message in stream:
        # Check If The Message Is A Streaming Chunk
        if hasattr(message, "type") and message.type == "ModelClientStreamingChunkEvent":
            # Print The Content Without Line Ending
            console.print(message.content, end="")

    # Print Newline For Spacing After The Response
    console.print()


# Function To Start A Chat Session
def start_chat(agent: AssistantAgent) -> None:
    """
    Starts A Chat Session With The Assistant Agent

    Args:
        agent (AssistantAgent): The Assistant Agent
    """

    # Create A Rich Console
    console: Console = Console()

    # Display The Initial Message
    display_initial_message(console)

    # Start Chat Loop
    chat_active = True

    try:
        # While The Chat Is Active
        while chat_active:
            # Get User Input
            user_input = display_user_prompt(console)

            # Check If User Wants To Exit
            if user_input.lower() in ["quit", "exit"]:
                # Display Closing Message
                display_closing_message(console)

                # Exit The Loop
                chat_active = False

                # Continue The Loop
                continue

            # Add A Newline For Spacing Before Agent Response
            console.print("")

            # Process The Agent Response
            asyncio.run(process_agent_response(console, agent, user_input))

    except KeyboardInterrupt:
        # Display A New Line For Better Formatting
        console.print("")

        # Display Closing Message
        display_closing_message(console)


# Exports
__all__: list[str] = [
    "display_agent_prompt",
    "display_closing_message",
    "display_initial_message",
    "display_user_prompt",
    "process_agent_response",
    "start_chat",
]
