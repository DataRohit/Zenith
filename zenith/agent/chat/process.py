# Third Party Imports
from autogen_agentchat.agents import AssistantAgent
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

# Local Imports
from zenith.agent.chat.display import display_agent_prompt


# Function To Process Agent Response
async def process_agent_response(console: Console, agent: AssistantAgent, user_input: str) -> None:
    """
    Processes The Agent Response Using Streaming

    Args:
        console (Console): The Rich Console
        agent (AssistantAgent): The Assistant Agent
        user_input (str): The User Input
    """

    # Create And Start Spinner
    spinner = console.status(status=f"{agent.name} Is Thinking...", spinner="dots")
    spinner.start()

    # Flag To Track The First Chunk
    first_chunk = True

    # Variable To Store The Full Message
    full_message = ""

    # Create a Live display object (but don't start it yet)
    live = None

    try:
        # Get The Streaming Response
        stream = agent.run_stream(task=user_input)

        # Process The Streaming Response
        async for message in stream:
            # Check If The Message Is A Streaming Chunk
            if hasattr(message, "type") and message.type == "ModelClientStreamingChunkEvent":
                # If It's The First Chunk
                if first_chunk:
                    # Stop The Spinner
                    spinner.stop()

                    # Display The Agent Prompt
                    display_agent_prompt(
                        console=console,
                        agent_name=agent.name,
                    )

                    # Initialize the Live display
                    live = Live("", console=console, auto_refresh=True, refresh_per_second=10)
                    live.start()

                    # Set The Flag To False
                    first_chunk = False

                # Append The New Chunk To The Full Message
                full_message += message.content

                # If The Live Display Is Started
                if live:
                    # Render The Full Message As Markdown
                    markdown_content = Markdown(full_message)

                    # Update The Live Display With The Markdown Content
                    live.update(markdown_content)

    finally:
        # If No Chunks Were Received
        if first_chunk:
            # Stop The Spinner
            spinner.stop()

        # If The Live Display Is Started
        elif live:
            # Stop The Live Display
            live.stop()

    # Print Newline For Spacing After The Response
    console.print()


# Exports
__all__: list[str] = [
    "process_agent_response",
]
