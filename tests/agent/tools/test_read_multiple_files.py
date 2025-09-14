# Standard Library Imports
import os
import tempfile
from pathlib import Path

# Local Imports
from zenith.agent.tools.read_multiple_files import read_multiple_files


# Test Read Multiple Files Function
def test_read_multiple_files_basic_success() -> None:
    """
    Tests The Read Multiple Files Function For Basic Success
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create Test Files
        file_1 = os.path.join(temp_dir, "file_1.txt")
        file_2 = os.path.join(temp_dir, "file_2.txt")

        # Write Content To File 1
        with open(file_1, "w", encoding="utf-8") as f:
            f.write("Content 1")

        # Write Content To File 2
        with open(file_2, "w", encoding="utf-8") as f:
            f.write("Content 2")

        # Read Multiple Files
        results = read_multiple_files([file_1, file_2])

        # Assertions
        assert len(results) == 2

        # Assert File 1 Data
        assert results[0]["success"] is True
        assert results[0]["path"] == str(Path(file_1).resolve())
        assert results[0]["content"] == "Content 1"

        # Assert File 2 Data
        assert results[1]["success"] is True
        assert results[1]["path"] == str(Path(file_2).resolve())
        assert results[1]["content"] == "Content 2"


# Test Read Multiple Files With Mixed Results
def test_read_multiple_files_mixed_results() -> None:
    """
    Tests The Read Multiple Files Function With Mixed Results (Success And Failure)
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create Test Files
        file_1 = os.path.join(temp_dir, "file_1.txt")
        non_existent_file = os.path.join(temp_dir, "non_existent.txt")

        # Write Content To File 1
        with open(file_1, "w", encoding="utf-8") as f:
            f.write("Content 1")

        # Read Multiple Files (One Existing, One Non-Existent)
        results = read_multiple_files([file_1, non_existent_file])

        # Assertions
        assert len(results) == 2

        # Assert File 1 Data (Success)
        assert results[0]["success"] is True
        assert results[0]["path"] == str(Path(file_1).resolve())
        assert results[0]["content"] == "Content 1"

        # Assert Non-Existent File Data (Failure)
        assert results[1]["success"] is False
        assert results[1]["path"] == non_existent_file
        assert results[1]["content"] is None
        assert "File Not Found" in results[1]["error"]


# Test Read Multiple Files With Line Range
def test_read_multiple_files_with_line_range() -> None:
    """
    Tests The Read Multiple Files Function With Line Range
    """

    # With Temporary Directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create Test Files
        file_1 = os.path.join(temp_dir, "file_1.txt")
        file_2 = os.path.join(temp_dir, "file_2.txt")

        # Write Content To File 1
        with open(file_1, "w", encoding="utf-8") as f:
            f.write("Line 1 File 1\nLine 2 File 1\nLine 3 File 1")

        # Write Content To File 2
        with open(file_2, "w", encoding="utf-8") as f:
            f.write("Line 1 File 2\nLine 2 File 2\nLine 3 File 2\nLine 4 File 2")

        # Read Multiple Files With Line Range
        results = read_multiple_files([file_1, file_2], start_line=2, end_line=3)

        # Assertions
        assert len(results) == 2

        # Assert File 1 Data
        assert results[0]["success"] is True
        assert results[0]["content"] == "Line 2 File 1\nLine 3 File 1"
        assert results[0]["selected_line_count"] == 2

        # Assert File 2 Data
        assert results[1]["success"] is True
        assert results[1]["content"] == "Line 2 File 2\nLine 3 File 2\n"
        assert results[1]["selected_line_count"] == 2


# Test Read Multiple Files With Empty List
def test_read_multiple_files_empty_list() -> None:
    """
    Tests The Read Multiple Files Function With An Empty List Of File Paths
    """

    # Read Multiple Files With An Empty List
    results = read_multiple_files([])

    # Assertions
    assert len(results) == 0
