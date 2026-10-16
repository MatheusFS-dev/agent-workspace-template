# Responding to Reviewers

> **Supporting module:** Part of the Scribe skill. Load it for response letters and point-by-point rebuttals.

## Core Rule

Answer every part of each actual comment directly, ground every statement in the manuscript or supplied evidence, and distinguish completed changes from proposed changes. Reviewer authority does not authorize unsupported claims or changes that contradict the work.

Before drafting, read the full decision letter, editor and reviewer comments, revised manuscript or change record, and target journal's revision instructions. Map each comment and its subpoints to a response and a verified manuscript action or reason for no change. If a comment, material evidence, or claimed revision is missing, ask for it. A working draft may carry conspicuous unresolved items, but do not present it as a submission-ready response letter until all material items are resolved.

Do not include TODOs, local paths, unresolved-task lists, working-draft notices, or promises of future changes in a submission-ready response letter. Keep them in a separate internal revision plan. A response that reports a completed manuscript change must include the verified blue excerpt. Unresolved changes must be resolved before submission.

For a LaTeX response letter, copy the Scribe asset `assets/response-letter.tex` as the base. Keep its brief opening letter, page break, and point-by-point responses; summarize the main revisions in the opening without predicting acceptance. Adapt the IEEEtran starting class and letter format to the target journal's requirements. Set `\ManuscriptID` only when the journal provides one and `\ReSubject` only when context calls for a subject. Include an editor section for substantive editor comments and one section per reviewer who supplied comments. Preserve each complete comment in its original order and wording unless the journal explicitly requires a different format; style the comment label in green and its text in italics, then give a numbered author response in normal text. Do not copy the manuscript bibliography into the letter. Add a letter reference list only when an author response makes a sourced explanation that is absent from the manuscript.

The response letter itself must show the manuscript changes in blue. After each response that reports a completed change, reproduce the complete relevant revised or added manuscript material verbatim in a distinct blue block, except that manuscript citation commands may be omitted. Preserve the remaining substantive wording and punctuation. Include all affected content needed to verify the change, including prose, equations, captions, lists, and the full contents of every new or revised table. Do not substitute a paraphrase, change summary, location reference, or partial table for this copy. If one response caused changes in multiple noncontiguous places, include a labeled blue block for each place. For deletion-only changes, quote the surrounding retained passage in blue when it is needed to make the deletion verifiable and state explicitly what was removed. Do not color the reviewer comment or the explanatory author-response prose blue unless that text is itself copied manuscript content.

The opening may state that manuscript changes are highlighted in blue. When the user has asked to remove blue revision coloring from the revision package, remove that statement and the blue markup while retaining every reproduced change. Do not manufacture comments, completed changes, manuscript locations, or line references. Replace every bracketed placeholder before calling the letter complete.

## Respond to Each Comment

1. Reproduce the complete original comment and keep multi-part requests together or explicitly map each subpoint. Do not silently shorten or selectively quote it.
2. Identify the concern and choose a response position: agree, partly agree, clarify, or respectfully disagree.
3. Answer each subpoint with the relevant evidence or reasoning. State precisely what changed, or explain why no change was made.
4. Locate completed revisions by verified section, figure, table, equation, page, or line; page and line numbers must refer to the revised manuscript.
5. Immediately after the explanation, copy the complete relevant revised or added material verbatim from the manuscript into a blue change block. Copy full new or revised tables, not only their captions or selected rows. Verify the copy against the revised manuscript.
6. If an action is only proposed or its result is unverified, label it as such in a working draft and resolve it before submission. Do not turn a planned change into a completed-change claim or create a blue change block for material that is not yet in the manuscript.

Keep the tone respectful and technical. Thank reviewers without repeating generic thanks for every point. Avoid flattery, defensiveness, claims about reviewer intent, and vague statements such as “the manuscript has been improved accordingly” without an identifiable change.

## Disagreement

When disagreeing, identify the factual or interpretive point, cite relevant manuscript evidence, acknowledge wording that could have caused the misunderstanding, and revise ambiguous wording when useful. Explain the decision not to change without dismissing the comment.

## Final Check

Check that every editor and reviewer comment and subpoint has a direct answer; every completed change is followed by its complete relevant manuscript copy in blue; every new or revised table is reproduced in full and in blue; separate responses do not contradict one another; locations and copied material match the revised manuscript verbatim; and no response promises an incompatible or unperformed change. Follow the journal's anonymity, file, marked-manuscript, and clean-manuscript instructions. Load `references/reviewer-derived-writing-notes.md` or one topical reviewer example only when relevant, then apply `quality-control.md`.

## Publisher Guidance

The target journal's instructions govern; these references support the general point-by-point approach:

- [IEEE Author Center: understanding the decision process](https://journals.ieeeauthorcenter.ieee.org/submit-your-article-for-peer-review/understanding-the-decision-process/)
- [Taylor & Francis: how to respond to reviewer comments](https://authorservices.taylorandfrancis.com/blog/peer-review/how-to-respond-to-reviewer-comments/)
- [Elsevier: how to respond to reviewer comments](https://www-prod.elsevier.com/connect/how-to-respond-to-reviewer-comments-the-calm-way)
