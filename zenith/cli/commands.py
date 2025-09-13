# Standard Library Imports
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Annotated

# Third Party Imports
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Local Imports
from zenith.agent import create_assistant_agent
from zenith.agent import start_chat
from zenith.cli.app import app
from zenith.cli.callbacks import help_callback
from zenith.cli.config_display import display_config
from zenith.cli.interface import create_panel
from zenith.utils import load_config

# Type Checking
if TYPE_CHECKING:
    # Third Party Imports
    from autogen_agentchat.agents import AssistantAgent


# The Main Command For The Zenith CLI Application
@app.callback(invoke_without_command=True, help="")
def main(
    ctx: typer.Context,
    config: Annotated[
        Path | None,
        typer.Option(
            "--config",
            "-c",
            help="Path To The Configuration File (.json Or .env).",
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ] = None,
    *,
    help: Annotated[  # noqa: A002
        bool,
        typer.Option(
            "--help",
            "-h",
            callback=help_callback,
            is_eager=True,
            help="Show This Message And Exit.",
        ),
    ] = False,
) -> None:
    """
    The Main Command For The Zenith CLI Application

    Args:
        ctx (typer.Context): The Typer Context
        config (Optional[Path]): The Path To The Configuration File
        help (bool): A Flag To Show The Help Message And Exit
    """

    # Create A Rich Console
    console: Console = Console()

    # Create A Panel
    panel: Panel = create_panel()

    # Print The Panel
    console.print(panel)

    # If The Configuration File Is Not Provided
    if config is None:
        # Define The .zenith Directory
        zenith_dir: Path = Path.cwd() / ".zenith"

        # If The .zenith Directory Exists
        if zenith_dir.is_dir():
            # Define Potential Configuration Files
            config_json: Path = zenith_dir / "config.json"
            config_env: Path = zenith_dir / ".config.env"

            # Check If Both Configuration Files Exist
            if config_json.is_file() and config_env.is_file():
                # Show Error
                console.print(
                    Panel(
                        Text(
                            "Both config.json And .config.env Files Exist In The .zenith Directory!\n"
                            "Please Remove One Of Them And Try Again!",
                            style="bold red",
                            justify="center",
                        ),
                        title="[bold red]Configuration Error[/bold red]",
                        border_style="red",
                        expand=True,
                        padding=(1, 2),
                    ),
                )

                # Exit The Application
                raise typer.Exit(code=1)

            # If Only The config.json File Exists
            if config_json.is_file():
                # Set The Configuration Path
                config = config_json

            # If Only The .config.env File Exists
            if config_env.is_file():
                # Set The Configuration Path
                config = config_env

    # Load The Configuration
    config_dict: dict[str, str] = load_config(config)

    # Store The Configuration In The Context
    ctx.obj = config_dict

    # Display The Configuration
    display_config(console, config_dict)


# Chat Command For The Zenith CLI Application
@app.command("chat")
def chat(
    ctx: typer.Context,
) -> None:
    """
    Start A Chat Session With The Zenith AI Assistant

    Args:
        ctx (typer.Context): The Typer Context
    """

    # Create A Rich Console
    console: Console = Console()

    # Get The Configuration From The Context
    config: dict[str, str] = ctx.obj

    # Create The Assistant Agent
    agent: AssistantAgent = create_assistant_agent(config)

    # Get Agent Name And Properties
    agent_name: str = agent.name
    description: str = agent.description

    # Create Table For Layout
    table: Table = Table.grid(expand=True)
    table.add_column(justify="center")

    # Add Content To The Table
    table.add_row(Text("Agent Name:", style="#FF6B6B") + Text(f" {agent_name}", style="#00BFFF"))

    # Add Description With Markdown On Same Line
    description_text = (
        Text("Description:", style="#FF6B6B") + Text(" ", style="default") + Text(description, style="#00BFFF")
    )
    description_text.justify = "center"
    table.add_row(description_text)

    # Create And Print The Panel
    panel: Panel = Panel(
        table,
        title="[bold green]Agent Initialized Successfully[/bold green]",
        title_align="center",
        border_style="bold green",
        expand=True,
        padding=(1, 2),
    )

    # Print The Panel
    console.print(panel)

    # Start The Chat Session
    start_chat(agent)


# Exports
__all__: list[str] = ["chat", "main"]
