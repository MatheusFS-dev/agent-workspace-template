---
name: create-publication-figures
description: Generate or revise clear, publication-ready scientific conceptual figures, system overviews, architecture diagrams, and data-flow illustrations by using an image-generation model directly. Use for first-time figure generation or for strict, change-only updates to the latest figure when scientific meaning, cross-view consistency, paper-scale legibility, and visual fidelity require explicit review. Deliver both a high-resolution PNG and a single-page PDF made from that exact PNG. Do not use code-based drawing or programmatic figure generation.
---

# Create Publication Figures

Generate the figure itself with an image-generation model. Treat this skill as a reusable image-generation prompt and visual-quality contract.

## Non-negotiable method

- Use the available image-generation tool to create or revise the artwork directly.
- Do not draw the figure with Python, Matplotlib, PIL, ReportLab, SVG, TikZ, LaTeX, HTML, CSS, Canvas, Mermaid, Graphviz, PowerPoint, or other programmatic or manual diagram-generation methods.
- Do not create or bundle a script that generates, redraws, labels, or repairs the figure.
- Permit only two deterministic post-generation operations: crop uniform blank canvas around the artwork, then embed the final cropped PNG unchanged in a PDF. Cropping must not rescale, redraw, relabel, or reinterpret any artwork.
- Return exactly two final figure files: a high-resolution PNG and a single-page PDF containing that exact PNG.
- Size the PDF page tightly to the PNG canvas. Never place the figure on an A4, Letter, presentation, or other larger page.

## Select the operating mode

Determine the mode automatically before inspecting references or calling image generation.

- Use **first-time generation mode** when no existing figure is the target of the request.
- Use **update mode** when the user refers to the latest or a specific prior figure, reports that something is wrong, or asks to fix, remove, replace, move, resize, restyle, or otherwise change an existing figure.
- Let an explicit user choice of mode override automatic detection.
- If several prior figures could be the target, stop and ask which one. Do not guess.
- In update mode, if any requested edit, target element, intended relationship, count, selection, label, or change boundary is ambiguous, stop immediately and ask a targeted question before editing.
- In update mode, the user's explicit edit instructions override this skill's visual defaults and bundled examples. Apply defaults only where the user is silent. Never add discretionary improvements outside the requested scope.

## Use the bundled visual references

Before the first generation in a conversation, inspect every PNG in `assets/style-examples/` with an image-viewing tool. Use them as style references in the image-generation call when the tool supports referenced images.

The bundled examples are stored as raster references that can be passed directly to the image-generation model:

- `system.png`: conceptual wireless system illustration.
- `cnn_fas_nn_diagram.png`: neural-network architecture diagram.
- `dataflow.png`: scientific data-flow diagram.
- `fas_concept_high_quality.png`: polished FAS concept illustration.
- `fas_scattering_system.png`: compact FAS propagation and scattering-environment concept figure.
- `ceta_system_overview.png`: grayscale perception and risk-analysis system overview with a restrained pastel inset.

Learn the shared visual language, not the depicted objects. Do not copy the examples' subject matter, topology, labels, equations, or device designs unless the user's requested figure genuinely needs them.

## Learn from the bundled bad examples

Read `references/bad-example-catalog.md` and inspect every PNG in `assets/bad-examples/` before the first generation or update in a conversation. These are negative references, not style references.

The specific defects in each bad example are:

