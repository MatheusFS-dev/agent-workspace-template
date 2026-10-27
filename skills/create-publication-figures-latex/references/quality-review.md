# Scientific and visual review

Review the compiled figure against the user's source requirements, first as its creator and then in a separate reviewer role. Inspect the actual PDF or a faithful rendering, both at enlarged scale and at its intended paper width. Record location, violated requirement, consequence, and a precise correction for each defect.

1. **Scientific validity and evidence:** Every entity, value, equation, subset, selection, and relationship is supported by the source. No decorative item implies a scientific claim.
2. **Topology and causality:** Each path has the correct source, destination, direction, and meaning. No unexplained branch, loop, duplicate connector, or nearly connected arrow appears.
3. **Cross-view identity:** Parent views, insets, legends, and repeated depictions agree on identity, counts, ordering, and selection. Comparable repeated geometry has consistent size, spacing, and alignment unless a supported difference is labeled.
4. **Notation and text:** Labels, case, units, equations, subscripts, acronyms, and values match the source. Symbols and meaningful colors, line styles, and shapes are unambiguous. Labels are attached to the right objects and do not repeat accidentally.
5. **Composition and anchoring:** Text does not collide with nodes or paths. Arrowheads, markers, brackets, callouts, and labels connect precisely to their targets. Containers fit their content, major groups align, and whitespace supports the reading order without excessive blank bands.
6. **Publication scale:** After all scaling, text, mathematical notation, arrowheads, secondary paths, and strokes remain readable and distinguishable at the intended physical width. Avoid tiny text even when it compiles successfully.
7. **PDF and source:** Verify a fresh, single-page PDF with a tight bounding box and safe padding, no clipped content, and vector artwork and text. Check that the delivered source compiles without hidden manuscript dependencies and corresponds to the final PDF. Check the full page in an actual viewer or faithful rendering.
8. **Update scope:** Compare the final source and render to the baseline. Confirm each requested edit and check unchanged regions, styles, geometry, and scientific relationships. Verify any necessary consistency edits are justified.

Correct confirmed defects in the TikZ source, recompile, and repeat the review. Do not declare a pass when a material issue remains or when actual visual inspection was unavailable. If the correct fix requires missing scientific information, ask the user.
