# Local Imports
from zenith.cli.logo import LOGO


# Test For The Logo Constant
def test_logo_is_string() -> None:
    """
    Tests If The LOGO Constant Is A String
    """

    # Assert The Logo Is A String
    assert isinstance(LOGO, str)


# Test For The Logo Content
def test_logo_content() -> None:
    """
    Tests If The LOGO Constant Has The Correct Content
    """

    # Expected Logo
    expected_logo = (
        "███████╗███████╗███╗   ██╗██╗████████╗██╗  ██╗\n"
        "╚══███╔╝██╔════╝████╗  ██║██║╚══██╔══╝██║  ██║\n"
        "  ███╔╝ █████╗  ██╔██╗ ██║██║   ██║   ███████║\n"
        " ███╔╝  ██╔══╝  ██║╚██╗██║██║   ██║   ██╔══██║\n"
        "███████╗███████╗██║ ╚████║██║   ██║   ██║  ██║\n"
        "╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝"
    )

    # Assert The Logo Content Is Correct
    assert LOGO == expected_logo