1. **`bad-example-01-faint-context-unsupported-selection.png`:** The background propagation paths are too faint to remain visible. The word “Compact” in “Compact aperture” is unnecessary. The candidate-port bracket marks only part of the port row even though that subset was not established, and all ports were intended to be candidates in this example. An unexplained arrow points back toward the building, and the lamp post has no scientific role. The remaining elements, overall styling, and text size are good and are not negative examples.
2. **`bad-example-02-spurious-path-cross-view-mismatch.png`:** A channel path terminates at an irrelevant lamp post. The phone selects the fifth port while the enlarged inset selects the fourth, so the parent view and zoom do not represent the same state. The candidate-port representation itself is correct.
3. **`bad-example-03-undefined-notation.png`:** The symbol `M` is used without defining what it represents. The aperture title states a numeric port count instead of introducing the concept as an `M`-port FAS aperture. The rest of the figure is good.
4. **`bad-example-04-inconsistent-repetition.png`:** The nearby-port panel contains eight ports while the distant-port panel contains seven, despite the panels being directly comparable. The port spacing also changes between panels without scientific justification.
5. **`bad-example-05-duplicate-axis-label.png`:** The y-axis meaning, “Outage probability,” appears twice. An axis title or other semantic label must not be duplicated accidentally.
6. **`bad-example-06-excessive-outer-whitespace.png`:** The scientific content is clear, but broad blank bands above and below the artwork waste canvas area and make the figure appear undersized when embedded. The final raster should be cropped to the artwork with narrow, balanced safety padding.
7. **`bad-example-07-inefficient-containers-and-ambiguous-icons.png`:** Several stages retain large empty interiors, while an ambiguous Optuna-trial graphic consumes space without clarifying the operation. Duplicate invalid-result connectors also represent one outcome more than once.
8. **`bad-example-08-equation-and-detail-overload.png`:** The method is buried under equations, set notation, and implementation-level text even though the intended explanation is visual. The density weakens the primary mechanism and reduces paper-scale legibility.
9. **`bad-example-09-misaligned-annotations-and-undefined-colors.png`:** Port-selection arrows are not anchored precisely to their target circles, count arrows add no meaning, and teal and gray sample states are not defined. Several labels are too distant from the objects they describe.
10. **`bad-example-10-notation-and-label-drift.png`:** The source variable `M` is replaced by `K`, including in the port count and matrix dimensions. The figure also retains an unnecessary “Square-root transform” label that was not part of the intended explanation.
11. **`bad-example-11-paper-scale-text-too-small.png`:** The visual mechanism is otherwise clear, but secondary labels, legend text, and explanatory text are too small relative to the stage headings and become difficult to read when reduced for a paper.

- Use them to recognize general failure classes during planning and review.
- Do not copy their subject matter, geometry, labels, or specific corrections.
- Do not pass them to image generation as positive visual references. Pass only the PNGs in `assets/style-examples/` for style.
- Do not turn a failure in one example into a domain-specific hardcoded rule. Apply the underlying consistency, evidence, causality, notation, contrast, or uniqueness check to any scientific figure.

## Shared visual language

Create a clean scientific illustration with these characteristics:

- White or very light neutral background.
- Dark navy or charcoal outlines with consistent stroke weight.
- Restrained palette led by charcoal or navy, with blue, teal, or muted green as the primary accent and at most one warm accent when useful.
- Light gray subsystem fills and a single muted pastel inset are acceptable when they improve grouping without reducing contrast.
- Large, high-contrast labels with short wording.
- Rounded rectangular containers for subsystems, stages, environments, or insets.
- Clear arrows or links that express one dominant reading direction.
- Generous whitespace and visibly separated semantic groups.
- Simple technical icons or stylized objects with enough detail to identify them, but without decorative clutter.
- Mostly flat 2D diagram language. Permit restrained soft shading or mild isometric depth for physical concept illustrations.
- Professional paper-figure appearance, not a poster, infographic, slide, advertisement, cartoon, photorealistic scene, or UI screenshot.

Choose one of two compatible treatments:

1. **Conceptual system figure**: combine simplified physical objects, signal paths, one or two labeled insets, light depth, and strong spatial grouping.
2. **Architecture or data-flow figure**: use flat rounded boxes, direct connectors, compact internal symbols, bold headings, and a limited color key.

Use the treatment that best explains the scientific idea. Combine them only when a physical system and an algorithmic inset must be shown together.

## Information-density rules

