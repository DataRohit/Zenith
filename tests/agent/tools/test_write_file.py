# Standard Library Imports
import os
import tempfile
from pathlib import Path

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.write_file import file_is_writable
from zenith.agent.tools.write_file import write_file
from zenith.utils.format_file_size import format_size


# Test Write File Function
def test_write_file() -> None:
    """
    Tests The Write File Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # Write The File
        result = write_file(test_file, "Test content")

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_file).resolve())
        assert result["encoding"] == "utf-8"
        assert result["append"] is False
        assert result["size"] == os.path.getsize(test_file)

        # With Open
        with open(test_file, "r", encoding="utf-8") as f:
            # Read The File Content
            content = f.read()

            # Check The File Content
            assert content == "Test content"


# Test Write File With Append
def test_write_file_append() -> None:
    """
    Tests The Write File Function With Append Mode
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Open
        with open(test_file, "w", encoding="utf-8") as f:
            # Write Initial Content
            f.write("Initial content\n")

        # Append To The File
        result = write_file(test_file, "Appended content", append=True)

        # Check The Result
        assert result["success"] is True
        assert result["append"] is True

        # With Open
        with open(test_file, "r", encoding="utf-8") as f:
            # Read The File Content
            content = f.read()

            # Check The File Content
            assert content == "Initial content\nAppended content"


# Test Write File With Create Parents
def test_write_file_create_parents() -> None:
    """
    Tests The Write File Function With Create Parents
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path With Nested Directories
        nested_dir = os.path.join(temp_dir, "nested", "directory")
        test_file = os.path.join(nested_dir, "test_file.txt")

        # Write The File With Create Parents
        result = write_file(test_file, "Test content", create_parents=True)

        # Check The Result
        assert result["success"] is True
        assert os.path.exists(nested_dir)
        assert os.path.exists(test_file)

        # With Open
        with open(test_file, "r", encoding="utf-8") as f:
            # Read The File Content
            content = f.read()

            # Check The File Content
            assert content == "Test content"


# Test Write File With Non-Existent Parent Directory
def test_write_file_non_existent_parent() -> None:
    """
    Tests The Write File Function With A Non-Existent Parent Directory
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path With Nested Directories
        nested_dir = os.path.join(temp_dir, "non_existent", "directory")
        test_file = os.path.join(nested_dir, "test_file.txt")

        # With FileNotFoundError
        with pytest.raises(FileNotFoundError) as excinfo:
            # Call Write File Without Create Parents
            write_file(test_file, "Test content")

        # Check The Error Message
        assert "Parent Directory Not Found" in str(excinfo.value)


# Test Write File With Permission Error
def test_write_file_permission_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Write File Function With A Permission Error

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

        # With PermissionError
        with pytest.raises(PermissionError) as excinfo:
            # Call Write File
            write_file(test_file, "Test content")

        # Check The Error Message
        assert "Permission Denied" in str(excinfo.value)


# Test Write File With Encoding Error
def test_write_file_encoding_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Write File Function With An Encoding Error

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock write Method That Raises UnicodeEncodeError
    def mock_write(*args: object, **kwargs: object) -> None:
        """
        Mock write Method That Raises UnicodeEncodeError
        """

        # Raise The UnicodeEncodeError
        raise UnicodeEncodeError("utf-8", b"test", 0, 1, "Invalid character")

    # Create A Mock File Context Manager
    class MockFileContextManager:
        """
        Mock File Context Manager Class
        """

        # Enter Method
        def __enter__(self) -> "MockFile":
            """
            Enter Method
            """

            # Return Mock File Object
            return MockFile()

        # Exit Method
        def __exit__(self, *args: object) -> None:
            """
            Exit Method
            """

            # Pass
            pass

    # Create A Mock File Object
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
            pass

        # Mock write Method
        def write(self, *args: object, **kwargs: object) -> None:
            """
            Mock write Method
            """

            # Raise The UnicodeEncodeError
            mock_write()

    # Patch Path.open
    monkeypatch.setattr(Path, "open", lambda *args, **kwargs: MockFileContextManager())

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error.txt")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Write File
            write_file(test_file, "Test content")

        # Check The Error Message
        error_message = str(excinfo.value)
        assert "Failed To Write File" in error_message


# Test Write File With Generic Exception
def test_write_file_generic_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Write File Function With A Generic Exception

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock write Method That Raises A Generic Exception
    def mock_write(*args: object, **kwargs: object) -> None:
        """
        Mock write Method That Raises A Generic Exception
        """

        # Raise A Generic Exception
        raise RuntimeError("Generic error")

    # Create A Mock File Object
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

        # Mock write Method
        def write(self, *args: object, **kwargs: object) -> None:
            """
            Mock write Method
            """

            # Call Mock Write
            mock_write()

    # Patch Path.open
    monkeypatch.setattr(Path, "open", lambda *args, **kwargs: MockFile())

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "generic_error.txt")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Write File
            write_file(test_file, "Test content")

        # Check The Error Message
        assert "Failed To Write File" in str(excinfo.value)
        assert "Generic error" in str(excinfo.value)


