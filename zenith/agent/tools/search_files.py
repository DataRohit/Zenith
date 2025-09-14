# Standard Library Imports
import fnmatch
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

# Local Imports
from zenith.utils.format_file_size import format_size

# Type Checking Imports
if TYPE_CHECKING:
    # Standard Library Imports
    from os import stat_result


# Function To Search Files
def search_files(  # noqa: PLR0913
    search_pattern: str,
    directory: str | None = None,
    *,
    case_sensitive: bool = False,
    file_types: list[str] | None = None,
    max_results: int = 100,
    include_hidden: bool = False,
    respect_gitignore: bool = True,
) -> list[dict[str, Any]]:
    """
    Searches For Files Matching A Pattern In The Specified Directory

    Args:
        search_pattern (str): The Pattern To Search For
        directory (str | None): The Directory To Search In, Defaults To Current Directory
        case_sensitive (bool): Whether The Search Should Be Case Sensitive
        file_types (list[str] | None): List Of File Extensions To Include (e.g., ["py", "txt"])
        max_results (int): Maximum Number Of Results To Return
        include_hidden (bool): Whether To Include Hidden Files And Directories
        respect_gitignore (bool): Whether To Respect .gitignore Patterns

    Returns:
        list[dict[str, Any]]: A List Of Matching Files With Metadata

    Raises:
        ValueError: If The Directory Does Not Exist
    """

    # If No Directory Is Provided
    if directory is None:
        # Use The Current Directory
        directory = Path.cwd()

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(directory).resolve()

    # If The Directory Does Not Exist
    if not abs_path.exists():
        # Raise A ValueError
        msg: str = f"Directory Does Not Exist: {abs_path}"

        # Raise A ValueError
        raise ValueError(msg)

    # If The Path Is Not A Directory
    if not abs_path.is_dir():
        # Raise A ValueError
        msg: str = f"Path Is Not A Directory: {abs_path}"

        # Raise A ValueError
        raise ValueError(msg)

    # If Case-Insensitive Search
    if not case_sensitive:
        # Convert The Pattern To Lowercase For Case-Insensitive Search
        search_pattern = search_pattern.lower()

    # Load Gitignore Patterns If Needed
    gitignore_patterns: list[re.Pattern] = []

    # If We're Respecting Gitignore
    if respect_gitignore:
        # Find Project Root
        project_root: Path = _find_project_root(abs_path)

        # Load Gitignore Patterns
        gitignore_patterns = _load_gitignore_patterns(project_root)

    # Initialize Results
    results: list[dict[str, Any]] = []

    # Search For Files
    for result in _search_directory(
        directory=abs_path,
        search_pattern=search_pattern,
        case_sensitive=case_sensitive,
        file_types=file_types,
        include_hidden=include_hidden,
        gitignore_patterns=gitignore_patterns,
        respect_gitignore=respect_gitignore,
        project_root=project_root if respect_gitignore else abs_path,
        max_results=max_results,
    ):
        # Add The Result
        results.append(result)

        # If We've Reached The Maximum Number Of Results
        if len(results) >= max_results:
            # Break The Loop
            break

    # Return The Results
    return results


# Helper Function To Process A File
def _process_file(  # noqa: PLR0913
    item: os.DirEntry,
    search_pattern: str,
    *,
    case_sensitive: bool,
    file_types: list[str] | None,
    respect_gitignore: bool,
    project_root: Path,
    gitignore_patterns: list[re.Pattern],
) -> dict[str, Any] | None:
    """
    Processes A File And Returns Its Metadata If It Matches The Search Criteria

    Args:
        item (os.DirEntry): The File Entry
        search_pattern (str): The Pattern To Search For
        case_sensitive (bool): Whether The Search Should Be Case Sensitive
        file_types (list[str] | None): List Of File Extensions To Include
        respect_gitignore (bool): Whether To Respect .gitignore Patterns
        project_root (Path): The Root Directory Of The Project
        gitignore_patterns (list[re.Pattern]): List Of Compiled Gitignore Patterns

    Returns:
        dict[str, Any] | None: The File Metadata If It Matches, None Otherwise
    """

    # Get The Full Path
    full_path: Path = Path(item.path)

    # Check File Type Filter
    if file_types:
        # Get The File Extension
        file_ext: str = full_path.suffix.lstrip(".")

        # If The File Extension Is Not In The List
        if file_ext not in file_types:
            # Skip The File
            return None

    # Check Gitignore
    if respect_gitignore:
        # Get Relative Path From Project Root
        rel_path: str = os.path.relpath(full_path, project_root)

        # If The File Is Ignored
        if _is_ignored(rel_path, gitignore_patterns):
            # Skip The File
            return None

    # Get The File Name For Matching
    file_name: str = item.name

    # If Case-Insensitive Search
    if not case_sensitive:
        # Convert The File Name To Lowercase
        file_name = file_name.lower()

    # Check If The File Name Matches The Pattern
    if case_sensitive:
        # Use Exact Pattern Matching For Case-Sensitive Search
        if search_pattern not in file_name:
            # No Match
            return None

    # Use Wildcard Pattern Matching For Case-Insensitive Search
    elif not fnmatch.fnmatch(file_name, f"*{search_pattern}*"):
        # No Match
        return None

    # Get File Stats
    stats: stat_result = full_path.stat()

    # Return The File Metadata
    return {
        "name": item.name,
        "path": str(full_path),
        "size": stats.st_size,
        "size_human": format_size(stats.st_size),
        "modified": stats.st_mtime,
        "type": "file",
    }


