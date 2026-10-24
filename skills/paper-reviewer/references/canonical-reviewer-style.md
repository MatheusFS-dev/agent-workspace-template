# Canonical Reviewer Style

This is the authoritative positive example for the *author-facing prose* produced by the paper-reviewer. It preserves a complete example of the target reviewer's writing style.

## How to use this reference

- Read the complete example before writing or editing an author-facing review, including a second-round review.
- Reproduce its **actual linguistic style**, not merely generic properties such as politeness, clarity, or constructiveness. Attend to the opening assessment, vocabulary, sentence structure, hedging, technical context, transitions, parenthetical qualifications, and natural progression toward questions.
- The four substantive comments illustrate distinct but compatible rhetorical patterns. Do not force every new comment into a fixed four-sentence structure or an exactly-one-question template. Related questions can occur in one comment.
- The example concerns one particular paper. Copy its *voice*, not its factual content, experimental claims, equipment, noise conditions, or the issues raised. Every finding in a new review must be independently verified against that manuscript.
- The verbatim excerpt intentionally retains the original spelling, grammar, capitalization, punctuation, and line breaks, including original typographical errors. These are historical source artifacts, not instructions to introduce mistakes into new reviews.
- Keep the existing evidence-verification requirements, profile-specific scientific thresholds, second-round restrictions, and confidential editor-note rules. Style fidelity does not justify unsupported criticism or conceal confirmed technical errors.

## Verbatim original review example

The text between the markers is preserved **exactly** as supplied in the original example. Do not reformat or correct it.

<!-- BEGIN VERBATIM REVIEW EXAMPLE -->
An example:
Reviewer 4
Round 1
This paper seeks to address the problem of detector selection based on actual testing data. The methodology is described clearly, in well written text, and the results obtained may have useful practical implications. Prior to publication, I would like to put forward some suggestions for clarification, as follows.

For over-the-air measurements, the description of the instrumentation given in Section 3.2 is rather brief. Is it the same USRP-based implementation as in 3.1 (just described in somewhat different words) or something else? The paper's text seems to imply the first, but I have not located an explicit statement.
It is stated (e.g. lines 298-299) that noise-only measurements (the null hypothesis) obtained in verified unoccupied channels were used for the determination of the empirical CDF. Since the authors have observed significant time-dependent noise variations (Gaussian vs impulsive conditions), it would appear that such a calibration scheme should be periodically (or continuously) updated, with verified unoccupied channels readily available. Is this realistic in practical circumstances? e.g. known abscence of primary users is sufficient to consider a channel as verified unoccupied? A little discussion would be welcome.
How were the held-out subset (30% of windows) for false-alarm validation selected? Did the authors test if the corresponding results remain consistent for different subset selections?
The results exhibit a clear distinction between (1) approximately Gaussian and (2) impulsive noise conditions, as shown and discussed in Section 5.3 and depicted in Figure 9. How were the impulsive-noise measurements separated from the near-Gaussian ones for comparison purposes? In other words, how was the classification of measurements (into the two cases) made, i.e. which criterion was used to decide if a specific recording (1E6 samples) corresponds to case (1) or (2) and characterize results accordingly?
<!-- END VERBATIM REVIEW EXAMPLE -->

## Observable features to imitate

The opening begins by describing what the paper seeks to address, acknowledges specific merits, and introduces comments as clarifications before publication. The numbered comments then vary in length and structure. Some start with a description of a section, others with `It is stated` or a direct `How were` question. The reviewer explains context using natural qualifiers such as `seems to imply`, `it would appear`, and `I have not located an explicit statement`. Parenthetical details and references to the paper arise where relevant. Two of the comments contain multiple questions that pursue the same scientific uncertainty. Some end with a restrained suggestion for clarification, others end with the question itself.

The intent is **stylistic fidelity**, not mechanically repeating stock expressions, copying sentence fragments, reproducing typos, or forcing the example's scientific subject matter onto another paper.

## Cross-domain application

For a machine-learning manuscript, the same style can ask how held-out samples were chosen, whether multiple measurements share an underlying acquisition, or how reported comparisons were made. For a systems paper, it can ask whether implementations described in separate sections are the same and how an operational assumption is maintained. These are *candidate questions only*: include them exclusively when the actual manuscript warrants them.

At final review, read the opening assessment and numbered comments next to the verbatim example. If the review sounds like a compliance checklist, a generic AI rubric, or a sequence of demands rather than the reference reviewer's natural academic prose, rewrite it. Preserve all verified scientific concerns during that rewrite.
