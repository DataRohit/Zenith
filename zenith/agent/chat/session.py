# Standard Library Imports
import asyncio

# Third Party Imports
from autogen_agentchat.agents import AssistantAgent
from openai import APITimeoutError
from openai import BadRequestError
from openai import NotFoundError
from rich.console import Console

# Local Imports
from zenith.agent.chat.display import display_closing_message
from zenith.agent.chat.display import display_error_message
from zenith.agent.chat.display import display_initial_message
from zenith.agent.chat.display import display_user_prompt
from zenith.agent.chat.process import process_agent_response


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
    display_initial_message(console=console)

    # Start Chat Loop
    chat_active = True

    try:
        # While The Chat Is Active
        while chat_active:
            # Get User Input
            user_input = display_user_prompt(console=console)

            # Check If User Wants To Exit
            if user_input.lower() in ["quit", "exit"]:
                # Display Closing Message
                display_closing_message(console=console)

                # Exit The Loop
                chat_active = False

                # Continue The Loop
                continue

            # Add A Newline For Spacing Before Agent Response
            console.print("")

            # Process The Agent Response
            asyncio.run(
                process_agent_response(
                    console=console,
                    agent=agent,
                    user_input=user_input,
                ),
            )

    except KeyboardInterrupt:
        # Display A New Line For Better Formatting
        console.print("")

        # Display Closing Message
        display_closing_message(console=console)

    except BadRequestError:
        # Display A New Line For Better Formatting
        console.print("")

        # Display Error Message Using Consistent Formatting
        display_error_message(
            console=console,
            error_message="Invalid API Key! Please Pass A Valid API Key!",
        )

    except APITimeoutError:
        # Display A New Line For Better Formatting
        console.print("")

        # Display Error Message Using Consistent Formatting
        display_error_message(
            console=console,
            error_message="API Timeout! Please Check API Base URL And API Key!",
        )

    except NotFoundError:
        # Display A New Line For Better Formatting
        console.print("")

        # Display Error Message Using Consistent Formatting
        display_error_message(
            console=console,
            error_message="Invalid Model! Please Check Model Name!",
        )


# Exports
__all__: list[str] = [
    "start_chat",
]
