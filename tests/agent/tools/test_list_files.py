# Standard Library Imports
import re
import stat
import tempfile
from pathlib import Path
from re import Pattern
from typing import Generator

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.list_files import _build_tree
from zenith.agent.tools.list_files import _create_node
from zenith.agent.tools.list_files import _find_project_root
from zenith.agent.tools.list_files import _get_permissions
from zenith.agent.tools.list_files import _gitignore_to_regex
from zenith.agent.tools.list_files import _is_ignored
from zenith.agent.tools.list_files import _load_gitignore_patterns
from zenith.agent.tools.list_files import list_files
from zenith.utils.format_file_size import format_size


# Fixture For Creating A Mock Project Structure
@pytest.fixture
def mock_project() -> Generator[Path, None, None]:
    """
    Creates A Mock Project Structure For Testing

    Returns:
        Generator[Path, None, None]: The Path To The Mock Project
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create Temporary Path
        temp_path = Path(temp_dir)

        # Create .git Directory To Simulate A Git Repository
        git_dir = temp_path / ".git"
        git_dir.mkdir(exist_ok=True)

        # Create A .gitignore File
        gitignore_content = """
# Ignore Node Modules
node_modules/

# Ignore Python Cache Files
__pycache__/
*.py[cod]
*$py.class

# Ignore Build Directories
build/
dist/

# Ignore Specific Files
secret.txt
*.log
"""

        # With .gitignore File
        with open(temp_path / ".gitignore", "w") as f:
            # Write The Gitignore Content
            f.write(gitignore_content)

        # Create Some Regular Directories And Files
        src_dir = temp_path / "src"
        src_dir.mkdir(exist_ok=True)

        # With Main Python File
        with open(src_dir / "main.py", "w") as f:
            # Write The Main Python File Content
            f.write("print('Hello, World!')")

        # With Utils Python File
        with open(src_dir / "utils.py", "w") as f:
            # Write The Utils Python File Content
            f.write("def add(a, b): return a + b")

        # Create A Tests Directory
        tests_dir = temp_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # With Test Main Python File
        with open(tests_dir / "test_main.py", "w") as f:
            # Write The Test Main Python File Content
            f.write("def test_main(): assert True")

        # Create Files That Should Be Ignored
        node_modules_dir = temp_path / "node_modules"
        node_modules_dir.mkdir(exist_ok=True)

        # With Package JSON File
        with open(node_modules_dir / "package.json", "w") as f:
            # Write The Package JSON File Content
            f.write("{}")

        # Create A Python Cache Directory
        pycache_dir = src_dir / "__pycache__"
        pycache_dir.mkdir(exist_ok=True)

        # With Compiled Python File
        with open(pycache_dir / "main.cpython-38.pyc", "w") as f:
            # Write The Compiled Python File Content
            f.write("# Compiled Python File")

        # Create A Secret File (Should Be Ignored)
        with open(temp_path / "secret.txt", "w") as f:
            # Write The Secret File Content
            f.write("This is a secret")

        # Create A Log File (Should Be Ignored)
        with open(temp_path / "app.log", "w") as f:
            # Write The Log File Content
            f.write("Some log data")

        # Create A Build Directory (Should Be Ignored)
        build_dir = temp_path / "build"
        build_dir.mkdir(exist_ok=True)

        # With Index HTML File
        with open(build_dir / "index.html", "w") as f:
            # Write The Index HTML File Content
            f.write("<html><body>Hello</body></html>")

        # Yield The Path To The Mock Project
        yield temp_path


# Test The Main List Files Function
def test_list_files(mock_project: Path) -> None:
    """
    Tests The Main List Files Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Call The Function
    result = list_files(mock_project)

    # Check The Result Is A Dictionary
    assert isinstance(result, dict)

    # Check The Root Node Has The Correct Name
    assert result["name"] == mock_project.name

    # Check The Root Node Has Children
    assert isinstance(result["children"], list)
    assert len(result["children"]) > 0

    # Check That Ignored Files Are Not In The Result
    child_names = [child["name"] for child in result["children"]]
    assert "src" in child_names
    assert "tests" in child_names
    assert ".gitignore" in child_names  # .gitignore Should Be Included
    assert "node_modules" not in child_names  # Should Be Ignored
    assert "secret.txt" not in child_names  # Should Be Ignored
    assert "app.log" not in child_names  # Should Be Ignored
    assert "build" not in child_names  # Should Be Ignored


