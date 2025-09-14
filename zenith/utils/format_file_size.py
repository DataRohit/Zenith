# Helper Function To Format File Size
def format_size(size: int) -> str:
    """
    Formats The File Size In A Human-Readable Format

    Args:
        size (int): The File Size In Bytes

    Returns:
        str: The Formatted File Size
    """

    # Define Size Units
    units: list[str] = ["B", "KB", "MB", "GB", "TB", "PB"]

    # Initialize Unit Index
    unit_index: int = 0

    # Convert Size
    size_float: float = float(size)

    # While The Size Is Greater Than 1024
    while size_float >= 1024 and unit_index < len(units) - 1:
        # Divide By 1024
        size_float /= 1024

        # Increment Unit Index
        unit_index += 1

    # Return Formatted Size
    return f"{size_float:.2f} {units[unit_index]}"


# Exports
__all__: list[str] = ["format_size"]
