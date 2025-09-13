# Third Party Imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# Function To Display Configuration
def display_config(console: Console, config: dict[str, str]) -> None:
    """
    Displays The Configuration In A Rich Interface

    Args:
        console (Console): The Rich Console
        config (dict[str, str]): The Configuration Dictionary
    """

    # Get Configuration Values
    api_key: str = config.get("zenith_openai_api_key", "")
    masked_key: str = mask_api_key(api_key)
    api_base: str = config.get("zenith_openai_api_base", "")
    model: str = config.get("zenith_model", "")

    # Create Table For Layout
    table: Table = Table.grid(expand=True)
    table.add_column(justify="center")

    # Add Content To The Table
    table.add_row(Text("API Key:", style="#FF6B6B") + Text(f" {masked_key}", style="#00BFFF"))
    table.add_row(Text("API Base URL:", style="#FF6B6B") + Text(f" {api_base}", style="#00BFFF"))
    table.add_row(Text("Model:", style="#FF6B6B") + Text(f" {model}", style="#00BFFF"))

    # Create And Print The Panel
    panel: Panel = Panel(
        table,
        title="[bold blue]Configuration[/bold blue]",
        title_align="center",
        border_style="bold blue",
        expand=True,
        padding=(1, 2),
    )

    # Print The Panel
    console.print(panel)


# Function To Mask API Key
def mask_api_key(api_key: str) -> str:
    """
    Masks An API Key For Display

    Args:
        api_key (str): The API Key To Mask

    Returns:
        str: The Masked API Key
    """

    # If The API Key Is Empty
    if not api_key:
        # Return An Empty String
        return ""

    # Get The Length Of The API Key
    key_length: int = len(api_key)

    # If The API Key Is Too Short
    if key_length <= 8:
        # Return The Masked API Key
        return "****" + api_key[-4:] if key_length >= 4 else "****"

    # Return The Masked API Key
    return api_key[:4] + "*" * (key_length - 8) + api_key[-4:]


# Exports
__all__: list[str] = ["display_config", "mask_api_key"]