- Communicate one primary message per figure.
- Prefer three to seven major visual components.
- Split complex material into labeled regions or insets instead of shrinking everything.
- Remove decorative objects, redundant arrows, repeated labels, long prose, and information that belongs in the caption.
- Keep arrows short, directional, visually distinct, and free of unnecessary crossings.
- Keep labels close to their objects. Avoid legends when direct labeling is clearer.
- Use equations only when scientifically necessary and supplied or confirmed by the user.
- Never invent variables, units, formulas, quantitative values, architecture layers, or scientific relationships.
- Size each container from the content it actually holds. A text-only or single-icon stage must not inherit the height of a dense stage and retain a large empty interior. Reallocate width and height across siblings before shrinking labels or compressing later stages.
- Use an icon only when it identifies the stage immediately and faithfully. Otherwise use a short text label. Do not retain equations, caption-level prose, exact implementation parameters, or redundant stages that are unnecessary for the figure's primary scientific message.

## Scientific and graphical integrity rules

- Give every object, arrow, path, highlight, and inset a defined scientific role. Remove unsupported or decorative elements that could be interpreted as part of the mechanism.
- Treat every arrow or path as a claim. Verify its source, target, direction, and meaning against the user's request or source material.
- Do not infer a subset, candidate set, selected item, count, or ordering. If the source does not establish it and the choice affects meaning, ask the user.
- When a parent view and an inset depict the same entity, preserve identity exactly, including selected index, state, orientation, color, ordering, and count.
- When repeated structures are intended to be comparable, keep glyph count, size, spacing, alignment, and scale consistent unless a difference is scientifically meaningful and labeled.
- Define every symbol, abbreviation, index, and variable where the reader first encounters it. A nearby title or label may define it, but a numeric value alone does not explain what a symbol represents.
- Render each title, axis title, legend entry, and annotation once unless repetition has a clear semantic purpose.
- Keep secondary paths and background context quieter than the main mechanism but still visible at reduced paper scale.
- Before generation, compile an exact source-of-truth list of labels, variable symbols, capitalization, units, and supplied values. Reject symbol substitutions, case changes, invented or unnecessary values, unsupported qualifiers, and merged or expanded names that are absent from the source.
- Anchor every marker, error symbol, arrowhead, bracket, callout, and axis caption exactly to its target. Keep labels close enough that ownership is unambiguous. Define every scientifically meaningful color, fill, line style, or marker shape with a compact legend or direct label.
- Represent one failure or event with one connector unless distinct branches are scientifically required. Reject floating, duplicated, off-center, or nearly connected annotations.

## Typography and paper-scale legibility

- Use a clean, consistent typeface with normal letterforms. Choose either a bold sans-serif treatment or a publication-style serif treatment according to the figure type and reference family. Do not mix type styles without a clear hierarchy.
- Make text intentionally larger than normal image-generator defaults.
- Use at most three text levels: title, component label, and short annotation.
- Keep most labels to one line and preferably under five words.
- Avoid paragraphs inside the figure.
- Make primary labels approximately 4% to 6% of the image height and secondary labels approximately 2.5% to 4% when composition permits.
- Ensure every important label remains readable when the whole figure is viewed at 25% scale or placed at approximately 85 mm column width.
- Preserve exact spelling, capitalization, mathematical notation, subscripts, superscripts, acronyms, and units from the user's content.
- Treat image-generator default typography as untrusted. Establish label sizes during composition, compare equivalent headings and peer labels directly, and verify the figure at both 25% scale and its intended paper width.
- When the user exempts titles or subtitles from enlargement, preserve that hierarchy exactly. Increase text by reallocating space rather than allowing collisions, clipping, or overflow.

## Composition

