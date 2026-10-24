"""Contract tests for the canonical author-facing paper-reviewer style.

These tests guard instructions and source-example fidelity. They do not
measure generative model writing quality, which requires sample review audits.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWER = ROOT / "skills" / "paper-reviewer"
START = "<!-- BEGIN VERBATIM REVIEW EXAMPLE -->\n"
END = "\n<!-- END VERBATIM REVIEW EXAMPLE -->"


def _fnv1a32(text):
    value = 2166136261
    for byte in text.encode("utf-8"):
        value = (value ^ byte) * 16777619 & 0xFFFFFFFF
    return f"{value:08x}"


class CanonicalReviewerStyleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (REVIEWER / "SKILL.md").read_text(encoding="utf-8")
        cls.voice = (REVIEWER / "references" / "reviewer-voice.md").read_text(encoding="utf-8")
        cls.evidence = (
            REVIEWER / "references" / "evidence-driven-scientific-review.md"
        ).read_text(encoding="utf-8")
        cls.reference = (
            REVIEWER / "references" / "canonical-reviewer-style.md"
        ).read_text(encoding="utf-8")

    def test_canonical_example_preserves_complete_source_verbatim(self):
        self.assertEqual(self.reference.count(START), 1)
        self.assertEqual(self.reference.count(END), 1)
        text = self.reference.split(START, 1)[1].split(END, 1)[0]
        self.assertEqual(len(text), 1978)
        self.assertEqual(_fnv1a32(text), "526d10da")
        self.assertTrue(text.startswith("An example:\nReviewer 4\nRound 1\n"))
        self.assertIn("How were the held-out subset (30% of windows)", text)
        self.assertIn("which criterion was used to decide", text)

    def test_skill_loads_canonical_reference_for_every_review_round(self):
        self.assertIn(
            "[Canonical Reviewer Style](references/canonical-reviewer-style.md)",
            self.skill,
        )
        self.assertIn("second-round", self.skill.lower())
        self.assertIn("canonical", self.skill.lower())
        self.assertIn("author-facing", self.skill.lower())

    def test_voice_prioritizes_style_imitation_not_generic_politeness(self):
        self.assertIn("exact linguistic style", self.voice)
        self.assertIn("canonical-reviewer-style.md", self.voice)
        self.assertIn("multiple closely related questions", self.voice)
        self.assertIn("sentence structure", self.voice)
        self.assertIn("opening assessment", self.voice)

    def test_voice_does_not_force_rigid_question_and_sentence_templates(self):
        self.assertNotIn("Ask one main question per comment.", self.voice)
        self.assertNotIn("Put the direct question near the center", self.voice)
        self.assertNotIn("Two to four sentences", self.voice)
        self.assertNotIn("State precisely what evidence would support", self.voice)

    def test_scientific_evidence_audit_remains_separate_from_style(self):
        self.assertIn("Evidence-Driven Scientific Review", self.evidence)
        self.assertIn("Canonical Reviewer Style", self.evidence)
        self.assertIn("Do not draft from the audit table itself.", self.evidence)
        self.assertIn("Never infer venue rules", self.skill)
        self.assertIn("Never infer venue rules", self.skill)

    def test_confidential_editor_boundary_and_outputs_are_preserved(self):
        self.assertIn("confidential editor-note PDF", self.skill)
        self.assertIn("author-facing review PDF", self.skill)
        self.assertIn("editor-only material never enters", self.skill)


if __name__ == "__main__":
    unittest.main()
