# Standard Library Imports
import os
import re
import stat
from datetime import datetime
from pathlib import Path
from re import Pattern
from typing import TYPE_CHECKING
from typing import Any

# Third Party Imports
from dateutil import tz

from zenith.utils.format_file_size import format_size

# Type Checking Imports
if TYPE_CHECKING:
    # Standard Library Imports
    from os import stat_result


# Function To List Files And Folders With Metadata
def list_files(folder_path: str | None = None) -> dict[str, Any]:
    """
    Lists All Files And Folders With Metadata In A Tree-Like Structure
    Respects .gitignore Patterns

    Args:
        folder_path (str | None): The Path To The Folder To List, Defaults To Current Directory

    Returns:
        dict[str, Any]: A Dictionary Containing The Tree Structure With Metadata

    Raises:
        ValueError: If The Folder Path Does Not Exist
    """

    # If No Folder Path Is Provided
    if folder_path is None:
        # Use The Current Directory
        folder_path = Path.cwd()

    # Convert To Absolute Path If Relative
    abs_path: Path = Path(folder_path).resolve()

    # If The Folder Path Does Not Exist
    if not abs_path.exists():
        # Raise A ValueError
        msg: str = f"Folder Path Does Not Exist: {abs_path}"

        # Raise A ValueError
        raise ValueError(msg)

    # Check If The Path Is A Directory
    if not abs_path.is_dir():
        # Raise A ValueError
        msg: str = f"Path Is Not A Directory: {abs_path}"

        # Raise A ValueError
        raise ValueError(msg)

    # Find Project Root (Directory Containing .git)
    project_root: Path = _find_project_root(abs_path)

    # Load Gitignore Patterns
    gitignore_patterns: list[Pattern] = _load_gitignore_patterns(project_root)

    # Create The Root Node
    root: dict[str, Any] = _create_node(abs_path)

    # Recursively Build The Tree
    _build_tree(root, project_root, gitignore_patterns)

    # Return The Root Node
    return root


# Helper Function To Create A Node With Metadata
def _create_node(path: str) -> dict[str, Any]:
    """
    Creates A Node With Metadata For A File Or Folder

    Args:
        path (str): The Path To The File Or Folder

    Returns:
        dict[str, Any]: A Dictionary Containing The Node Information
    """

    # Get File Stats
    stats: stat_result = Path.stat(path)

    # Get File Type
    file_type: str = "directory" if Path.is_dir(path) else "file"

    # Get File Size
    size: int = stats.st_size

    # Get Last Modified Time
    modified_time: str = datetime.fromtimestamp(
        timestamp=stats.st_mtime,
        tz=tz.tzlocal(),
    ).strftime("%Y-%m-%d %H:%M:%S")

    # Get Last Access Time
    access_time: str = datetime.fromtimestamp(
        timestamp=stats.st_atime,
        tz=tz.tzlocal(),
    ).strftime("%Y-%m-%d %H:%M:%S")

    # Get File Permissions
    permissions: str = _get_permissions(stats.st_mode)

    # Create & Return The Node
    return {
        "name": Path(path).name,
        "path": path,
        "type": file_type,
        "size": size,
        "size_human": format_size(size),
        "modified_time": modified_time,
        "access_time": access_time,
        "permissions": permissions,
        "children": [] if file_type == "directory" else None,
    }


# Helper Function To Build The Tree Recursively
def _build_tree(node: dict[str, Any], project_root: Path, gitignore_patterns: list[Pattern]) -> None:
    """
    Builds The Tree Structure Recursively

    Args:
        node (dict[str, Any]): The Current Node
        project_root (Path): The Root Directory Of The Project
        gitignore_patterns (list[Pattern]): List Of Compiled Gitignore Patterns
    """

    # If The Node Is Not A Directory
    if node["type"] != "directory":
        # Return
        return

    # Get The Path
    path: Path = Path(node["path"])

    try:
        # Get All Items In The Directory
        items: list[Path] = list(path.iterdir())

        # Sort Items (Directories First, Then Files)
        items.sort(key=lambda x: (0 if x.is_dir() else 1, x.name.lower()))

        # Process Each Item
        for item in items:
            # If The Item Is Hidden
            if item.name.startswith(".") and item.name != ".gitignore":
                # Skip
                continue

            # Get Relative Path From Project Root
            rel_path: str = os.path.relpath(item, project_root)

            # Check If The Item Is Ignored By Gitignore
            if _is_ignored(rel_path, gitignore_patterns) and item.name != ".gitignore":
                # Skip
                continue

            # Create A Child Node
            child: dict[str, Any] = _create_node(item)

            # Add The Child To The Current Node
            node["children"].append(child)

            # Recursively Build The Tree For The Child
            _build_tree(child, project_root, gitignore_patterns)

    except (PermissionError, OSError):
        # Handle Permission Errors
        node["children"] = []
        node["error"] = "Permission Denied"


# Helper Function To Get File Permissions
def _get_permissions(mode: int) -> str:
    """
    Gets The File Permissions In A Human-Readable Format

    Args:
        mode (int): The File Mode

    Returns:
        str: The File Permissions
    """

    # Initialize Permission String
    perms: str = ""

    # If The Mode Is A Directory
    if stat.S_ISDIR(mode):
        # Add Directory Permission
        perms += "d"

    # If The Mode Is A Link
    elif stat.S_ISLNK(mode):
        # Add Link Permission
        perms += "l"

    else:
        # Add File Permission
        perms += "-"

    # Add User Permissions
    perms += "r" if mode & stat.S_IRUSR else "-"
    perms += "w" if mode & stat.S_IWUSR else "-"
    perms += "x" if mode & stat.S_IXUSR else "-"

    # Add Group Permissions
    perms += "r" if mode & stat.S_IRGRP else "-"
    perms += "w" if mode & stat.S_IWGRP else "-"
    perms += "x" if mode & stat.S_IXGRP else "-"

    # Add Other Permissions
    perms += "r" if mode & stat.S_IROTH else "-"
    perms += "w" if mode & stat.S_IWOTH else "-"
    perms += "x" if mode & stat.S_IXOTH else "-"

    # Return Permission String
    return perms


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
def _load_gitignore_patterns(project_root: Path) -> list[Pattern]:
    """
    Loads And Compiles Gitignore Patterns

    Args:
        project_root (Path): The Project Root Directory

    Returns:
        list[Pattern]: List Of Compiled Gitignore Patterns
    """

    # Initialize Patterns List
    patterns: list[Pattern] = []

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
                regex: Pattern = re.compile(pattern)

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
    if is_negation:
        # Remove The Negation
        pattern: str = pattern[1:]

    # If The Pattern Is A Directory-Only Pattern
    is_dir_only: bool = pattern.endswith("/")
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
def _is_ignored(path: str, patterns: list[Pattern]) -> bool:
    """
    Checks If A Path Is Ignored By Gitignore Patterns

    Args:
        path (str): The Path To Check
        patterns (list[Pattern]): List Of Compiled Gitignore Patterns

    Returns:
        bool: True If The Path Is Ignored, False Otherwise
    """

    # Normalize Path
    path: str = path.replace("\\", "/")

    # Check Each Pattern And Return True If Any Pattern Matches
    return any(pattern.search(path) for pattern in patterns)


# Exports
__all__: list[str] = ["list_files"]
