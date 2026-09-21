"""Small PDF utilities for ingest-context.

Requires PyMuPDF (``pymupdf``). The script intentionally exposes only operations
needed by the skill: page-range slicing, figure crops, and embedded-image
candidate extraction.
"""

import json
import sys
from pathlib import Path

import fitz


def split_pdf(source_path: Path, spec_path: Path) -> None:
    """Split a PDF into page-range slices described by a JSON file.

    Args:
        source_path: PDF to split.
        spec_path: JSON array containing ``output``, ``start_page``, and
            ``end_page``. Page numbers are 1-based and inclusive. Relative
            output paths are resolved from the JSON file's parent directory.

    Raises:
        ValueError: If a requested range is invalid.
    """
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    source = fitz.open(source_path)
    try:
        for item in spec:
            start_page = int(item["start_page"])
            end_page = int(item["end_page"])
            if start_page < 1 or end_page < start_page or end_page > source.page_count:
                raise ValueError(
                    f"Invalid page range {start_page}-{end_page} for {source.page_count}-page PDF"
                )

            output = Path(item["output"])
            if not output.is_absolute():
                output = spec_path.parent / output
            output.parent.mkdir(parents=True, exist_ok=True)

            sliced = fitz.open()
            try:
                sliced.insert_pdf(source, from_page=start_page - 1, to_page=end_page - 1)
                sliced.save(output, garbage=4, deflate=True)
            finally:
                sliced.close()
    finally:
        source.close()


def crop_page(
    source_path: Path,
    page_number: int,
    bbox: tuple[float, float, float, float],
    output_path: Path,
    dpi: int,
) -> None:
    """Render a rectangular PDF-page region to an image.

    Args:
        source_path: Source PDF.
        page_number: 1-based source PDF page number.
        bbox: Crop box ``(x0, y0, x1, y1)`` in PDF points.
        output_path: PNG/JPEG output path.
        dpi: Render resolution.

    Raises:
        ValueError: If the page number or crop rectangle is invalid.
    """
    source = fitz.open(source_path)
    try:
        if page_number < 1 or page_number > source.page_count:
            raise ValueError(f"Page {page_number} is outside 1-{source.page_count}")

        page = source[page_number - 1]
        clip = fitz.Rect(*bbox) & page.rect
        if clip.is_empty or clip.width <= 0 or clip.height <= 0:
            raise ValueError("Crop rectangle does not intersect the page")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        pixmap = page.get_pixmap(clip=clip, dpi=dpi, alpha=False)
        pixmap.save(output_path)
    finally:
        source.close()


def extract_embedded_images(source_path: Path, output_dir: Path) -> None:
    """Extract embedded image objects as figure candidates.

    Embedded objects are candidates only. A complete scientific figure may be
    composed from multiple raster/vector objects and separate text, so callers
    must visually verify candidates before retaining them as final figures.

    Args:
        source_path: Source PDF.
        output_dir: Directory for extracted candidate images.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    source = fitz.open(source_path)
    seen_xrefs: set[int] = set()
    try:
        for page_index in range(source.page_count):
            page = source[page_index]
            for image_index, image in enumerate(page.get_images(full=True), start=1):
                xref = int(image[0])
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)
                data = source.extract_image(xref)
                extension = data.get("ext", "bin")
                output = output_dir / f"p{page_index + 1:04d}_img{image_index:03d}_xref{xref}.{extension}"
                output.write_bytes(data["image"])
    finally:
        source.close()


def print_usage() -> None:
    """Print concise command usage."""
    print(
        "Usage:\n"
        "  pdf_tools.py split <source.pdf> <slices.json>\n"
        "  pdf_tools.py crop <source.pdf> <page> <x0> <y0> <x1> <y1> <output> [dpi]\n"
        "  pdf_tools.py images <source.pdf> <output-dir>"
    )


def main() -> int:
    """Run the requested PDF utility operation.

    Returns:
        Process exit code. Zero indicates success.
    """
    if len(sys.argv) < 2:
        print_usage()
        return 2

    command = sys.argv[1]
    try:
        if command == "split" and len(sys.argv) == 4:
            split_pdf(Path(sys.argv[2]), Path(sys.argv[3]))
            return 0

        if command == "crop" and len(sys.argv) in (9, 10):
            dpi = int(sys.argv[9]) if len(sys.argv) == 10 else 200
            crop_page(
                Path(sys.argv[2]),
                int(sys.argv[3]),
                tuple(float(value) for value in sys.argv[4:8]),
                Path(sys.argv[8]),
                dpi,
            )
            return 0

        if command == "images" and len(sys.argv) == 4:
            extract_embedded_images(Path(sys.argv[2]), Path(sys.argv[3]))
            return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
