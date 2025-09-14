# Standard Library Imports
import os
import tempfile
from pathlib import Path

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.read_file import file_exists
from zenith.agent.tools.read_file import read_file


# Test Read File Function
def test_read_file() -> None:
    """
    Tests The Read File Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        # Read The File
        result = read_file(test_file)

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_file).resolve())
        assert result["content"] == "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        assert result["line_count"] == 5
        assert result["selected_line_count"] == 5
        assert result["encoding"] == "utf-8"
        assert result["size"] == os.path.getsize(test_file)


# Test Read File With Line Range
def test_read_file_line_range() -> None:
    """
    Tests The Read File Function With Line Range
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        # Read The File With Line Range
        result = read_file(test_file, start_line=2, end_line=4)

        # Check The Result
        assert result["success"] is True
        assert result["content"] == "Line 2\nLine 3\nLine 4\n"
        assert result["line_count"] == 5
        assert result["selected_line_count"] == 3


# Test Read File With Start Line Only
def test_read_file_start_line() -> None:
    """
    Tests The Read File Function With Start Line Only
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        # Read The File With Start Line Only
        result = read_file(test_file, start_line=3)

        # Check The Result
        assert result["success"] is True
        assert result["content"] == "Line 3\nLine 4\nLine 5"
        assert result["line_count"] == 5
        assert result["selected_line_count"] == 3


# Test Read File With End Line Only
def test_read_file_end_line() -> None:
    """
    Tests The Read File Function With End Line Only
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        # Read The File With End Line Only
        result = read_file(test_file, end_line=3)

        # Check The Result
        assert result["success"] is True
        assert result["content"] == "Line 1\nLine 2\nLine 3\n"
        assert result["line_count"] == 5
        assert result["selected_line_count"] == 3


# Test Read File With Invalid Line Range
def test_read_file_invalid_line_range() -> None:
    """
    Tests The Read File Function With Invalid Line Range
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Read File With Invalid Line Range
            read_file(test_file, start_line=4, end_line=2)

        # Check The Error Message
        assert "Invalid Line Range" in str(excinfo.value)


# Test Read File With Non-Existent File
def test_read_file_non_existent() -> None:
    """
    Tests The Read File Function With A Non-Existent File
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Non-Existent File Path
        non_existent_file = os.path.join(temp_dir, "non_existent.txt")

        # With FileNotFoundError
        with pytest.raises(FileNotFoundError) as excinfo:
            # Call Read File With The Non-Existent File Path
            read_file(non_existent_file)

        # Check The Error Message
        assert "File Not Found" in str(excinfo.value)


# Test Read File With Directory Path
def test_read_file_directory() -> None:
    """
    Tests The Read File Function With A Directory Path
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Read File With The Directory Path
            read_file(temp_dir)

        # Check The Error Message
        assert "Path Is Not A File" in str(excinfo.value)


# Test Read File With Permission Error
def test_read_file_permission_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Read File Function With A Permission Error

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock open Function That Raises PermissionError
    def mock_open(*args: object, **kwargs: object) -> None:
        """
        Mock open Function That Raises PermissionError
        """

        # Raise The PermissionError
        raise PermissionError("Permission denied")

    # Patch Path.open
    monkeypatch.setattr(Path, "open", mock_open)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "permission_error.txt")

        # Create The File (Using os.open To Bypass The Patched Path.open)
        with open(test_file, "w") as f:
            # Write The Test File Content
            f.write("Test content")

        # With PermissionError
        with pytest.raises(PermissionError) as excinfo:
            # Call Read File With The Test File Path
            read_file(test_file)

        # Check The Error Message
        assert "Permission Denied" in str(excinfo.value)


# Test Read File With Encoding Error
def test_read_file_encoding_error() -> None:
    """
    Tests The Read File Function With An Encoding Error
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error.txt")

        # With Test File (Write Binary Data)
        with open(test_file, "wb") as f:
            # Write Invalid UTF-8 Bytes
            f.write(b"\xFF\xFE\xFF\xFE")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Read File With The Test File Path
            read_file(test_file, encoding="utf-8")

        # Check The Error Message
        assert "Failed To Decode File With Encoding" in str(excinfo.value)


# Test Read File With Generic Exception
def test_read_file_generic_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Read File Function With A Generic Exception

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock Open Method That Raises A Generic Exception
    class MockFile:
        """
        Mock File Class
        """

        # Constructor
        def __init__(self, *args: object, **kwargs: object) -> None:
            """
            Constructor
            """

            # Pass
            pass

        # Mock __enter__ Method
        def __enter__(self) -> "MockFile":
            """
            Mock __enter__ Method
            """

            # Return Self
            return self

        # Mock __exit__ Method
        def __exit__(self, *args: object) -> None:
            """
            Mock __exit__ Method
            """

            # Pass
            pass

        # Mock readlines Method
        def readlines(self) -> list[str]:
            """
            Mock readlines Method That Raises A Generic Exception
            """

            # Raise The Generic Exception
            raise RuntimeError("Generic error")

        # Mock read Method
        def read(self) -> str:
            """
            Mock read Method That Raises A Generic Exception
            """

            # Raise The Generic Exception
            raise RuntimeError("Generic error")

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write The Test File Content
            f.write("Line 1\nLine 2\nLine 3")

        # Patch The Path.open Method
        monkeypatch.setattr(Path, "open", lambda *args, **kwargs: MockFile())

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Read File
            read_file(test_file, start_line=1)

        # Check The Error Message
        assert "Failed To Read File" in str(excinfo.value)
        assert "Generic error" in str(excinfo.value)


# Test Format Size Function
def test_format_size() -> None:
    """
    Tests The Format Size Function
    """

    # Import The Function Directly
    from zenith.agent.tools.read_file import _format_size

    # Test Bytes
    assert _format_size(500) == "500.00 B"

    # Test Kilobytes
    assert _format_size(1500) == "1.46 KB"

    # Test Megabytes
    assert _format_size(1500000) == "1.43 MB"

    # Test Gigabytes
    assert _format_size(1500000000) == "1.40 GB"

    # Test Terabytes
    assert _format_size(1500000000000) == "1.36 TB"


# Test File Exists Function
def test_file_exists() -> None:
    """
    Tests The File Exists Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w") as f:
            # Write The Test File Content
            f.write("Test content")

        # Check That The File Exists
        assert file_exists(test_file) is True

        # Create A Non-Existent File Path
        non_existent_file = os.path.join(temp_dir, "non_existent.txt")

        # Check That The File Does Not Exist
        assert file_exists(non_existent_file) is False

        # Check That The Directory Is Not Considered A File
        assert file_exists(temp_dir) is False
