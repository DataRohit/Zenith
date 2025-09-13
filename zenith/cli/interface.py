# Standard Library Imports
from pathlib import Path

# Third Party Imports
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Local Imports
from zenith.cli.logo import LOGO


# Creates A Rich Panel With A Welcome Message
def create_panel() -> Panel:
    """
    Creates A Rich Panel With A Welcome Message

    Returns:
        Panel: A Rich Panel With A Welcome Message
    """

    # Create Table For Layout
    table: Table = Table.grid(expand=True)
    table.add_column(justify="center")

    # Add Content To The Table
    table.add_row(Text(LOGO, style="bold #9933FF"))
    table.add_row("")
    table.add_row(Text("Transforming Natural Language Into Production-Ready Code", style="#00BFFF"))
    table.add_row("")
    table.add_row(
        Text(
            (
                "Zenith Is A CLI-Based AI Coding Agent That Transforms "
                "Natural Language Into Efficient, Production-Ready Code!"
            ),
            justify="center",
        ),
    )
    table.add_row("")
    table.add_row(Text(f"Current Working Directory: {Path.cwd()}", style="dim"))

    # Return The Panel
    return Panel(
        table,
        title="[bold blue]🌌 Zenith[/bold blue]",
        border_style="bold blue",
        expand=True,
        padding=(2, 1, 1, 1),
    )


# Exports
__all__: list[str] = ["create_panel"]
