# Standard Library Imports
from pathlib import Path
from typing import Any

# Local Imports
from zenith.utils.format_file_size import format_size


# Function To Read File Contents
def read_file(
    file_path: str,
    *,
    encoding: str = "utf-8",
    start_line: int | None = None,
    end_line: int | None = None,
) -> dict[str, Any]:
    """
    Reads The Contents Of A File

    Args:
        file_path (str): The Path To The File To Read
        encoding (str): The Encoding To Use When Reading The File
        start_line (int | None): The Line Number To Start Reading From (1-based, Inclusive)
        end_line (int | None): The Line Number To End Reading At (1-based, Inclusive)

    Returns:
        dict[str, Any]: A Dictionary Containing The File Contents And Metadata

    Raises:
        FileNotFoundError: If The File Does Not Exist
        PermissionError: If Permission Is Denied
        ValueError: If The Path Is Invalid Or If start_line > end_line
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(file_path).resolve()

    # Check If The File Exists
    if not abs_path.exists():
        # Raise A FileNotFoundError
        msg: str = f"File Not Found: {abs_path}"

        # Raise The Error
        raise FileNotFoundError(msg) from None

    # Check If The Path Is A File
    if not abs_path.is_file():
        # Raise A ValueError
        msg: str = f"Path Is Not A File: {abs_path}"

        # Raise The Error
        raise ValueError(msg) from None

    # Validate Line Range
    if start_line is not None and end_line is not None and start_line > end_line:
        # Raise A ValueError
        msg: str = f"Invalid Line Range: start_line ({start_line}) > end_line ({end_line})"

        # Raise The Error
        raise ValueError(msg) from None

    try:
        # If We're Reading Specific Lines
        if start_line is not None or end_line is not None:
            # Initialize Line Numbers
            start: int = max(1, start_line or 1) - 1  # Convert To 0-based

            # Read The File Line By Line
            with abs_path.open(encoding=encoding) as f:
                # Read All Lines
                lines: list[str] = f.readlines()

                # If We're Reading Specific Lines
                if end_line is not None:
                    # Get The Requested Lines
                    selected_lines: list[str] = lines[start:end_line]

                else:
                    # Get The Requested Lines
                    selected_lines: list[str] = lines[start:]

                # Join The Lines
                content: str = "".join(selected_lines)

                # Get Line Count
                line_count: int = len(lines)

                # Get Selected Line Count
                selected_line_count: int = len(selected_lines)

        else:
            # Read The File
            with abs_path.open(encoding=encoding) as f:
                # Read The File Content
                content = f.read()

                # Count The Lines
                line_count: int = content.count("\n") + (0 if content == "" or content.endswith("\n") else 1)

                # Set Selected Line Count
                selected_line_count: int = line_count

        # Get File Size
        file_size: int = abs_path.stat().st_size

        # Return The Result
        return {
            "success": True,
            "path": str(abs_path),
            "content": content,
            "size": file_size,
            "size_human": format_size(file_size),
            "line_count": line_count,
            "selected_line_count": selected_line_count,
            "encoding": encoding,
        }

    except PermissionError:
        # Handle Permission Denied Error
        msg: str = f"Permission Denied: {abs_path}"

        # Raise The Error
        raise PermissionError(msg) from None

    except UnicodeDecodeError:
        # Handle Encoding Error
        msg: str = f"Failed To Decode File With Encoding '{encoding}': {abs_path}"

        # Raise A ValueError
        raise ValueError(msg) from None

    except Exception as e:
        # Handle Other Errors
        msg: str = f"Failed To Read File: {abs_path}. Error: {e!s}"

        # Raise A ValueError
        raise ValueError(msg) from e


# Function To Check If A File Exists
def file_exists(file_path: str) -> bool:
    """
    Checks If A File Exists At The Specified Path

    Args:
        file_path (str): The Path To Check

    Returns:
        bool: True If The File Exists, False Otherwise
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(file_path).resolve()

    # Return Whether The Path Exists And Is A File
    return abs_path.exists() and abs_path.is_file()


# Exports
__all__: list[str] = ["read_file"]
