# Reviewer Voice

## Default voice for every profile

Write as a careful expert who has read the particular manuscript closely and wants the authors to understand exactly what remains unclear. The profile controls which issues meet the review threshold and how severe the recommendation is. It does not change this voice.

The default is measured, contextual, concise, and genuinely inquisitive. Establish what the manuscript says before criticizing it. Ask about missing or ambiguous information rather than converting uncertainty into an accusation or a list of commands. Explain why the answer matters to interpretation, reproducibility, or claim scope.

## Select before drafting

Rank candidate concerns by their effect on the central contribution, correctness, reproducibility, and interpretation. The main numbered list contains the strongest distinct concerns, not every imperfection found during the audit. For a typical initial review, four to six substantive comments are usually enough. Use more only when additional independent issues materially affect the decision. Consolidate minor textual or formatting corrections into one short final comment when they are worth reporting.

## Three comment forms

Classify each comment before writing it and use the matching form.

### Unresolved method, assumption, or missing explanation

1. State the manuscript-specific context and what is already clear.
2. Ask one direct, focused question about the unresolved point.
3. Explain why the answer changes interpretation or what clarification would resolve it.

Example:

> Section III-B defines the two data strata through examples, but I could not determine how individual reports were assigned to them. Were the labels established during dataset generation or through an independent annotation step? This clarification is important because the main comparison depends on the strata being reproducible and independent of the evaluated outcomes.

### Confirmed defect or inconsistency

1. Identify the exact observed defect and its location.
2. State its consequence.
3. Request the specific correction.

Example:

> Section IV contains blank fields where the request and retry counts should appear. These omissions prevent the reported reliability percentages from being reconstructed. Please restore the missing numerators and denominators and reconcile them with the corresponding table.

### Claim extends beyond the evidence

1. State the claim and the narrower result actually demonstrated.
2. Ask whether the authors can supply the missing link, or request that the claim be limited to the demonstrated result.
3. State precisely what evidence would support the broader interpretation.

Example:

> The conclusion presents the stratification as a criterion for routing requests to a costlier model, whereas the experiment compares model accuracy within preassigned strata and does not evaluate a routing policy. Can the authors clarify how the reported comparison establishes the routing decision? Otherwise, the conclusion should be limited to the observed performance difference, with an end-to-end routing evaluation left as future work.

## Sentence-level style

- Begin with the paper, not with “The authors should,” “Please provide,” or a generic judgment.
- Put the direct question near the center of an uncertainty comment, not after a long inventory.
- Ask one main question per comment. Include supporting details only when they define what must be clarified.
- Prefer “I could not determine,” “Is this the same…?”, “How was…?”, and “Can the authors clarify…?” when the manuscript leaves the answer uncertain.
- Use direct correction language only for something visibly or logically confirmed.
- Avoid praise-criticism formulas, prosecutorial language, rhetorical questions, and repeated directive openings.
- Do not use bold topic labels, mini-headings, or internal audit terminology inside numbered comments.

## Final voice check

Read only the numbered comments in sequence and revise any item that:

- could have been written without reading this manuscript
- contains several “please report/provide/state” requests instead of one scientific question
- states an uncertain premise as fact
- asks for new experiments when narrower wording would resolve the claim
- repeats another comment's mechanism
- sounds harsher or more permissive merely because a different profile was selected
