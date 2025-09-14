# Standard Library Imports
import os
import re
import tempfile
from pathlib import Path
from re import Pattern
from typing import Generator

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.search_files import _find_project_root
from zenith.agent.tools.search_files import _format_size
from zenith.agent.tools.search_files import _gitignore_to_regex
from zenith.agent.tools.search_files import _is_ignored
from zenith.agent.tools.search_files import _load_gitignore_patterns
from zenith.agent.tools.search_files import _process_file
from zenith.agent.tools.search_files import _should_skip_directory
from zenith.agent.tools.search_files import search_files
from zenith.agent.tools.search_files import _search_directory


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

        # Create Files For Search Testing
        docs_dir = temp_path / "docs"
        docs_dir.mkdir(exist_ok=True)

        # Create Various File Types For Testing
        with open(docs_dir / "readme.md", "w") as f:
            f.write("# Project Documentation")

        with open(docs_dir / "api_reference.md", "w") as f:
            f.write("# API Reference")

        with open(docs_dir / "tutorial.md", "w") as f:
            f.write("# Tutorial")

        with open(docs_dir / "config.json", "w") as f:
            f.write('{"setting": "value"}')

        # Create Hidden Files
        with open(docs_dir / ".hidden_doc.md", "w") as f:
            f.write("# Hidden Documentation")

        # Yield The Path To The Mock Project
        yield temp_path


# Test The Main Search Files Function
def test_search_files(mock_project: Path) -> None:
    """
    Tests The Main Search Files Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Test Basic Search
    results = search_files("main", mock_project)

    # Check The Results
    assert len(results) > 0
    assert any(result["name"] == "main.py" for result in results)

    # Test Search With File Type Filter
    results = search_files("main", mock_project, file_types=["py"])

    # Check The Results
    assert len(results) > 0
    assert all(Path(result["path"]).suffix == ".py" for result in results)

    # Test Case Sensitivity
    results_case_sensitive = search_files("README", mock_project, case_sensitive=True)
    results_case_insensitive = search_files("readme", mock_project, case_sensitive=False)

    # Check The Results
    assert len(results_case_sensitive) == 0
    assert len(results_case_insensitive) > 0


# Test Search Files With Hidden Files
def test_search_files_hidden(mock_project: Path) -> None:
    """
    Tests The Search Files Function With Hidden Files

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Test Without Including Hidden Files
    results = search_files("hidden", mock_project, include_hidden=False)

    # Check The Results
    assert len(results) == 0

    # Test With Including Hidden Files
    results = search_files("hidden", mock_project, include_hidden=True)

    # Check The Results
    assert len(results) > 0
    assert any(result["name"] == ".hidden_doc.md" for result in results)


# Test Search Files With Gitignore
def test_search_files_gitignore(mock_project: Path) -> None:
    """
    Tests The Search Files Function With Gitignore Patterns

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Test With Respecting Gitignore
    results = search_files("secret", mock_project, respect_gitignore=True)

    # Check The Results
    assert len(results) == 0  # secret.txt should be ignored

    # Test Without Respecting Gitignore
    results = search_files("secret", mock_project, respect_gitignore=False)

    # Check The Results
    assert len(results) > 0
    assert any(result["name"] == "secret.txt" for result in results)


# Test Search Files With Max Results
def test_search_files_max_results(mock_project: Path) -> None:
    """
    Tests The Search Files Function With Max Results Limit

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create Additional Files For Testing
    for i in range(10):
        with open(mock_project / f"test_file_{i}.txt", "w") as f:
            f.write(f"Test file {i}")

    # Test With Max Results
    results = search_files("test", mock_project, max_results=5)

    # Check The Results
    assert len(results) <= 5


# Test Search Files With Non-Existent Directory
def test_search_files_non_existent_directory() -> None:
    """
    Tests The Search Files Function With A Non-Existent Directory
    """

    # Check That A ValueError Is Raised
    with pytest.raises(ValueError) as excinfo:
        search_files("test", "non_existent_directory")

    # Check The Error Message
    assert "Directory Does Not Exist" in str(excinfo.value)


