# Standard Library Imports
from typing import NoReturn

# Third Party Imports
import typer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


# Function To Show An Error And Exit
def show_error_and_exit(console: Console, message: str) -> NoReturn:
    """
    Creates And Displays An Error Panel, Then Exits The Application.

    Args:
        console (Console): The Rich Console
        message (str): The Error Message To Display

    Raises:
        typer.Exit: Exits The Application With A Non-Zero Code
    """

    # Create An Error Panel
    error_panel: Panel = Panel(
        Align.center(Text(message, justify="center")),
        title="[bold red]Error[/bold red]",
        border_style="red",
        expand=True,
    )

    # Print The Error Panel
    console.print(error_panel)

    # Exit The Application With A Non-Zero Code
    raise typer.Exit(code=1)
