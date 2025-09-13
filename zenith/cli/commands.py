# Standard Library Imports
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Annotated

# Third Party Imports
import typer
from rich.console import Console

# Local Imports
from zenith.cli.app import app
from zenith.cli.callbacks import help_callback
from zenith.cli.config_display import display_config
from zenith.cli.interface import create_panel
from zenith.utils import load_config
from zenith.utils import show_error_and_exit

# Type Checking
if TYPE_CHECKING:
    # Third Party Imports
    from rich.panel import Panel


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
                # Show An Error Message And Exit
                show_error_and_exit(
                    console,
                    "Both 'config.json' and '.config.env' found in '.zenith' directory.\n"
                    "Please Provide Only One Configuration File.",
                )

            # If Only The config.json File Exists
            elif config_json.is_file():
                # Set The Configuration Path
                config = config_json

            # If Only The .config.env File Exists
            elif config_env.is_file():
                # Set The Configuration Path
                config = config_env

    # If The Configuration File Is Not Found
    if config is None:
        # Show An Error Message And Exit
        show_error_and_exit(
            console,
            (
                "Configuration File Not Found!\n"
                "Use The --config/-c Flag To Provide Config File Path\n"
                "Or Create .zenith Directory In Current Working Directory And Create Config File In It.\n"
                "Use The --help/-h Flag To See Full Implementation."
            ),
        )

    try:
        # Load The Configuration
        config_dict: dict[str, str] = load_config(config)

        # Store The Configuration In The Context
        ctx.obj = config_dict

        # Display The Configuration
        display_config(console, config_dict)

    except Exception as e:  # noqa: BLE001
        # Show An Error Message And Exit
        show_error_and_exit(console, f"Error Loading Configuration File: {e!s}")


# Exports
__all__: list[str] = ["main"]