- Prefer a wide landscape canvas between approximately 1.6:1 and 2.2:1 for a normal paper figure, unless the content or target layout requires another ratio.
- Establish a clear left-to-right or top-to-bottom reading order.
- Reserve narrow, balanced safety margins around the full composition. Do not crop labels, arrows, outlines, or meaningful shadows.
- Use the canvas efficiently. Do not leave broad blank bands above, below, or beside the artwork merely to preserve a generator-selected aspect ratio.
- Use alignment, spacing, and container boundaries to show hierarchy.
- Make the central mechanism visually dominant. Supporting context must be quieter.
- Use one inset only when it materially improves explanation. Use two only when essential.

## Canvas fit and cropping

- Treat excessive empty outer canvas as a deliverable defect, even when the artwork itself is correct.
- Inspect all four edges of the final raster. Distinguish intentional internal whitespace between semantic groups from unused canvas outside the complete composition.
- Crop uniform blank outer canvas to the visible artwork, then retain narrow, visually balanced safety padding. As a practical default, keep approximately 1.5% to 3% of the shorter image dimension, increasing it only when needed to protect strokes, arrowheads, labels, or meaningful shadows.
- Do not crop by a fixed aspect-ratio preset. Let the final canvas aspect ratio follow the composed artwork.
- Do not rescale or alter artwork pixels during the crop. If blank space is embedded inside a nonuniform background or the content cannot be isolated safely, use the image-generation tool to recompose the figure instead of applying a destructive crop.
- After cropping, inspect the complete image again. Reject any result with clipped content, uneven accidental padding, or remaining large blank bands.
- Treat the cropped PNG as the final master used for PDF export and delivery.

## Build the image-generation prompt

Translate the user's scientific content into the following prompt structure. Replace the bracketed fields and omit irrelevant clauses.

```text
Create a publication-ready scientific figure for a peer-reviewed paper.

Scientific message:
[State the single idea the reader must understand.]

Required content and relationships:
[List the exact components, their spatial grouping, and the direction or meaning of every essential connection.]

Layout:
[Specify left-to-right or top-to-bottom reading order, major regions, and any necessary inset. Use a wide landscape composition unless another ratio is required.]

Visual style:
Follow the attached reference figures as a visual family, not as content templates. Use a white or very light neutral background, dark charcoal or navy outlines, a restrained palette built from blue, teal, muted green, or light gray with at most one warm accent, rounded containers, simple technical icons, clean arrows, generous whitespace, and subtle depth only where it clarifies physical objects. Keep the figure polished, precise, and suitable for an IEEE or similar scientific paper.

Typography:
Use large, high-contrast, correctly spelled labels. Keep labels short. Use one coherent bold sans-serif or publication-serif treatment and no more than three text levels. Ensure all important text remains readable when the complete figure is reduced to a single paper column. Render the following labels exactly: [EXACT LABEL LIST].

Scientific constraints:
[List equations, notation, units, ordering, colors with semantic meaning, and facts that must not change.]

Avoid:
Dense layouts, tiny text, paragraphs, decorative clutter, unnecessary legends, crossing arrows, gradients that reduce contrast, photorealism, poster styling, slide styling, watermarks, captions outside the figure, invented labels, invented equations, and any element not required to explain the scientific message.

Output:
Generate one clean, high-resolution raster figure that uses the canvas efficiently. Keep only narrow, balanced safety padding around the complete artwork. Do not leave large blank bands above, below, or beside the composition, and do not clip any content. The artwork must be ready to embed in a paper.
```

Pass all relevant PNG files from `assets/style-examples/` as visual references. Use the prompt to specify content. Do not rely on the reference images to communicate scientific facts.

## Build an update prompt

In update mode, attach the last delivered high-resolution PNG as the edit input. Put this preservation contract at the top of the edit prompt, before the requested changes:

