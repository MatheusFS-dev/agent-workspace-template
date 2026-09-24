"""Rendered behavior checks for Scribe's reusable LaTeX letter assets."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIBE = Path(__file__).resolve().parents[1] / "skills" / "scribe"


class ScribeLettersContractTest(unittest.TestCase):
    """Check optional letter metadata and response pagination in the PDF."""

    @classmethod
    def setUpClass(cls) -> None:
        """Skip rendering checks where TeX or PDF text extraction is absent."""
        if not shutil.which("pdflatex") or not shutil.which("pdftotext"):
            raise unittest.SkipTest("pdflatex and pdftotext are required")

    def _render(self, asset: str, overrides: str = "", page: int = 1) -> str:
        """Compile one letter variant and extract text from the requested page.

        Args:
            asset: Filename of the Scribe LaTeX asset.
            overrides: LaTeX definitions applied after the template preamble.
            page: One-based PDF page to inspect.

        Returns:
            Extracted text from the requested PDF page.
        """
        job_name = Path(asset).stem
        source = (SCRIBE / "assets" / asset).as_posix()
        tex_input = (
            r"\AtBeginDocument{" + overrides + r"}\input{" + source + "}"
        )
        with tempfile.TemporaryDirectory(prefix="scribe-letter-") as temp_dir:
            latex = subprocess.run(
                [
                    "pdflatex",
                    "-halt-on-error",
                    "-interaction=nonstopmode",
                    f"-jobname={job_name}",
                    f"-output-directory={temp_dir}",
                    tex_input,
                ],
                cwd=SCRIBE.parents[1],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(latex.returncode, 0, latex.stdout)
            pdf = Path(temp_dir) / f"{job_name}.pdf"
            extracted = subprocess.run(
                ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(extracted.returncode, 0, extracted.stdout)
            return extracted.stdout

    def test_first_submission_omits_id_and_re_subject(self) -> None:
        """Render a first-submission cover without revision-only metadata."""
        cover = self._render("cover-letter.tex")

        self.assertIn("Cover Letter", cover)
        self.assertNotIn("Manuscript ID:", cover)
        self.assertNotIn("Re:", cover)

    def test_revision_cover_uses_supplied_id_and_subject(self) -> None:
        """Render a revision cover with its context-specific metadata."""
        cover = self._render(
            "cover-letter.tex",
            r"\def\ManuscriptID{ABC-123}"
            r"\def\ReSubject{Response to minor revision comments}",
        )

        self.assertIn("Manuscript ID: ABC-123", cover)
        self.assertIn("Re: Response to minor revision comments", cover)

    def test_response_without_id_starts_replies_on_next_page(self) -> None:
        """Render a response with a subject, no ID, and a separate reply page."""
        overrides = r"\def\ReSubject{Second-round review}"
        opening = self._render("response-letter.tex", overrides, page=1)
        replies = self._render("response-letter.tex", overrides, page=2)

        self.assertIn("Re: Second-round review", opening)
        self.assertNotIn("Manuscript ID:", opening + replies)
        self.assertNotIn("Reviewer 1, Comment 1:", opening)
        self.assertIn("Reviewer 1, Comment 1:", replies)
        self.assertIn("Author Response R1.1:", replies)


if __name__ == "__main__":
    unittest.main()
