# Standard Library Imports
from pathlib import Path
from typing import Any


# Function To Create A Directory
def make_directory(
    directory_path: str,
    *,
    parents: bool = True,
    exist_ok: bool = True,
    mode: int = 0o777,
) -> dict[str, Any]:
    """
    Creates A Directory At The Specified Path

    Args:
        directory_path (str): The Path Where The Directory Should Be Created
        parents (bool): If True, Create Parent Directories As Needed
        exist_ok (bool): If True, Do Not Raise An Error If The Directory Already Exists
        mode (int): The File Mode Bits To Apply To The Directory

    Returns:
        dict[str, Any]: A Dictionary Containing The Result Of The Operation

    Raises:
        ValueError: If The Path Is Invalid
        PermissionError: If Permission Is Denied
        FileExistsError: If The Directory Already Exists And exist_ok Is False
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(directory_path).resolve()

    try:
        # Create The Directory
        abs_path.mkdir(parents=parents, exist_ok=exist_ok, mode=mode)

        # Return Success Result
        return {
            "success": True,
            "path": str(abs_path),
            "message": f"Directory Created Successfully: {abs_path}",
        }

    except FileExistsError:
        # Handle Directory Already Exists Error
        msg: str = f"Directory Already Exists: {abs_path}"

        # Raise The Error
        raise FileExistsError(msg) from None

    except PermissionError:
        # Handle Permission Denied Error
        msg: str = f"Permission Denied: {abs_path}"

        # Raise The Error
        raise PermissionError(msg) from None

    except OSError as e:
        # Handle Other OS Errors
        msg: str = f"Failed To Create Directory: {abs_path}. Error: {e!s}"

        # Raise A ValueError
        raise ValueError(msg) from e


# Function To Check If A Directory Exists
def directory_exists(directory_path: str) -> bool:
    """
    Checks If A Directory Exists At The Specified Path

    Args:
        directory_path (str): The Path To Check

    Returns:
        bool: True If The Directory Exists, False Otherwise
    """

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(directory_path).resolve()

    # Return Whether The Path Exists And Is A Directory
    return abs_path.exists() and abs_path.is_dir()


# Exports
__all__: list[str] = ["make_directory"]
