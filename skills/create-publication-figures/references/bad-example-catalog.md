# Bad-example catalog

Use this catalog only as a taxonomy of failures to prevent. Inspect the corresponding PNGs with an image-viewing tool. Do not use them as positive style references and do not copy their scientific content.

The examples contain many successful qualities. A negative example designation applies only to the defects listed here.

## Example 1: faint context, unsupported subset, and invalid scene logic

File: `assets/bad-examples/bad-example-01-faint-context-unsupported-selection.png`

Successful qualities to preserve in future work include the text size, overall styling, and most elements.

Failure classes:

- Secondary propagation paths are so light that they become difficult to see.
- A label contains an unnecessary qualifier that is not needed to identify the object.
- The candidate selection marks only some ports even though the intended candidate set was not established. The figure inferred scientific content.
- A path points back toward a building without an explained propagation or causal role.
- A lamp post is present without a scientific purpose.

General checks:

- Can every secondary path still be seen at paper scale?
- Is every qualifier necessary and supported?
- Does a subset or selection come from the user or source, rather than the generator?
- Can every arrow and environmental object be justified scientifically?

## Example 2: spurious destination and cross-view selection mismatch

File: `assets/bad-examples/bad-example-02-spurious-path-cross-view-mismatch.png`

The candidate ports are otherwise represented correctly.

Failure classes:

- A channel path terminates at an irrelevant lamp post.
- The selected port in the terminal differs from the selected port in the zoomed inset.

General checks:

- Does every path terminate at a scientifically meaningful entity?
- When an inset enlarges a parent element, do selection index, ordering, state, and color match exactly?

## Example 3: undefined notation

File: `assets/bad-examples/bad-example-03-undefined-notation.png`

The figure is otherwise strong.

Failure class:

- The symbol `M` appears in equations and a value assignment, but the figure never defines what `M` represents. A title that names an `M`-port aperture would establish the meaning more clearly than a numeric title alone.

General checks:

- Can a reader define every variable and abbreviation from the figure itself?
- Does the first relevant title, label, legend, or annotation introduce the symbol's meaning, not only its value?

## Example 4: inconsistent repeated structures

File: `assets/bad-examples/bad-example-04-inconsistent-repetition.png`

Failure classes:

- Two comparable port rows contain different numbers of ports without a scientific reason.
- Port spacing changes between panels even though the rows are intended to support a direct comparison.

General checks:

- For comparable repeated structures, do count, glyph size, spacing, alignment, and scale agree?
- If they differ, is the difference intentional, meaningful, and explicitly communicated?

## Example 5: duplicated semantic label

File: `assets/bad-examples/bad-example-05-duplicate-axis-label.png`

Failure class:

- The y-axis meaning is labeled twice, creating an accidental duplicate.

General checks:

- Does every axis title, heading, legend item, and annotation appear exactly once unless repetition is intentional?
- Are a directional annotation and an axis title visually and semantically distinct?

## Example 6: excessive outer whitespace

File: `assets/bad-examples/bad-example-06-excessive-outer-whitespace.png`

The scientific content, text legibility, and left-to-right layout are not the negative example.

Failure class:

- Broad blank bands above and below the complete composition waste canvas area. When the raster is embedded at a fixed width, the useful artwork becomes unnecessarily small.

General checks:

- Does the visible composition use the raster canvas efficiently on all four edges?
- Are outer margins narrow and visually balanced rather than inherited from an arbitrary generator or page aspect ratio?
- Can unused uniform background be removed without clipping labels, arrowheads, outlines, paths, or meaningful shadows?

## Example 7: inefficient containers, ambiguous icons, and duplicate outcomes

File: `assets/bad-examples/bad-example-07-inefficient-containers-and-ambiguous-icons.png`

The overall pipeline order, stage grouping, and restrained visual style are useful qualities and are not negative examples.

Failure classes:

- Text-only and simple stages inherit tall containers with large empty interiors.
- The Optuna-trial graphic is visually prominent but does not identify candidate proposal clearly or faithfully.
- A single invalid feasibility outcome is represented with duplicate connectors.
- Dense and sparse stages receive similar dimensions, wasting space that could support larger text or less compressed neighboring content.

General checks:

- Size each container from the content it actually holds. A text-only or single-icon stage must not inherit the height of a dense stage and retain a large empty interior.
- Reallocate width and height across sibling stages before shrinking labels or compressing later stages.
- Use an icon only when it identifies the stage immediately and faithfully. Otherwise, use a short text label.
- Represent one failure or event with one connector unless distinct branches are scientifically required.

