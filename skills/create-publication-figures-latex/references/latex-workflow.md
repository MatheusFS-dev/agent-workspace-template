# LaTeX and TikZ workflow

## Design at publication width

Find the intended final width from the user's instructions or the manuscript. If no single-column width is supplied, use 85 mm as a starting assumption and say so. For a two-column figure, inspect the manuscript or ask for the width. The actual publication layout controls readability.

Lay out at the intended size with short line-wrapped labels, parameterized spacing, consistent node styles, and anchored arrows. Route feedback paths around objects with sufficient clearance. Draw technical glyphs with TikZ primitives in scoped coordinates. Use the reference paper's four colors only as optional defaults. Colors, line styles, shapes, and arrows that carry scientific meaning need direct labels or a key. Distinguish comparable repeated elements consistently.

Do not shrink a dense figure to fit and accept unreadable text. Reallocate space, simplify only nonessential visual details, split panels, or discuss a larger figure with the user. If scaling is necessary, inspect the final effective type size and stroke widths after scaling. Preserve supplied labels, symbols, and relationships.

## Preflight and compile

Check `pdflatex --version`, `kpsewhich standalone.cls`, and `kpsewhich tikz.sty`. Check the package files used by the figure as well. For the optional command-line preview and metadata checks, check `pdfinfo`, `pdffonts`, and `pdftoppm`. A missing compiler or required package prevents PDF delivery. Do not install it or use another drawing method silently. A missing renderer prevents visual approval unless another actual PDF viewing capability is available.

Compile from the directory containing both files:

```bash
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error figure.tex
```

Ensure the output is fresh and the command succeeds. Inspect the log for undefined control sequences, missing colors or fonts, and overfull boxes. Resolve unexpected overfull horizontal and vertical boxes, then recompile and inspect the result. Remove or isolate an old output before compiling so a failed run cannot be mistaken for a new result. Resolve manuscript-only acronyms, colors, and custom macros explicitly in the source bundle, preserving their meaning. If the source does not establish a macro's meaning, ask rather than guessing. Keep auxiliary build files out of final deliverables.

```bash
pdfinfo figure.pdf
pdffonts figure.pdf
pdftoppm -singlefile -png -r 300 figure.pdf figure
```

Confirm one page and tight page dimensions. Inspect the font list and use PDF inspection or actual rendering to confirm the artwork is vector and complete. `pdffonts` alone cannot prove all content is vector. View the resulting page at the actual publication width and inspect it at a larger scale for clipping and collisions. If a PNG preview is delivered, derive it from that same final PDF, then verify it displays the whole page.

## Manuscript inclusion

The bundled wrapper loads `amsmath`, `amssymb`, `xcolor`, `tikz`, and `arrows.meta,positioning,calc,fit,backgrounds`. A manuscript must load the packages and libraries actually used by its adapted drawing. Include the body with `\input{figure.tikz}` inside the manuscript's own `figure` environment, and put its caption and label in the manuscript. Do not use `standalone`'s document class inside the manuscript. Ensure required file paths resolve in the manuscript's build context. An exported standalone PDF can alternatively be included with `\includegraphics`.

The drawing body defines its colors and styles locally so unrelated manuscript figures are not affected. When adapting an existing figure, preserve its source organization and avoid renaming or moving unrelated content.
