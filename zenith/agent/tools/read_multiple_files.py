# Standard Library Imports
from typing import Any

# Local Imports
from zenith.agent.tools.read_file import read_file


# Function To Read Multiple Files
def read_multiple_files(
    file_paths: list[str],
    *,
    encoding: str = "utf-8",
    start_line: int | None = None,
    end_line: int | None = None,
) -> list[dict[str, Any]]:
    """
    Reads The Contents Of Multiple Files

    Args:
        file_paths (list[str]): A List Of Paths To The Files To Read
        encoding (str): The Encoding To Use When Reading The Files
        start_line (int | None): The Line Number To Start Reading From (1-based, Inclusive)
        end_line (int | None): The Line Number To End Reading At (1-based, Inclusive)

    Returns:
        list[dict[str, Any]]: A List Of Dictionaries, Each Containing The File Contents And Metadata
    """

    # Initialize Results List
    results: list[dict[str, Any]] = []

    # Iterate Through File Paths
    for file_path in file_paths:
        try:
            # Read The File
            file_content: dict[str, Any] = read_file(
                file_path,
                encoding=encoding,
                start_line=start_line,
                end_line=end_line,
            )

            # Add Success Status
            file_content["success"] = True

            # Append To Results
            results.append(file_content)

        except (FileNotFoundError, PermissionError, ValueError) as e:
            # Append Error Result
            results.append(
                {
                    "success": False,
                    "path": file_path,
                    "content": None,
                    "error": str(e),
                },
            )

    # Return Results
    return results


# Define Module Exports
__all__: list[str] = ["read_multiple_files"]
