"""Generate a local preview of the scientific plotting style."""

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
import sys

HELPER_PATH = Path(__file__).resolve().parents[1] / "references" / "publication_plot_style.py"
DEFAULT_OUTPUT_PATH = Path("plot-style-preview.png")


def load_helper(path: Path):
    """Load the bundled plotting helper module.

    Args:
        path: Python helper file to import.

    Returns:
        Imported module object.

    Raises:
        FileNotFoundError: If the helper file is missing.
        ImportError: If the helper cannot be imported.
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing plotting helper: {path}")

    spec = spec_from_file_location("publication_plot_style", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create module spec for {path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_preview(output_path: Path) -> Path:
    """Create a preview figure with the bundled plotting style.

    Args:
        output_path: File path where the preview image will be saved.

    Returns:
        The saved output path.

    Raises:
        ImportError: If Matplotlib or the helper cannot be imported.
        OSError: If the output path cannot be written.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError("Matplotlib is required to generate the preview.") from error

    helper = load_helper(HELPER_PATH)
    helper.apply_publication_style()
    figure, axis = plt.subplots(figsize=(4.0, 2.6), dpi=160)
    x_values = [0, 1, 2, 3, 4]
    y_values = [0.0, 0.7, 1.1, 1.0, 1.4]
    axis.plot(x_values, y_values, marker="o", linewidth=1.4, markersize=4.0)
    helper.style_axes(axis, "Sample index", "Normalized value", title="Publication style preview")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(figure)
    return output_path


def main() -> int:
    """Generate the plotting style preview.

    Args:
        None.

    Returns:
        Zero when the preview is generated, otherwise one.

    Raises:
        None.
    """
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT_PATH

    try:
        saved_path = create_preview(output_path)
    except (ImportError, OSError) as error:
        print(f"preview_plot_style: failed: {error}")
        return 1

    print(f"preview_plot_style: saved {saved_path}")
    return 0


raise SystemExit(main())