# Test File Is Writable Function
def test_file_is_writable() -> None:
    """
    Tests The File Is Writable Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(test_file, "w") as f:
            # Write The Test File Content
            f.write("Test content")

        # Check That The File Is Writable
        assert file_is_writable(test_file) is True

        # Create A Non-Existent File Path
        non_existent_file = os.path.join(temp_dir, "non_existent.txt")

        # Check That The File Is Writable (Since The Directory Is Writable)
        assert file_is_writable(non_existent_file) is True

        # Create A Non-Existent File Path With Non-Existent Parent Directory
        non_existent_dir_file = os.path.join(temp_dir, "non_existent_dir", "file.txt")

        # Check That The File Is Not Writable (Since The Parent Directory Doesn't Exist)
        assert file_is_writable(non_existent_dir_file) is False


# Test Format Size Function
def test_format_size_bytes() -> None:
    """
    Tests The Format Size Function For Bytes
    """

    # Test Bytes
    assert format_size(500) == "500.00 B"


# Test Format Size Function For Kilobytes
def test_format_size_kilobytes() -> None:
    """
    Tests The Format Size Function For Kilobytes
    """

    # Test Kilobytes
    assert format_size(1500) == "1.46 KB"


# Test Format Size Function For Megabytes
def test_format_size_megabytes() -> None:
    """
    Tests The Format Size Function For Megabytes
    """

    # Test Megabytes
    assert format_size(1500000) == "1.43 MB"


# Test Format Size Function For Gigabytes
def test_format_size_gigabytes() -> None:
    """
    Tests The Format Size Function For Gigabytes
    """

    # Test Gigabytes
    assert format_size(1500000000) == "1.40 GB"


# Test Format Size Function For Terabytes
def test_format_size_terabytes() -> None:
    """
    Tests The Format Size Function For Terabytes
    """

    # Test Terabytes
    assert format_size(1500000000000) == "1.36 TB"


# Test Format Size Function For Petabytes
def test_format_size_petabytes() -> None:
    """
    Tests The Format Size Function For Petabytes
    """

    # Test Petabytes
    assert format_size(1500000000000000) == "1.33 PB"

# Test Write File With UnicodeEncodeError
def test_write_file_unicode_encode_error() -> None:
    """
    Tests The Write File Function With UnicodeEncodeError
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error.txt")

        # Try To Write Non-ASCII Content With ASCII Encoding
        with pytest.raises(ValueError) as excinfo:
            # This Should Raise UnicodeEncodeError Which Is Caught And Wrapped In ValueError
            write_file(
                test_file,
                "Test content with non-ASCII character: \u00A9",
                encoding="ascii"
            )

        # Check The Error Message
        error_message = str(excinfo.value)
        assert "Failed To Encode Content With Encoding 'ascii'" in error_message


# Test Write File With Direct UnicodeEncodeError
def test_write_file_direct_unicode_encode_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Write File Function With A Direct UnicodeEncodeError

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test File Path
        test_file = os.path.join(temp_dir, "encoding_error.txt")

        # Define A Mock File Class With UnicodeEncodeError
        class MockFileWithUnicodeEncodeError:
            """
            Mock File Class That Raises UnicodeEncodeError On write
            """

            # Constructor
            def __init__(self, *args: object, **kwargs: object) -> None:
                """
                Constructor
                """

                # Store The Encoding
                self.encoding = kwargs.get("encoding", "utf-8")

            # Enter Method
            def __enter__(self) -> "MockFileWithUnicodeEncodeError":
                """
                Enter Method
                """

                # Return Self
                return self

            # Exit Method
            def __exit__(self, *args: object) -> None:
                """
                Exit Method
                """

                # Pass
                pass

            # Write Method That Raises UnicodeEncodeError
            def write(self, content: str) -> None:
                """
                Write Method That Raises UnicodeEncodeError
                """

                # Raise UnicodeEncodeError
                raise UnicodeEncodeError(self.encoding, b"test", 0, 1, "Invalid character")

        # Patch Path.open
        monkeypatch.setattr(Path, "open", lambda *args, **kwargs: MockFileWithUnicodeEncodeError(*args, **kwargs))

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Write File
            write_file(test_file, "Test content")

        # Check The Error Message
        error_message = str(excinfo.value)
        assert "Failed To Write File" in error_message