```text
Edit the attached previous figure. Treat it as the immutable visual and scientific baseline. Copy it exactly outside the explicitly requested changes. Preserve all unmentioned objects, text, positions, dimensions, internal spacing, colors, line weights, arrows, relationships, and style. Do not redesign, recompose, simplify, correct, or add anything beyond the requested scope. A final crop may remove only uniform blank canvas outside the complete artwork, as required by this skill's canvas-fit rule.

Requested changes:
[List each atomic edit exactly as requested by the user.]

Required consistency after the edit:
[List cross-view identities, counts, selections, labels, geometry, and relationships that the edit must preserve or synchronize.]

Protected content:
[List important regions and properties that must remain unchanged.]
```

Use the previous PNG as the content source of truth. Use the positive style examples only to maintain its existing visual family. If the image-generation tool cannot receive the exact prior PNG, stop and ask the user to attach it again rather than regenerating from memory.

## Generate and revise

### First-time generation mode

1. Extract the scientific message, exact labels, essential objects, and required relationships from the user's request or supplied paper.
2. Ask a targeted question when missing information would change scientific meaning. Otherwise make a conservative layout choice.
3. Inspect the positive and negative bundled references according to their separate roles.
4. Build the generation prompt using the template above.
5. Generate the figure directly with the image-generation tool at the highest practical native resolution.
6. Inspect the complete image and a reduced-size view.
7. Run the separate reviewer pass below.
8. Use image generation again to edit or regenerate every confirmed defect.
9. Repeat inspection and review until the figure passes every check.

### Update mode

1. Preserve the last delivered high-resolution PNG untouched. Make a byte-for-byte working copy when a local file is available, then use that copy as the image-edit input.
2. Inventory the baseline before editing: canvas and layout, labels, objects, arrows and paths, repeated-element counts and spacing, highlighted or selected indices, inset-to-parent mappings, colors, and scientific relationships.
3. Convert the user's request into an atomic change ledger. Separate requested changes from protected invariants.
4. If the ledger contains an unresolved target, interpretation, or scientific consequence, stop immediately and ask the user. Do not edit.
5. Build the update prompt with the preservation contract first and the atomic edits below it.
6. Edit the prior PNG directly with the image-generation tool. Do not perform a fresh generation from a textual reconstruction.
7. Compare the result with the baseline. Verify every requested change and verify that all protected regions and properties remain unchanged.
8. Run the separate reviewer pass below, focusing on both global correctness and inconsistencies introduced by the edit.
9. Reject and redo any result that changes unrelated content, misses an edit, or creates a new inconsistency.
10. Repeat until the updated figure passes every check. Do not silently broaden the edit scope while iterating.

### Finalize either mode

1. Preserve the final generated raster as a high-quality PNG. Do not substitute a screenshot or a recompressed preview.
2. Inspect the raster for unused outer canvas and crop uniform blank space according to the canvas-fit rules. Preserve a narrow, balanced safety margin and verify that no label, arrowhead, outline, path, or meaningful shadow is clipped.
3. Make the cropped high-quality PNG the final master. Do not rescale, redraw, or otherwise modify its artwork during cropping.
4. Export that exact cropped PNG as a single-page PDF using a standard image-to-PDF export or conversion capability. Preserve the full image, aspect ratio, resolution, color, and the safety margins present inside the PNG.
5. Set the PDF MediaBox and CropBox to the exact placed-image rectangle. Place the PNG at the page origin and make it fill the page edge to edge. The PDF page must have the same aspect ratio as the PNG and no external padding.
6. Do not use A4, Letter, presentation, or another fixed page preset. Do not add a page border, caption, header, footer, or whitespace outside the PNG canvas.
7. Verify the exported PDF before delivery. Confirm that it has exactly one page, that the page aspect ratio matches the cropped PNG, and that rendering the page shows the complete PNG with no added border, padding, clipping, or altered content.

## Separate scientific reviewer pass

After the creator inspection, perform a distinct reviewer pass as if reviewing a submitted paper figure without relying on the creator's intent. When an independent reviewer instance is available, give it only the rendered figure and the source requirements, not the creator's rationale or suspected defects. Otherwise perform a clearly separated role-isolated reviewer pass. The reviewer must inspect the actual rendered image and report each defect by location, violated principle, scientific or visual consequence, and precise corrective edit.