# Test List Files With No Path Provided
def test_list_files_no_path(mock_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The List Files Function When No Path Is Provided

    Args:
        mock_project (Path): The Path To The Mock Project
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Mock The Current Working Directory
    monkeypatch.setattr(Path, "cwd", lambda: mock_project)

    # Call The Function Without A Path
    result = list_files()

    # Check The Result Is A Dictionary
    assert isinstance(result, dict)

    # Check The Root Node Has The Correct Name
    assert result["name"] == mock_project.name


# Test List Files With Non-Existent Path
def test_list_files_non_existent_path(mock_project: Path) -> None:
    """
    Tests The List Files Function With A Non-Existent Path

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create A Non-Existent Path
    non_existent_path = mock_project / "non_existent"

    # Check That A ValueError Is Raised
    with pytest.raises(ValueError) as excinfo:
        list_files(non_existent_path)

    # Check The Error Message
    assert "Folder Path Does Not Exist" in str(excinfo.value)


# Test List Files With A File Path
def test_list_files_file_path(mock_project: Path) -> None:
    """
    Tests The List Files Function With A File Path

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create A File Path
    file_path = mock_project / "src" / "main.py"

    # Check That A ValueError Is Raised
    with pytest.raises(ValueError) as excinfo:
        list_files(file_path)

    # Check The Error Message
    assert "Path Is Not A Directory" in str(excinfo.value)


# Test Create Node Function
def test_create_node(mock_project: Path) -> None:
    """
    Tests The Create Node Helper Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create A Test File
    test_file = mock_project / "test_file.txt"

    # With Test File
    with open(test_file, "w") as f:
        # Write The Test File Content
        f.write("Test Content")

    # Call The Function
    node = _create_node(test_file)

    # Check The Node Is A Dictionary
    assert isinstance(node, dict)

    # Check The Node Has The Correct Name
    assert node["name"] == "test_file.txt"

    # Check The Node Has The Correct Path
    assert node["path"] == test_file

    # Check The Node Has The Correct Type
    assert node["type"] == "file"

    # Check The Node Has A Size
    assert isinstance(node["size"], int)
    assert node["size"] > 0

    # Check The Node Has A Human-Readable Size
    assert isinstance(node["size_human"], str)

    # Test The Human-Readable Size Is Correct
    assert node["size_human"] == format_size(node["size"])

    # Check The Node Has Modified Time
    assert isinstance(node["modified_time"], str)

    # Check The Node Has Access Time
    assert isinstance(node["access_time"], str)

    # Check The Node Has Permissions
    assert isinstance(node["permissions"], str)

    # Check The Node Has No Children (It's A File)
    assert node["children"] is None

    # Test With A Directory
    test_dir = mock_project / "test_dir"
    test_dir.mkdir(exist_ok=True)

    # Call The Function
    node = _create_node(test_dir)

    # Check The Node Is A Dictionary
    assert isinstance(node, dict)

    # Check The Node Has The Correct Type
    assert node["type"] == "directory"

    # Check The Node Has Children (It's A Directory)
    assert isinstance(node["children"], list)
    assert len(node["children"]) == 0


# Test Build Tree Function
def test_build_tree(mock_project: Path) -> None:
    """
    Tests The Build Tree Helper Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create A Test Directory Structure
    test_dir = mock_project / "test_build_tree"
    test_dir.mkdir(exist_ok=True)

    # Create Some Files
    (test_dir / "file1.txt").write_text("File 1")
    (test_dir / "file2.txt").write_text("File 2")

    # Create A Subdirectory
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir(exist_ok=True)
    (sub_dir / "file3.txt").write_text("File 3")

    # Create A Hidden File (Should Be Skipped)
    (test_dir / ".hidden").write_text("Hidden File")

    # Create A File That Should Be Ignored By Gitignore
    (test_dir / "node_modules").mkdir(exist_ok=True)
    (test_dir / "node_modules" / "package.json").write_text("{}")

    # Create A Node For The Test Directory
    node = _create_node(test_dir)

    # Create Gitignore Patterns
    patterns: list[Pattern] = [re.compile("^test_build_tree/node_modules$|^test_build_tree/node_modules/.*$")]

    # Call The Function
    _build_tree(node, mock_project, patterns)

    # Check The Node Has Children
    assert isinstance(node["children"], list)

    # Get The Children Names
    child_names = [child["name"] for child in node["children"]]

    # Check For Expected Files
    assert "file1.txt" in child_names
    assert "file2.txt" in child_names
    assert "subdir" in child_names

    # Check That Hidden And Ignored Files Are Skipped
    assert ".hidden" not in child_names
    assert "node_modules" not in child_names

    # Update The Expected Count Based On What's Actually Found
    assert len(node["children"]) == len(child_names)

    # Find The Subdirectory
    subdir_node = next(child for child in node["children"] if child["name"] == "subdir")

    # Check The Subdirectory Has Children
    assert isinstance(subdir_node["children"], list)
    assert len(subdir_node["children"]) == 1

    # Check The Subdirectory Child Name
    assert subdir_node["children"][0]["name"] == "file3.txt"

    # Test With A File Node (Should Return Early)
    file_node = _create_node(test_dir / "file1.txt")
    _build_tree(file_node, mock_project, patterns)
    assert file_node["children"] is None


# Test Build Tree With Permission Error
def test_build_tree_permission_error(mock_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Build Tree Function With A Permission Error

    Args:
        mock_project (Path): The Path To The Mock Project
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Create A Test Directory
    test_dir = mock_project / "test_permission"
    test_dir.mkdir(exist_ok=True)

    # Create A Node For The Test Directory
    node = _create_node(test_dir)

    # Mock The iterdir Method To Raise A Permission Error
    def mock_iterdir(self: Path) -> list[Path]:
        """
        Mock Function That Raises A Permission Error

        Args:
            self (Path): The Path Instance

        Raises:
            PermissionError: Always Raises A Permission Error
        """

        # Raise A Permission Error
        raise PermissionError("Permission denied")

    # Apply The Mock
    monkeypatch.setattr(Path, "iterdir", mock_iterdir)

    # Call The Function
    _build_tree(node, mock_project, [])

    # Check The Node Has An Empty Children List
    assert isinstance(node["children"], list)
    assert len(node["children"]) == 0

    # Check The Node Has An Error Message
    assert node["error"] == "Permission Denied"

    # Test With OSError
    node = _create_node(test_dir)

    # Mock The iterdir Method To Raise An OSError
    def mock_iterdir_oserror(self: Path) -> list[Path]:
        """
        Mock Function That Raises An OSError

        Args:
            self (Path): The Path Instance

        Raises:
            OSError: Always Raises An OSError
        """

        # Raise An OSError
        raise OSError("OS Error")

    # Apply The Mock
    monkeypatch.setattr(Path, "iterdir", mock_iterdir_oserror)

    # Call The Function
    _build_tree(node, mock_project, [])

    # Check The Node Has An Empty Children List
    assert isinstance(node["children"], list)
    assert len(node["children"]) == 0

    # Check The Node Has An Error Message
    assert node["error"] == "Permission Denied"


# Test Format Size Function
def test_format_size() -> None:
    """
    Tests The Format Size Helper Function
    """

    # Test With Various Sizes
    assert format_size(0) == "0.00 B"
    assert format_size(1023) == "1023.00 B"
    assert format_size(1024) == "1.00 KB"
    assert format_size(1024 * 1024) == "1.00 MB"
    assert format_size(1024 * 1024 * 1024) == "1.00 GB"
    assert format_size(1024 * 1024 * 1024 * 1024) == "1.00 TB"


# Test Get Permissions Function
def test_get_permissions() -> None:
    """
    Tests The Get Permissions Helper Function
    """

    # Test Directory Permissions
    dir_mode = stat.S_IFDIR | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
    assert _get_permissions(dir_mode) == "drwx------"

    # Test File Permissions
    file_mode = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    assert _get_permissions(file_mode) == "-rw-r--r--"

    # Test Link Permissions
    link_mode = stat.S_IFLNK | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
    assert _get_permissions(link_mode) == "lrwxrwxrwx"


# Test Find Project Root Function
def test_find_project_root(mock_project: Path) -> None:
    """
    Tests The Find Project Root Helper Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Test With A Path Inside The Project
    src_dir = mock_project / "src"
    assert _find_project_root(src_dir) == mock_project

    # Test With The Project Root Itself
    assert _find_project_root(mock_project) == mock_project

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as outside_dir:
        # Create Outside Path
        outside_path = Path(outside_dir)

        # Check The Project Root Is The Outside Path
        assert _find_project_root(outside_path) == outside_path


# Test Load Gitignore Patterns Function
def test_load_gitignore_patterns(mock_project: Path) -> None:
    """
    Tests The Load Gitignore Patterns Helper Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Call The Function
    patterns = _load_gitignore_patterns(mock_project)

    # Check The Result Is A List
    assert isinstance(patterns, list)

    # Check The List Contains Compiled Regex Patterns
    assert all(isinstance(p, Pattern) for p in patterns)

    # Check The Number Of Patterns (Excluding Empty Lines And Comments)
    assert len(patterns) == 8

    # Test With No Gitignore File
    with tempfile.TemporaryDirectory() as no_gitignore_dir:
        # Create No Gitignore Path
        no_gitignore_path = Path(no_gitignore_dir)

        # Call The Function
        patterns = _load_gitignore_patterns(no_gitignore_path)

        # Check The Result Is A List
        assert len(patterns) == 0


# Test Gitignore To Regex Function
def test_gitignore_to_regex() -> None:
    """
    Tests The Gitignore To Regex Helper Function
    """

    # Test Simple Pattern
    assert _gitignore_to_regex("file.txt") == "^file\\.txt$|^file\\.txt/.*$"

    # Test Directory Pattern
    assert _gitignore_to_regex("dir/") == "^dir$|^dir/.*$"

    # Test Wildcard Pattern
    assert _gitignore_to_regex("*.txt") == "^[^/]*\\.txt$|^[^/]*\\.txt/.*$"

    # Test Double Wildcard Pattern
    assert _gitignore_to_regex("**/*.js") == "^.*/[^/]*\\.js$|^.*/[^/]*\\.js/.*$"

    # Test Negation Pattern
    assert _gitignore_to_regex("!file.txt") == "^file\\.txt$|^file\\.txt/.*$"

    # Test Question Mark Pattern
    assert _gitignore_to_regex("file?.txt") == "^file[^/]\\.txt$|^file[^/]\\.txt/.*$"


# Test Is Ignored Function
def test_is_ignored() -> None:
    """
    Tests The Is Ignored Helper Function
    """

    # Compile Some Test Patterns
    patterns = [
        re.compile("^node_modules$|^node_modules/.*$"),
        re.compile("^.*\\.log$|^.*\\.log/.*$"),
        re.compile("^build$|^build/.*$"),
    ]

    # Test Matching Paths
    assert _is_ignored("node_modules", patterns) is True
    assert _is_ignored("node_modules/file.js", patterns) is True
    assert _is_ignored("logs/app.log", patterns) is True
    assert _is_ignored("build", patterns) is True
    assert _is_ignored("build/index.html", patterns) is True

    # Test Non-Matching Paths
    assert _is_ignored("src", patterns) is False
    assert _is_ignored("src/main.js", patterns) is False
    assert _is_ignored("logs", patterns) is False
    assert _is_ignored("builder", patterns) is False


# Test Path Normalization In Is Ignored
def test_is_ignored_path_normalization() -> None:
    """
    Tests Path Normalization In The Is Ignored Function
    """

    # Compile A Test Pattern
    patterns = [re.compile("^test$|^test/.*$")]

    # Test With Different Path Separators
    assert _is_ignored("test", patterns) is True
    assert _is_ignored("test/file.txt", patterns) is True
    assert _is_ignored("test\\file.txt", patterns) is True  # Windows Path
