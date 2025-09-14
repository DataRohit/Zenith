# Standard Library Imports
import os
import tempfile
from pathlib import Path

# Third Party Imports
import pytest

# Local Imports
from zenith.agent.tools.make_directory import directory_exists
from zenith.agent.tools.make_directory import make_directory


# Test Make Directory Function
def test_make_directory() -> None:
    """
    Tests The Make Directory Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test Directory Path
        test_dir = os.path.join(temp_dir, "test_directory")

        # Make The Directory
        result = make_directory(test_dir)

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_dir).resolve())
        assert "Directory Created Successfully" in result["message"]

        # Check That The Directory Exists
        assert os.path.exists(test_dir)
        assert os.path.isdir(test_dir)


# Test Make Directory With Parents
def test_make_directory_with_parents() -> None:
    """
    Tests The Make Directory Function With Parent Directories
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Nested Test Directory Path
        test_dir = os.path.join(temp_dir, "parent", "child", "grandchild")

        # Make The Directory With Parents
        result = make_directory(test_dir, parents=True)

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_dir).resolve())

        # Check That The Directory Exists
        assert os.path.exists(test_dir)
        assert os.path.isdir(test_dir)


# Test Make Directory With Existing Directory
def test_make_directory_existing() -> None:
    """
    Tests The Make Directory Function With An Existing Directory
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test Directory Path
        test_dir = os.path.join(temp_dir, "existing_directory")

        # Create The Directory First
        os.makedirs(test_dir)

        # Make The Directory Again With exist_ok=True
        result = make_directory(test_dir, exist_ok=True)

        # Check The Result
        assert result["success"] is True
        assert result["path"] == str(Path(test_dir).resolve())

        # Check That The Directory Exists
        assert os.path.exists(test_dir)
        assert os.path.isdir(test_dir)


# Test Make Directory With Existing Directory And exist_ok=False
def test_make_directory_existing_error() -> None:
    """
    Tests The Make Directory Function With An Existing Directory And exist_ok=False
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test Directory Path
        test_dir = os.path.join(temp_dir, "existing_directory")

        # Create The Directory First
        os.makedirs(test_dir)

        # With FileExistsError
        with pytest.raises(FileExistsError) as excinfo:
            # Call Make Directory With The Test Directory Path And exist_ok=False
            make_directory(test_dir, exist_ok=False)

        # Check The Error Message
        assert "Directory Already Exists" in str(excinfo.value)


# Test Make Directory With Permission Error
def test_make_directory_permission_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Make Directory Function With A Permission Error

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock mkdir Function That Raises PermissionError
    def mock_mkdir(*args: object, **kwargs: object) -> None:
        """
        Mock mkdir Function That Raises PermissionError
        """

        # Raise The PermissionError
        raise PermissionError("Permission denied")

    # Patch Path.mkdir
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test Directory Path
        test_dir = os.path.join(temp_dir, "permission_error")

        # With PermissionError
        with pytest.raises(PermissionError) as excinfo:
            # Call Make Directory With The Test Directory Path
            make_directory(test_dir)

        # Check The Error Message
        assert "Permission Denied" in str(excinfo.value)


# Test Make Directory With OS Error
def test_make_directory_os_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests The Make Directory Function With An OS Error

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest MonkeyPatch Fixture
    """

    # Define A Mock mkdir Function That Raises OSError
    def mock_mkdir(*args: object, **kwargs: object) -> None:
        """
        Mock mkdir Function That Raises OSError
        """

        # Raise The OSError
        raise OSError("Some OS error")

    # Patch Path.mkdir
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create A Test Directory Path
        test_dir = os.path.join(temp_dir, "os_error")

        # With ValueError
        with pytest.raises(ValueError) as excinfo:
            # Call Make Directory With The Test Directory Path
            make_directory(test_dir)

        # Check The Error Message
        assert "Failed To Create Directory" in str(excinfo.value)


# Test Directory Exists Function
def test_directory_exists() -> None:
    """
    Tests The Directory Exists Function
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Check That The Directory Exists
        assert directory_exists(temp_dir) is True

        # Create A Non-Existent Directory Path
        non_existent_dir = os.path.join(temp_dir, "non_existent")

        # Check That The Directory Does Not Exist
        assert directory_exists(non_existent_dir) is False

        # Create A File Path
        file_path = os.path.join(temp_dir, "test_file.txt")

        # With Test File
        with open(file_path, "w") as f:
            # Write The Test File Content
            f.write("Test content")

        # Check That The File Path Is Not Considered A Directory
        assert directory_exists(file_path) is False