# Helper Function To Check If A Directory Should Be Skipped
def _should_skip_directory(
    path: Path,
    *,
    respect_gitignore: bool,
    project_root: Path,
    gitignore_patterns: list[re.Pattern],
) -> bool:
    """
    Checks If A Directory Should Be Skipped Based On Gitignore Rules

    Args:
        path (Path): The Directory Path
        respect_gitignore (bool): Whether To Respect .gitignore Patterns
        project_root (Path): The Root Directory Of The Project
        gitignore_patterns (list[re.Pattern]): List Of Compiled Gitignore Patterns

    Returns:
        bool: True If The Directory Should Be Skipped, False Otherwise
    """

    # If We're Not Respecting Gitignore
    if not respect_gitignore:
        # Don't Skip
        return False

    # Get Relative Path From Project Root
    rel_path: str = os.path.relpath(path, project_root)

    # Return Whether The Directory Is Ignored
    return _is_ignored(rel_path, gitignore_patterns)


# Helper Function To Search A Directory
def _search_directory(  # noqa: PLR0913
    directory: Path,
    search_pattern: str,
    *,
    case_sensitive: bool,
    file_types: list[str] | None,
    include_hidden: bool,
    gitignore_patterns: list[re.Pattern],
    respect_gitignore: bool,
    project_root: Path,
    max_results: int,
) -> list[dict[str, Any]]:
    """
    Searches A Directory For Files Matching A Pattern

    Args:
        directory (Path): The Directory To Search In
        search_pattern (str): The Pattern To Search For
        case_sensitive (bool): Whether The Search Should Be Case Sensitive
        file_types (list[str] | None): List Of File Extensions To Include
        include_hidden (bool): Whether To Include Hidden Files And Directories
        gitignore_patterns (list[re.Pattern]): List Of Compiled Gitignore Patterns
        respect_gitignore (bool): Whether To Respect .gitignore Patterns
        project_root (Path): The Root Directory Of The Project
        max_results (int): Maximum Number Of Results To Return

    Returns:
        list[dict[str, Any]]: A List Of Matching Files With Metadata
    """

    # Initialize Results
    results: list[dict[str, Any]] = []

    try:
        # Iterate Through All Items In The Directory
        directory_items = list(os.scandir(directory))

    except (PermissionError, OSError):
        # Handle Permission Errors Or Other OS Errors
        return results

    # Process Each Item
    for item in directory_items:
        # If We've Reached The Maximum Number Of Results
        if len(results) >= max_results:
            # Break The Loop
            break

        # If The Item Is Hidden And We're Not Including Hidden Files
        if not include_hidden and item.name.startswith("."):
            # Skip The Item
            continue

        try:
            # Process Directories
            if item.is_dir():
                # Get The Full Path
                full_path: Path = Path(item.path)

                # Check If Directory Should Be Skipped
                if _should_skip_directory(
                    path=full_path,
                    respect_gitignore=respect_gitignore,
                    project_root=project_root,
                    gitignore_patterns=gitignore_patterns,
                ):
                    # Skip The Directory
                    continue

                # Recursively Search The Directory
                subdir_results = _search_directory(
                    directory=full_path,
                    search_pattern=search_pattern,
                    case_sensitive=case_sensitive,
                    file_types=file_types,
                    include_hidden=include_hidden,
                    gitignore_patterns=gitignore_patterns,
                    respect_gitignore=respect_gitignore,
                    project_root=project_root,
                    max_results=max_results - len(results),
                )

                # Add The Results
                results.extend(subdir_results)

            # Process Files
            elif item.is_file():
                # Process The File
                file_result = _process_file(
                    item=item,
                    search_pattern=search_pattern,
                    case_sensitive=case_sensitive,
                    file_types=file_types,
                    respect_gitignore=respect_gitignore,
                    project_root=project_root,
                    gitignore_patterns=gitignore_patterns,
                )

                # If We Got A Result
                if file_result:
                    # Add It To The Results
                    results.append(file_result)

        except (PermissionError, OSError):
            # Skip Items We Can't Access
            continue

    # Return The Results
    return results


