# Standard Library Imports
from typing import TYPE_CHECKING

# Third Party Imports
import typer
from rich.console import Console

# Local Imports
from zenith.cli.interface import create_panel

# Type Checking
if TYPE_CHECKING:
    # Third Party Imports
    from rich.panel import Panel


# Help Callback
def help_callback(ctx: typer.Context, *, value: bool) -> None:
    """
    Help Callback

    Args:
        ctx (typer.Context): The Typer Context
        value (bool): The Value Of The Help Option

    Raises:
        typer.Exit: The Typer Exit
    """

    # If The Value Is Not True
    if not value:
        # Return
        return

    # Create A Rich Console
    console: Console = Console()

    # Create A Panel
    panel: Panel = create_panel()

    # Print The Panel
    console.print(panel)

    # Print The Help Message
    console.print(ctx.get_help())

    # Exit The Application
    raise typer.Exit


# Exports
__all__: list[str] = ["help_callback"]
