# Standard Library Imports
import os
from pathlib import Path
from typing import Any


# Function To Write File Contents
def write_file(
    file_path: str,
    content: str,
    *,
    encoding: str = "utf-8",
    create_parents: bool = False,
    append: bool = False,
) -> dict[str, Any]:
    """
    Writes Content To A File

    Args:
        file_path (str): The Path To The File To Write
        content (str): The Content To Write To The File
        encoding (str): The Encoding To Use When Writing The File
        create_parents (bool): Whether To Create Parent Directories If They Don't Exist
        append (bool): Whether To Append To The File Instead Of Overwriting

    Returns:
        dict[str, Any]: A Dictionary Containing The Result And Metadata

    Raises:
        FileNotFoundError: If The Parent Directory Does Not Exist And create_parents Is False
        PermissionError: If Permission Is Denied
        ValueError: If The Path Is Invalid
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(file_path).resolve()

    # Check If Parent Directory Exists
    if not abs_path.parent.exists():
        # If We Should Create Parent Directories
        if create_parents:
            # Create Parent Directories
            abs_path.parent.mkdir(parents=True, exist_ok=True)

        else:
            # Raise A FileNotFoundError
            msg: str = f"Parent Directory Not Found: {abs_path.parent}"

            # Raise The Error
            raise FileNotFoundError(msg) from None

    try:
        # Determine The Write Mode
        mode: str = "a" if append else "w"

        # Write The File
        with abs_path.open(mode=mode, encoding=encoding) as f:
            # Write The Content
            f.write(content)

        # Get File Size
        file_size: int = abs_path.stat().st_size

        # Return The Result
        return {
            "success": True,
            "path": str(abs_path),
            "size": file_size,
            "size_human": _format_size(file_size),
            "encoding": encoding,
            "append": append,
        }

    except PermissionError:
        # Handle Permission Denied Error
        msg: str = f"Permission Denied: {abs_path}"

        # Raise The Error
        raise PermissionError(msg) from None

    except UnicodeEncodeError as e:
        # Handle Encoding Error
        msg: str = f"Failed To Encode Content With Encoding '{encoding}': {abs_path}"

        # Raise A ValueError
        raise ValueError(msg) from e

    except Exception as e:
        # Handle Other Errors
        msg: str = f"Failed To Write File: {abs_path}. Error: {e!s}"

        # Raise A ValueError
        raise ValueError(msg) from e


# Function To Check If A File Is Writable
def file_is_writable(file_path: str) -> bool:
    """
    Checks If A File Is Writable At The Specified Path

    Args:
        file_path (str): The Path To Check

    Returns:
        bool: True If The File Is Writable, False Otherwise
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(file_path).resolve()

    # If The File Exists
    if abs_path.exists():
        # Return Whether The File Is Writable
        return os.access(abs_path, os.W_OK)

    # If The File Doesn't Exist, Check If The Parent Directory Is Writable
    return os.access(abs_path.parent, os.W_OK) if abs_path.parent.exists() else False


# Helper Function To Format File Size
def _format_size(size: int) -> str:
    """
    Formats The File Size In A Human-Readable Format

    Args:
        size (int): The File Size In Bytes

    Returns:
        str: The Formatted File Size
    """

    # Define Size Units
    units: list[str] = ["B", "KB", "MB", "GB", "TB", "PB"]

    # Initialize Unit Index
    unit_index: int = 0

    # Convert Size
    size_float: float = float(size)

    # While The Size Is Greater Than 1024
    while size_float >= 1024 and unit_index < len(units) - 1:
        # Divide By 1024
        size_float /= 1024

        # Increment Unit Index
        unit_index += 1

    # Return Formatted Size
    return f"{size_float:.2f} {units[unit_index]}"


# Exports
__all__: list[str] = ["write_file"]