# Helper Function To Find Project Root
def _find_project_root(start_path: Path) -> Path:
    """
    Finds The Project Root Directory (The One Containing .git)

    Args:
        start_path (Path): The Starting Path

    Returns:
        Path: The Project Root Directory
    """

    # Start With The Given Path
    current_path: Path = start_path

    # While Not At The Root Directory
    while current_path != current_path.parent:
        # Check If .git Directory Exists
        if (current_path / ".git").exists():
            # Return The Current Path
            return current_path

        # Move Up One Directory
        current_path: Path = current_path.parent

    # If No .git Directory Found, Use The Start Path
    return start_path


# Helper Function To Load Gitignore Patterns
def _load_gitignore_patterns(project_root: Path) -> list[re.Pattern]:
    """
    Loads And Compiles Gitignore Patterns

    Args:
        project_root (Path): The Project Root Directory

    Returns:
        list[re.Pattern]: List Of Compiled Gitignore Patterns
    """

    # Initialize Patterns List
    patterns: list[re.Pattern] = []

    # Path To Gitignore File
    gitignore_path: Path = project_root / ".gitignore"

    # If Gitignore File Exists
    if gitignore_path.exists():
        # Read Gitignore File
        with Path.open(gitignore_path, "r") as f:
            # Read Lines
            lines: list[str] = f.readlines()

            # Process Each Line
            for line in lines:
                # Strip Whitespace
                line: str = line.strip()  # noqa: PLW2901

                # If The Line Is Empty Or Starts With A Comment
                if not line or line.startswith("#"):
                    # Skip
                    continue

                # Convert Gitignore Pattern To Regex
                pattern: str = _gitignore_to_regex(line)

                # Compile The Regex
                regex: re.Pattern = re.compile(pattern)

                # Add To Patterns List
                patterns.append(regex)

    # Return Patterns
    return patterns


# Helper Function To Convert Gitignore Pattern To Regex
def _gitignore_to_regex(pattern: str) -> str:
    """
    Converts A Gitignore Pattern To A Regex Pattern

    Args:
        pattern (str): The Gitignore Pattern

    Returns:
        str: The Regex Pattern
    """

    # If The Pattern Is A Negation
    is_negation: bool = pattern.startswith("!")

    # If The Pattern Is A Negation
    if is_negation:
        # Remove The Negation
        pattern: str = pattern[1:]

    # If The Pattern Is A Directory-Only Pattern
    is_dir_only: bool = pattern.endswith("/")

    # If The Pattern Is A Directory-Only Pattern
    if is_dir_only:
        # Remove The Trailing Slash
        pattern: str = pattern[:-1]

    # Escape Special Characters
    pattern: str = re.escape(pattern)

    # Handle Wildcards
    pattern: str = pattern.replace("\\*\\*", ".*")
    pattern: str = pattern.replace("\\*", "[^/]*")
    pattern: str = pattern.replace("\\?", "[^/]")

    # If The Pattern Is A Directory-Only Pattern
    if is_dir_only:
        # Add Directory Pattern
        pattern: str = f"^{pattern}$|^{pattern}/.*$"

    else:
        # Add File Pattern
        pattern: str = f"^{pattern}$|^{pattern}/.*$"

    # Return Pattern
    return pattern


# Helper Function To Check If A Path Is Ignored
def _is_ignored(path: str, patterns: list[re.Pattern]) -> bool:
    """
    Checks If A Path Is Ignored By Gitignore Patterns

    Args:
        path (str): The Path To Check
        patterns (list[re.Pattern]): List Of Compiled Gitignore Patterns

    Returns:
        bool: True If The Path Is Ignored, False Otherwise
    """

    # Normalize Path
    path: str = path.replace("\\", "/")

    # Check Each Pattern And Return True If Any Pattern Matches
    return any(pattern.search(path) for pattern in patterns)


# Exports
__all__: list[str] = ["search_files"]
