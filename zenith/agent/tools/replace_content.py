# Standard Library Imports
from pathlib import Path
from typing import Any

# Local Imports
from zenith.utils.format_file_size import format_size


# Function To Replace Content In A File
def replace_content(
    file_path: str,
    old_content: str,
    new_content: str,
    *,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """
    Replaces The First Occurrence Of Old Content With New Content In A File

    Args:
        file_path (str): The Path To The File To Modify
        old_content (str): The Content To Be Replaced
        new_content (str): The Content To Replace With
        encoding (str): The Encoding To Use When Reading And Writing The File

    Returns:
        dict[str, Any]: A Dictionary Containing The Result And Metadata

    Raises:
        FileNotFoundError: If The File Does Not Exist
        PermissionError: If Permission Is Denied
        ValueError: If The Path Is Invalid Or Old Content Not Found
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

    try:
        # Read The Entire File Content
        original_content: str = abs_path.read_text(encoding=encoding)

        # Perform The Replacement
        modified_content: str = original_content.replace(old_content, new_content, 1)

        # If The Old Content Was Not Found
        if original_content == modified_content:
            # Raise A ValueError
            msg: str = f"Old Content Not Found In File: {abs_path}"

            # Raise The Error
            raise ValueError(msg) from None  # noqa: TRY301

        # Write The Modified Content Back To The File
        abs_path.write_text(modified_content, encoding=encoding)

        # Get New File Size
        file_size: int = abs_path.stat().st_size

        # Return The Result
        return {
            "success": True,
            "path": str(abs_path),
            "size": file_size,
            "size_human": format_size(file_size),
            "encoding": encoding,
            "replaced": True,
        }

    except PermissionError:
        # Handle Permission Denied Error
        msg: str = f"Permission Denied: {abs_path}"

        # Raise The Error
        raise PermissionError(msg) from None

    except UnicodeDecodeError:
        # Handle Encoding Error During Read
        msg: str = f"Failed To Decode File With Encoding '{encoding}': {abs_path}"

        # Raise A ValueError
        raise ValueError(msg) from None

    except UnicodeEncodeError as e:
        # Handle Encoding Error During Write
        msg: str = f"Failed To Encode Content With Encoding '{encoding}': {abs_path}"

        # Raise A ValueError
        raise ValueError(msg) from e

    except Exception as e:
        # Handle Other Errors
        msg: str = f"Failed To Replace Content In File: {abs_path}. Error: {e!s}"

        # Raise A ValueError
        raise ValueError(msg) from e


# Exports
__all__: list[str] = ["replace_content"]