# Test Search Files With Default Directory
def test_search_files_default_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Search Files Function With Default Directory

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Create A Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert To Path
        temp_path = Path(temp_dir)

        # With Test File
        with open(temp_path / "test_file.txt", "w") as f:
            # Write The Test File Content
            f.write("Test Content")

        # Mock Path.cwd To Return Our Temp Directory
        monkeypatch.setattr(Path, "cwd", lambda: temp_path)

        # Call Search Files With No Directory
        results = search_files("test", None)

        # Check Results
        assert len(results) > 0
        assert any(result["name"] == "test_file.txt" for result in results)


# Test Search Files With File Path
def test_search_files_file_path(mock_project: Path) -> None:
    """
    Tests The Search Files Function With A File Path

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Create A File Path
    file_path = mock_project / "src" / "main.py"

    # With ValueError
    with pytest.raises(ValueError) as excinfo:
        # Call Search Files With The File Path
        search_files("test", file_path)

    # Check The Error Message
    assert "Path Is Not A Directory" in str(excinfo.value)


# Test Process File Function
def test_process_file(mock_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Process File Function

    Args:
        mock_project (Path): The Path To The Mock Project
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Create A Mock DirEntry
    class MockDirEntry:
        """
        Mock DirEntry Class

        Attributes:
            path (str): The Path To The File
            name (str): The Name Of The File

        Methods:
            is_file(self) -> bool: Returns True If The Item Is A File
            is_dir(self) -> bool: Returns True If The Item Is A Directory
        """

        # Constructor
        def __init__(self, path: str, name: str):
            """
            Constructor

            Args:
                path (str): The Path To The File
                name (str): The Name Of The File
            """

            # Initialize The Attributes
            #
            self.path = path
            self.name = name

        # Method To Check If The Item Is A File
        def is_file(self) -> bool:
            """
            Returns True If The Item Is A File
            """

            # Return True
            return True

        # Method To Check If The Item Is A Directory
        def is_dir(self) -> bool:
            """
            Returns True If The Item Is A Directory
            """

            # Return False
            return False

    # Create A Test File
    test_file = mock_project / "test_file.txt"

    # With Test File
    with open(test_file, "w") as f:
        # Write The Test File Content
        f.write("Test Content")

    # Create A Mock DirEntry
    mock_entry = MockDirEntry(str(test_file), "test_file.txt")

    # Test With Matching Pattern
    result = _process_file(
        item=mock_entry,
        search_pattern="test",
        case_sensitive=False,
        file_types=None,
        respect_gitignore=False,
        project_root=mock_project,
        gitignore_patterns=[],
    )

    # Check The Result
    assert result is not None
    assert result["name"] == "test_file.txt"
    assert result["path"] == str(test_file)

    # Test With Non-Matching Pattern
    result = _process_file(
        item=mock_entry,
        search_pattern="xyz",
        case_sensitive=False,
        file_types=None,
        respect_gitignore=False,
        project_root=mock_project,
        gitignore_patterns=[],
    )

    # Check The Result
    assert result is None

    # Test With File Type Filter
    result = _process_file(
        item=mock_entry,
        search_pattern="test",
        case_sensitive=False,
        file_types=["py"],
        respect_gitignore=False,
        project_root=mock_project,
        gitignore_patterns=[],
    )

    # Check The Result
    assert result is None


# Test Should Skip Directory Function
def test_should_skip_directory(mock_project: Path) -> None:
    """
    Tests The Should Skip Directory Function

    Args:
        mock_project (Path): The Path To The Mock Project
    """

    # Load Gitignore Patterns
    gitignore_patterns = _load_gitignore_patterns(mock_project)

    # Test With Directory That Should Be Skipped
    node_modules_dir = mock_project / "node_modules"
    should_skip = _should_skip_directory(
        path=node_modules_dir,
        respect_gitignore=True,
        project_root=mock_project,
        gitignore_patterns=gitignore_patterns,
    )

    # Check The Result
    assert should_skip is True

    # Test With Directory That Should Not Be Skipped
    src_dir = mock_project / "src"
    should_skip = _should_skip_directory(
        path=src_dir,
        respect_gitignore=True,
        project_root=mock_project,
        gitignore_patterns=gitignore_patterns,
    )

    # Check The Result
    assert should_skip is False

    # Test With Respect Gitignore Set To False
    should_skip = _should_skip_directory(
        path=node_modules_dir,
        respect_gitignore=False,
        project_root=mock_project,
        gitignore_patterns=gitignore_patterns,
    )

    # Check The Result
    assert should_skip is False


# Test Format Size Function
def test_format_size() -> None:
    """
    Tests The Format Size Helper Function
    """

    # Test With Various Sizes
    assert _format_size(0) == "0.00 B"
    assert _format_size(1023) == "1023.00 B"
    assert _format_size(1024) == "1.00 KB"
    assert _format_size(1024 * 1024) == "1.00 MB"
    assert _format_size(1024 * 1024 * 1024) == "1.00 GB"
    assert _format_size(1024 * 1024 * 1024 * 1024) == "1.00 TB"


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
    assert _is_ignored("test\\file.txt", patterns) is True


# Test Exception Handling In Search Directory
def test_search_directory_exceptions(mock_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests Exception Handling In The Search Directory Function

    Args:
        mock_project (Path): The Path To The Mock Project
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Test Permission Error In scandir
    def mock_scandir_permission_error(_):
        """
        Mock Function That Raises PermissionError
        """
        raise PermissionError("Permission denied")

    # Patch os.scandir To Raise PermissionError
    monkeypatch.setattr(os, "scandir", mock_scandir_permission_error)

    # Call _search_directory (Should Handle The Exception Gracefully)
    results = _search_directory(
        directory=mock_project,
        search_pattern="test",
        case_sensitive=False,
        file_types=None,
        include_hidden=False,
        gitignore_patterns=[],
        respect_gitignore=False,
        project_root=mock_project,
        max_results=100,
    )

    # Check That An Empty List Is Returned
    assert results == []

    # Reset The Monkeypatch
    monkeypatch.undo()

    # Create A Mock DirEntry That Raises An Exception
    class ExceptionRaisingDirEntry:
        """
        Mock DirEntry Class That Raises Exceptions

        Attributes:
            path (str): The Path To The File
            name (str): The Name Of The File
        """

        def __init__(self, path: str, name: str):
            """
            Constructor

            Args:
                path (str): The Path To The File
                name (str): The Name Of The File
            """
            self.path = path
            self.name = name

        def is_dir(self) -> bool:
            """
            Raises PermissionError When Called
            """
            raise PermissionError("Permission denied")

        def is_file(self) -> bool:
            """
            Raises PermissionError When Called
            """
            raise PermissionError("Permission denied")

    # Create A Mock scandir Function
    def mock_scandir_with_exception_entry(_):
        """
        Mock Function That Returns A List With An Exception-Raising Entry
        """
        return [ExceptionRaisingDirEntry(str(mock_project / "problem_file.txt"), "problem_file.txt")]

    # Patch os.scandir To Return Our Mock Entry
    monkeypatch.setattr(os, "scandir", mock_scandir_with_exception_entry)

    # Call _search_directory (Should Handle The Exception Gracefully)
    results = _search_directory(
        directory=mock_project,
        search_pattern="test",
        case_sensitive=False,
        file_types=None,
        include_hidden=False,
        gitignore_patterns=[],
        respect_gitignore=False,
        project_root=mock_project,
        max_results=100,
    )

    # Check That An Empty List Is Returned
    assert results == []
