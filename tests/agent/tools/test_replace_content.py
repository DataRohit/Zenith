# Standard Library Imports
import os
import tempfile
from pathlib import Path
from typing import Any

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.replace_content import replace_content


# Test Replace Content Function
def test_replace_content() -> None:
    """
    Tests The Replace Content Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("Hello World\nHello Python\nHello Java")

        # Replace Content
        result = replace_content(test_file, "World", "Zenith")

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_file).resolve())
        assert result["encoding"] == "utf-8"
        assert result["replaced"] is True
        assert result["size"] == os.path.getsize(test_file)

        # With Open
        with open(test_file, "r", encoding="utf-8") as f:
            # Read The File Content
            content = f.read()

            # Check The File Content
            assert content == "Hello Zenith\nHello Python\nHello Java"


# Test Replace Content With Multiple Occurrences (Only First Should Be Replaced)
def test_replace_content_multiple_occurrences() -> None:
    """
    Tests The Replace Content Function With Multiple Occurrences
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("apple apple banana")

        # Replace The First Occurrence
        result = replace_content(test_file, "apple", "orange")

        # Check The Result
        assert result["success"] is True

        # With Open
        with open(test_file, "r", encoding="utf-8") as f:
            # Read The File Content
            content = f.read()

            # Check The File Content
            assert content == "orange apple banana"


# Test Replace Content With Non-Existent File
def test_replace_content_non_existent_file() -> None:
    """
    Tests The Replace Content Function With A Non-Existent File
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Non-Existent File Path
        non_existent_file = os.path.join(temp_dir, "non_existent.txt")

        # With FileNotFoundError
        with pytest.raises(FileNotFoundError) as excinfo:
            # Call Replace Content
            replace_content(non_existent_file, "old", "new")

        # Check The Error Message
        assert "File Not Found" in str(excinfo.value)


# Test Replace Content With Directory Path
def test_replace_content_directory_path() -> None:
    """
    Tests The Replace Content Function With A Directory Path
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content
            replace_content(temp_dir, "old", "new")

        # Check The Error Message
        assert "Path Is Not A File" in str(excinfo.value)


# Test Replace Content When Old Content Is Not Found
def test_replace_content_old_content_not_found() -> None:
    """
    Tests The Replace Content Function When Old Content Is Not Found
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("some content")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content With Non-Existent Old Content
            replace_content(test_file, "non_existent", "new")

        # Check The Error Message
        assert "Old Content Not Found In File" in str(excinfo.value)


# Test Replace Content With Permission Error On Read
def test_replace_content_permission_error_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Permission Error On Read
    """

    # Define A Mock read_text Function That Raises PermissionError
    def mock_read_text(*args: object, **kwargs: object) -> str:
        """
        Mock read_text Function That Raises PermissionError
        """

        # Raise The PermissionError
        raise PermissionError("Permission denied")

    # Patch Path.read_text
    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "permission_error_read.txt")

        # Create The File
        Path(test_file).touch()

        # With PermissionError
        with pytest.raises(PermissionError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "old", "new")

        # Check The Error Message
        assert "Permission Denied" in str(excinfo.value)


# Test Replace Content With Permission Error On Write
def test_replace_content_permission_error_write(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Permission Error On Write
    """

    # Define A Mock write_text Function That Raises PermissionError
    def mock_write_text(*args: object, **kwargs: object) -> Any:
        """
        Mock write_text Function That Raises PermissionError
        """

        # Raise The PermissionError
        raise PermissionError("Permission denied")

    # Patch Path.write_text
    monkeypatch.setattr(Path, "write_text", mock_write_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "permission_error_write.txt")

        # With Open
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("original content")

        # With PermissionError
        with pytest.raises(PermissionError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "original", "new")

        # Check The Error Message
        assert "Permission Denied" in str(excinfo.value)


# Test Replace Content With Encoding Error On Read
def test_replace_content_encoding_error_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Encoding Error On Read
    """

    # Define A Mock read_text Function That Raises UnicodeDecodeError
    def mock_read_text(*args: object, **kwargs: object) -> str:
        """
        Mock read_text Function That Raises UnicodeDecodeError
        """

        # Raise The UnicodeDecodeError
        raise UnicodeDecodeError("utf-8", b"test", 0, 1, "Invalid byte")

    # Patch Path.read_text
    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error_read.txt")

        # Create The File
        Path(test_file).touch()

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "old", "new")

        # Check The Error Message
        assert "Failed To Decode File With Encoding" in str(excinfo.value)


# Test Replace Content With Encoding Error On Write
def test_replace_content_encoding_error_write(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Encoding Error On Write
    """

    # Define A Mock write_text Function That Raises UnicodeEncodeError
    def mock_write_text(*args: object, **kwargs: object) -> Any:
        """
        Mock write_text Function That Raises UnicodeEncodeError
        """

        # Raise The UnicodeEncodeError
        raise UnicodeEncodeError("utf-8", "test", 0, 1, "Invalid character")

    # Patch Path.write_text
    monkeypatch.setattr(Path, "write_text", mock_write_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error_write.txt")

        # With Open
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("original content")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "original", "new")

        # Check The Error Message
        assert "Failed To Encode Content With Encoding" in str(excinfo.value)


# Test Replace Content With Generic Exception On Read
def test_replace_content_generic_exception_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Generic Exception On Read
    """

    # Define A Mock read_text Function That Raises A Generic Exception
    def mock_read_text(*args: object, **kwargs: object) -> str:
        """
        Mock read_text Function That Raises A Generic Exception
        """

        # Raise The Generic Exception
        raise RuntimeError("Generic error")

    # Patch Path.read_text
    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "generic_error_read.txt")

        # Create The File
        Path(test_file).touch()

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "old", "new")

        # Check The Error Message
        assert "Failed To Replace Content In File" in str(excinfo.value)
        assert "Generic error" in str(excinfo.value)


# Test Replace Content With Generic Exception On Write
def test_replace_content_generic_exception_write(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Replace Content Function With Generic Exception On Write
    """

    # Define A Mock write_text Function That Raises A Generic Exception
    def mock_write_text(*args: object, **kwargs: object) -> Any:
        """
        Mock write_text Function That Raises A Generic Exception
        """

        # Raise The Generic Exception
        raise RuntimeError("Generic error")

    # Patch Path.write_text
    monkeypatch.setattr(Path, "write_text", mock_write_text)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "generic_error_write.txt")

        # With Open
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("original content")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Replace Content
            replace_content(test_file, "original", "new")

        # Check The Error Message
        assert "Failed To Replace Content In File" in str(excinfo.value)
        assert "Generic error" in str(excinfo.value)