## Example 8: equation, prose, and implementation-detail overload

File: `assets/bad-examples/bad-example-08-equation-and-detail-overload.png`

The three-stage reading order and consistent color semantics are useful qualities and are not negative examples.

Failure classes:

- Equations and set notation occupy the center of the explanation even though the intended message can be communicated visually.
- Caption-level prose and implementation detail compete with the actual selection and coverage mechanism.
- Excessive content forces secondary text to become small at paper scale.

General checks:

- Show only the information needed to understand the figure's primary scientific message.
- Remove caption-level prose, redundant stages, exact implementation parameters, and equations that are not necessary for the visual explanation or explicitly required.
- If the figure should be visual-only, represent relationships with objects, states, and arrows rather than formula blocks.
- Do not retain a stage merely because it appears in the implementation when removing it leaves the scientific explanation intact.

## Example 9: imprecise annotation anchoring and undefined visual states

File: `assets/bad-examples/bad-example-09-misaligned-annotations-and-undefined-colors.png`

The three-panel organization and overall selected-port ranking concept are useful qualities and are not negative examples.

Failure classes:

- The top-port arrows do not terminate precisely at the centers of their intended port circles.
- Repeated arrows beneath the sample columns add no scientific meaning and create visual noise.
- Teal and gray sample states carry scientific meaning but are not defined by a legend or direct labels.
- Several labels are far enough from their objects that ownership becomes less immediate.

General checks:

- Anchor every marker, error symbol, arrowhead, bracket, callout, and axis caption exactly to its intended target.
- Keep labels close enough that ownership is unambiguous.
- Whenever color, fill, line style, or marker shape carries scientific meaning, define every state with a compact legend or direct label.
- Reject floating, duplicated, off-center, or nearly connected annotations. A visually approximate attachment is not sufficient when the annotation identifies a specific sample, port, stage, or endpoint.

## Example 10: notation and label drift

File: `assets/bad-examples/bad-example-10-notation-and-label-drift.png`

The left-to-right dataset-generation sequence and major stage structure are useful qualities and are not negative examples.

Failure classes:

- The source variable `M` is replaced by `K` in the port count and correlation-matrix dimensions.
- The unnecessary label “Square-root transform” remains even though it is not part of the intended conceptual explanation.
- The notation is internally understandable but scientifically wrong, which is distinct from undefined notation.

General checks:

- Before generation, compile an exact source-of-truth list of labels, variable symbols, capitalization, units, and supplied values.
- Compare the rendered figure against that list.
- Reject symbol substitutions such as `K` for `M`, case changes such as `m` for `M`, invented or unnecessary numerical values, unsupported qualifiers, and merged or expanded names that are absent from the source.
- Review notation definition and notation fidelity separately. A symbol can be well defined and still be wrong.

## Example 11: paper-scale text is too small

File: `assets/bad-examples/bad-example-11-paper-scale-text-too-small.png`

The visual-only three-stage mechanism, color legend, and reading order are useful qualities and are not negative examples.

Failure classes:

- Secondary labels, legend entries, and explanatory text are disproportionately small relative to the stage headings.
- Important labels become difficult to read when the whole figure is reduced to paper width.
- The available internal space could support larger text without collisions or overflow.

General checks:

- Treat image-generator default typography as untrusted.
- Establish label sizes during composition and inspect the complete figure at 25% scale and at its intended paper width.
- Reject any important label that is unreadable or any equivalent headings and peer labels with inconsistent sizes.
- When the user exempts titles or subtitles from enlargement, preserve that hierarchy exactly.
- Increase text by reallocating space rather than allowing labels to collide, clip, or overflow.

## Generalization rule

Do not search only for these exact objects or labels. Apply the underlying audits to any domain:

- evidence before depiction;
- meaningful endpoints and directions;
- identity consistency across representations;
- consistent repeated geometry;
- complete notation;
- exact notation, label, capitalization, unit, and value fidelity;
- unique semantic labels;
- precise annotation anchoring and complete visual-state definitions;
- content-sized containers and semantically faithful icons;
- message-appropriate information density;
- paper-scale typography with a consistent hierarchy;
- efficient canvas use with safe, balanced outer padding;
- visible but subordinate context.