Review in this order:

1. **Semantic validity:** Does every depicted element have a necessary, defensible role?
2. **Causal and topological validity:** Does every path connect valid endpoints in the correct direction, without unexplained branches, loops, or destinations?
3. **Evidence and completeness:** Are all and only supported entities, subsets, states, values, and relationships shown?
4. **Cross-view identity:** Do parent views, zooms, insets, legends, and repeated depictions agree exactly?
5. **Repeated-geometry integrity:** Are comparable counts, sizes, spacing, alignment, and scales consistent?
6. **Notation closure:** Is every variable, abbreviation, color, marker, and symbol defined unambiguously?
7. **Notation fidelity:** Do every variable, case, unit, qualifier, and supplied value match the source-of-truth list exactly?
8. **Text uniqueness and correctness:** Are labels exact, non-duplicated, non-conflicting, and attached to the correct objects or axes?
9. **Annotation anchoring and semantic keys:** Do markers, connectors, brackets, callouts, axis captions, colors, fills, and line styles have precise targets and unambiguous meanings?
10. **Internal space efficiency:** Are containers sized to their content without large empty interiors or compressed sibling stages, and are all icons necessary and semantically faithful?
11. **Paper-scale visibility:** Are secondary channels, boundaries, markers, and labels visible at reduced size without competing with the main mechanism?
12. **Canvas efficiency:** Is the outer canvas tightly fitted with narrow, balanced safety padding and no large blank bands on any edge?

Do not deliver while the reviewer identifies a material issue. Fix it with image generation and repeat the reviewer pass. If a scientifically correct fix requires information not established by the user or source, stop and ask the user instead of inventing it.

## Final quality gate

Do not deliver the figure unless all conditions are true:

- The scientific relationships match the user's description.
- No unsupported objects, values, equations, or claims were introduced.
- Every arrow and path has a justified source, target, direction, and meaning.
- All requested components are present and visually distinct.
- Candidate sets, selected states, counts, and ordering are supported rather than inferred.
- Parent views and insets preserve the same entity identities and selected states.
- Comparable repeated elements use consistent counts, sizes, spacing, alignment, and scale.
- Every variable, symbol, abbreviation, color, and marker is defined.
- Every label, variable, capitalization choice, unit, and supplied value matches the source exactly.
- Titles, axis labels, legends, and annotations are not accidentally duplicated.
- All text is correct, large, high-contrast, and readable at reduced size.
- Markers, error symbols, arrowheads, brackets, callouts, and axis captions are precisely anchored to their intended targets.
- Every scientifically meaningful color, fill, line style, and marker shape is defined by a compact legend or direct label.
- Containers are sized to their content, without large empty interiors or compressed sibling stages.
- Every icon is necessary, compact, and semantically faithful. Equations and implementation details are present only when required by the scientific message.
- Supporting paths and background context remain visible at reduced size.
- The layout has one obvious reading order and no confusing arrow crossings.
- Stroke weights, icon style, corner radii, and colors are consistent.
- Whitespace is sufficient and the figure is not dense.
- Outer whitespace is narrow and visually balanced, with no large unused bands above, below, or beside the composition.
- Nothing is clipped or too close to an edge.
- The PNG is the highest-quality final generated image after the verified blank-canvas crop, not a thumbnail.
- The PDF contains the same figure as the PNG on one tightly fitted page, without visible quality loss, external whitespace, clipping, or content cropping.
- The PDF MediaBox and CropBox match the placed image bounds, and the PDF page aspect ratio matches the PNG canvas.
- In update mode, every requested edit is present and all unrequested content remains unchanged from the baseline.

## Delivery

Provide the final PNG and PDF together. Do not provide SVG, source code, generation scripts, or an alternative programmatically drawn version unless the user explicitly overrides this skill.
