# Third Party Imports
from rich.console import Console

# Local Imports
from zenith.cli.interface import create_panel


# Main Function
def main() -> None:
    """
    Main Function
    """

    # Create Console
    console = Console()

    # Create Panel
    panel = create_panel()

    # Print Panel
    console.print(panel)


# If The Script Is Run Directly
if __name__ == "__main__":
    # Run Main Function
    main()
