from pathlib import Path

def get_input_path(day_number: int) -> Path:
    """Returns the path to the input file for the given day."""
    # Assuming inputs are stored in 'inputs/day_XX.txt'
    root_dir = Path(__file__).parent.parent
    return root_dir / "inputs" / f"day_{day_number:02d}.txt"

def read_text(day_number: int) -> str:
    """Reads the input file for the given day as a single string."""
    return get_input_path(day_number).read_text().strip()

def read_lines(day_number: int) -> list[str]:
    """Reads the input file for the given day as a list of lines."""
    return read_text(day_number).splitlines()
