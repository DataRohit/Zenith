# Standard Library Imports
from pathlib import Path

# Third Party Imports
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# Function To Create Panel
def create_panel() -> Panel:
    """
    Creates A Rich Panel With A Welcome Message And The Current Working Directory

    Returns:
        Panel: A Rich Panel instance with a professional design.
    """

    # ASCII Art For Zenith
    logo = (
        "███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗\n"
        "╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║\n"
        "  ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║\n"
        " ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║\n"
        "███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║\n"
        "╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝"
    )

    # Create Table For Layout
    table = Table.grid(expand=True)
    table.add_column(justify="center")

    # Add Content To The Table
    table.add_row(Text(logo, style="bold #9933FF"))
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
__all__ = ["create_panel"]
