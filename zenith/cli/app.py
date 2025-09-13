# Third Party Imports
import typer

# Create A Typer App
app: typer.Typer = typer.Typer(
    name="zenith",
    add_completion=False,
    rich_markup_mode="markdown",
    help=(
        "Zenith Is A CLI-Based AI Coding Agent That Transforms Natural Language Into Efficient, Production-Ready Code!"
    ),
    add_help_option=False,
)

# Exports
__all__: list[str] = ["app"]
