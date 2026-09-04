"""Install the scientific plotting helper into the current project."""

from pathlib import Path
import shutil
import sys

SOURCE_PATH = Path(__file__).resolve().parents[1] / "references" / "publication_plot_style.py"
DEFAULT_DESTINATION = Path("publication_plot_style.py")


def resolve_destination(arguments: list[str]) -> Path:
    """Resolve the helper destination path.

    Args:
        arguments: Optional positional destination path supplied after the script
            name.

    Returns:
        Destination path for the copied plotting helper.

    Raises:
        None.
    """
    if arguments:
        return Path(arguments[0])
    return DEFAULT_DESTINATION


def install_helper(source_path: Path, destination_path: Path) -> Path:
    """Copy the plotting helper to a project path.

    Args:
        source_path: Existing helper file bundled with the skill.
        destination_path: Destination file to create or overwrite.

    Returns:
        The destination path that received the helper.

    Raises:
        FileNotFoundError: If the bundled helper is missing.
        OSError: If the destination cannot be written.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Missing plotting helper: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)
    return destination_path


def main() -> int:
    """Install the plotting helper from positional arguments.

    Args:
        None.

    Returns:
        Zero when installation succeeds, otherwise one.

    Raises:
        None.
    """
    destination_path = resolve_destination(sys.argv[1:])

    try:
        installed_path = install_helper(SOURCE_PATH, destination_path)
    except OSError as error:
        print(f"install_plot_style: failed: {error}")
        return 1

    print(f"install_plot_style: installed {installed_path}")
    return 0


raise SystemExit(main())
