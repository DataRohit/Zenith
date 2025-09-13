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

    # Print The Prompt Without Line Ending
    console.print(prompt, end="")

    # Get User Input & Return It
    return input()


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

    # Start Chat Loop
    chat_active = True

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


# Exports
__all__: list[str] = ["display_closing_message", "display_initial_message", "display_user_prompt", "start_chat"]
