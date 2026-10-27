---
name: create-publication-figures-latex
description: Use when creating or revising publication-ready scientific conceptual figures, system overviews, architecture diagrams, or data-flow illustrations in LaTeX or TikZ. Use for editable TikZ source or vector PDF figures, not numerical results plots or image-generated artwork.
---

# Create Publication Figures with LaTeX

Create scientific artwork, text, mathematical notation, and technical glyphs entirely with LaTeX and TikZ. Deliver editable, reproducible source and a tightly bounded, single-page vector PDF. Use this skill when the user chooses this medium. The image-generation skill and the scientific plotting skill have different purposes.

## Method and output

- Draw with TikZ primitives and native LaTeX text. Do not use image generation, imported artwork, embedded raster images, or other drawing backends. Rendering a PDF for inspection or a PNG preview does not change the artwork.
- Deliver `figure.tikz`, containing the drawing and its local styles and colors, `figure.tex`, a standalone wrapper with explicit dependencies, and the freshly compiled `figure.pdf`. Add `figure.png` only if requested or useful as a preview, rendered directly from that PDF. Names may follow the user's convention.
- Keep captions, manuscript floats, and document-specific macros outside the reusable drawing. Include any custom commands the drawing needs in the delivered bundle and document their manuscript dependencies.
- Compile without shell escape. If a compiler, package, or visual inspection tool is unavailable, identify the missing dependency and report what could not be verified. Never substitute a different drawing method, claim success from a stale PDF, or install software without authorization.

Read [the LaTeX workflow](references/latex-workflow.md) for layout, compilation, manuscript integration, and diagnostics. Adapt the [working template](assets/figure-template/figure.tex) and its companion TikZ body when useful. The template's colors and geometry are defaults, not scientific content or required style.

## Select the mode

Use first-time generation when no existing figure is the target. Use update mode for a requested change to a particular existing figure. An explicit user choice takes precedence. If the target or a requested edit is ambiguous in a way that affects scientific meaning, ask a focused question.

### First-time generation

1. Extract the scientific message, entities, relationships and arrow directions, exact labels and notation, units, colors with semantic meaning, repeated structures, and target publication width. Ask when missing information changes the meaning. Do not invent scientific content.
2. Design the composition around the target width, with short labels, clear reading order, and enough room for text and connectors. Use panels or insets only where they clarify the mechanism. Use the user's visual constraints when provided.
3. Write self-contained TikZ source. Compile, inspect the actual PDF at full size and intended paper width, and correct defects. Follow [the quality review](references/quality-review.md) before delivery.

### Update mode

1. Identify the exact source and rendered baseline. Inventory layout, labels, nodes, paths, repeated counts, visual styles, and relationships. Keep a baseline copy outside the edited files.
2. Record each requested change and the protected properties. Make only those edits and any consistency changes required by them. Preserve unrelated source, geometry, and styles. If a required consistency change is scientifically ambiguous, ask before editing.
3. Compile the modified source. Compare the source diff and actual render with the baseline, including parent views and insets. Run the quality review and correct any unintended change.
4. If only a raster image is available, explain that it requires reconstruction and cannot guarantee original source or exact geometry. Resolve whether reconstruction is intended before proceeding or claiming strict preservation. If several candidate source files or figures exist, ask which is the target.

## Review and delivery

After creator inspection, perform a distinct reviewer pass using the rendered figure and scientific requirements, without relying on the creator's rationale. Use an independent reviewer only when available and authorized, otherwise perform a separate role-isolated pass. Record each defect, its consequence, and the precise correction. Repeat compilation and review after corrections.

Do not present a figure as complete until scientific content, topology, labels, readability at the intended size, bounding box, and vector output have been checked. Report any unresolved limitations, required manuscript packages, and final file paths. Never invent missing information to clear a review finding.
