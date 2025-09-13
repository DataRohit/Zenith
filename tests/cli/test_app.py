# Third Party Imports
import typer
from typer.testing import CliRunner

# Local Imports
from zenith.cli.app import app

# Create A Runner
runner = CliRunner()


# Test For The App Instance
def test_app_is_typer_instance() -> None:
    """
    Tests If The App Is A Typer Instance
    """

    # Assert The App Is A Typer Instance
    assert isinstance(app, typer.Typer)


# Test For The App Properties
def test_app_properties() -> None:
    """
    Tests The Properties Of The App
    """

    # Assert The App Properties Are Correct
    assert app.info.name == "zenith"
    assert app.info.help == (
        "Zenith Is A CLI-Based AI Coding Agent That Transforms "
        "Natural Language Into Efficient, Production-Ready Code!"
    )


# Test For No Completion Commands
def test_app_no_completion_commands() -> None:
    """
    Tests That No Shell Completion Commands Are Available
    """

    # Invoke The App With --help
    result = runner.invoke(app, ["--help"])

    # Assert The Exit Code Is 0
    assert result.exit_code == 0

    # Assert Completion Commands Are Not In The Output
    assert "install-completion" not in result.stdout
    assert "show-completion" not in result.stdout
