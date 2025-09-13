# Standard Library Imports
import json
from pathlib import Path


# Function To Load JSON Configuration File
def load_json_config(config_path: Path) -> dict[str, str]:
    """
    Loads A JSON Configuration File And Returns Its Contents As A Dictionary

    Args:
        config_path (Path): The Path To The JSON Configuration File

    Returns:
        dict[str, str]: The Configuration As A Dictionary
    """

    # Open And Read The JSON File
    with Path.open(config_path, "r") as file:
        # Parse The JSON Data
        return json.load(file)


# Function To Load ENV Configuration File
def load_env_config(config_path: Path) -> dict[str, str]:
    """
    Loads An ENV Configuration File And Returns Its Contents As A Dictionary

    Args:
        config_path (Path): The Path To The ENV Configuration File

    Returns:
        dict[str, str]: The Configuration As A Dictionary
    """

    # Initialize An Empty Dictionary
    config: dict[str, str] = {}

    # Open And Read The ENV File
    with Path.open(config_path, "r") as file:
        # Read Each Line
        for line in file:
            # If The Line Is Empty
            if not line.strip():
                # Skip The Line
                continue

            # Split The Line By The First Equals Sign
            if "=" in line:
                # Split The Line By The First Equals Sign
                key, value = line.strip().split("=", 1)

                # Convert The Key To Lowercase And Remove ZENITH_ Prefix
                key = key.lower()

                # If The Key Starts With ZENITH_
                if key.startswith("zenith_"):
                    # Add The Key-Value Pair To The Configuration Dictionary
                    config[key] = value

                else:
                    # Add The Key-Value Pair To The Configuration Dictionary
                    config[f"zenith_{key}"] = value

    # Return The Configuration
    return config


# Function To Load Configuration File Based On File Extension
def load_config(config_path: Path) -> dict[str, str]:
    """
    Loads A Configuration File Based On Its Extension And Returns Its Contents As A Dictionary

    Args:
        config_path (Path): The Path To The Configuration File

    Returns:
        dict[str, str]: The Configuration As A Dictionary

    Raises:
        ValueError: If The Configuration File Has An Unsupported Extension
    """

    # Get The File Extension
    file_extension: str = config_path.suffix.lower()

    # If The File Extension Is JSON
    if file_extension == ".json":
        # Load The JSON Configuration
        return load_json_config(config_path)

    # If The File Extension Is ENV
    if file_extension == ".env":
        # Load The ENV Configuration
        return load_env_config(config_path)

    # Raise A ValueError
    msg = f"Unsupported Configuration File Extension: {file_extension}"
    raise ValueError(msg)


# Exports
__all__: list[str] = ["load_config", "load_env_config", "load_json_config"]
