# Standard Library Imports
from typing import TYPE_CHECKING

# Third Party Imports
from rich.console import Console
from rich.text import Text

# Local Imports
from zenith.utils import get_current_datetime

# Type Checking
if TYPE_CHECKING:
    # Third Party Imports
    from autogen_agentchat.agents import AssistantAgent


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
    message.append("To Stop The Program Execution Enter quit/exit", style="bold yellow")

    # Print The Message
    console.print("")
    console.print(message)
    console.print("")


# Function To Start A Chat Session
def start_chat(agent: "AssistantAgent") -> None:
    """
    Starts A Chat Session With The Assistant Agent

    Args:
        agent (AssistantAgent): The Assistant Agent
    """

    # Create A Rich Console
    console: Console = Console()

    # Display The Initial Message
    display_initial_message(console)


# Exports
__all__: list[str] = ["display_initial_message", "start_chat"]
