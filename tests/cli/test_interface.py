# Standard Library Imports
from pathlib import Path
from unittest.mock import patch

# Third Party Imports
import pytest
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Local Imports
from zenith.cli.interface import create_panel


# Test Fixture For create_panel
@pytest.fixture
def panel() -> Panel:
    """
    Pytest Fixture To Create A Panel Instance For Testing
    """

    # With Patch For Path.cwd
    with patch("zenith.cli.interface.Path.cwd") as mock_cwd:
        # Set Mock Return Value
        mock_cwd.return_value = Path("/test/dir")

        # Yield The Panel
        yield create_panel()


# Tests For Interface Module
def test_create_panel_instance(panel: Panel) -> None:
    """
    Tests If The create_panel Function Returns A Panel Instance

    Args:
        panel (Panel): The Panel Instance To Test
    """

    # Assert The Panel Instance Is A Panel
    assert isinstance(panel, Panel)


# Tests For The Properties Of The Panel
def test_create_panel_properties(panel: Panel) -> None:
    """
    Tests The Properties Of The Panel Returned By create_panel

    Args:
        panel (Panel): The Panel Instance To Test
    """

    # Assert The Panel Styles Are Correct
    assert panel.title == "[bold blue]🌌 Zenith[/bold blue]"
    assert panel.border_style == "bold blue"
    assert panel.expand is True

    # Assert The Panel Padding Is Correctly Set
    assert panel.padding == (2, 1, 1, 1)


# Tests For The Table Properties Of The Panel
def test_create_panel_table_properties(panel: Panel) -> None:
    """
    Tests The Table Properties Within The Panel

    Args:
        panel (Panel): The Panel Instance To Test
    """

    # Get The Table From The Panel
    table = panel.renderable

    # Assert The Table Is A Table
    assert isinstance(table, Table)
    assert len(table.columns) == 1

    # Assert The Table Columns Are Correctly Set
    assert table.columns[0].justify == "center"


# Tests For The Content Of The Table Within The Panel
def test_create_panel_table_content(panel: Panel) -> None:
    """
    Tests The Content Of The Table Within The Panel

    Args:
        panel (Panel): The Panel Instance To Test
    """

    # Get The Table From The Panel
    table = panel.renderable

    # Assert The Logo Is Correct
    logo = (
        "███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗\n"
        "╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║\n"
        "  ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║\n"
        " ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║\n"
        "███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║\n"
        "╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝"
    )

    # Expected Rows Data (text, style)
    expected_rows = [
        (logo, "bold #9933FF"),
        ("", None),
        ("Transforming Natural Language Into Production-Ready Code", "#00BFFF"),
        ("", None),
        (
            (
                "Zenith Is A CLI-Based AI Coding Agent That Transforms "
                "Natural Language Into Efficient, Production-Ready Code!"
            ),
            None,
        ),
        ("", None),
        (f"Current Working Directory: {Path('/test/dir')}", "dim"),
    ]

    # Assert The Number Of Rows Is Correct
    assert len(table.rows) == len(expected_rows)

    # Get The Cells From The Table
    cells = list(table.columns[0].cells)

    # Iterate Over The Expected Rows
    for i, (text, style) in enumerate(expected_rows):
        # Get The Cell From The Table
        cell = cells[i]

        # If The Cell Is A Text
        if isinstance(cell, Text):
            # Assert The Cell Plain Text Is Correct
            assert cell.plain == text

            # If The Style Is Not None
            if style:
                # Assert The Cell Style Is Correct
                assert str(cell.style) == style
        else:
            # Assert The Cell Is Correct
            assert cell == text

    # Get The Description Text From The Table
    description_text = cells[4]

    # Assert The Justify Property Is Correct
    assert description_text.justify == "center"
