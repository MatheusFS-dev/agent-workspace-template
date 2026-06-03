---
name: scientific-plot-maker
description: |
  Creates and reviews publication-style scientific plots with a muted serif visual language.
  Use for plotting, figure generation, Matplotlib code, chart styling, and figure review.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Scientific Plot Maker

Use this skill for plots, figures, charts, graphs, histograms, scatter plots, boxplots, error-bar plots, Matplotlib style changes, and publication-figure review.

## Visual contract

- White background.
- Serif typography, preferably Times New Roman, Times, or DejaVu Serif.
- Muted, disciplined palette.
- No flashy colors, gradients, decorative effects, or heavy backgrounds.
- Thin visible left and bottom spines, hidden top and right spines.
- Subtle dashed grid only when it improves readability.
- Clear axis labels with units when applicable.
- Frameless legends only when they add information.
- Publication-ready saved output with tight bounding boxes and adequate DPI.

## Implementation rules

- Prefer Matplotlib.
- Do not use Seaborn unless explicitly requested.
- Do not hard-code labels or units unless confirmed by the task or source data.
- Do not add decorative annotations without analytical purpose.
- Keep plotting functions small and explicit.
- Preserve existing plot semantics when refactoring.

## Reference decision table

- Need to create plot code: use this `SKILL.md` only.
- Need the style helper in a project: run `python .agent/skills/scientific-plot-maker/scripts/install_plot_style.py`.
- Need to preview the visual result: run `python .agent/skills/scientific-plot-maker/scripts/preview_plot_style.py`.
- Need example syntax: search `.agent/skills/scientific-plot-maker/references/plot_examples.py` with `search_reference.py`.
- Need to modify the style implementation: read `.agent/skills/scientific-plot-maker/references/publication_plot_style.py`.

## Helper usage

Do not read `references/publication_plot_style.py` unless editing the style itself.

When adding plot code, prefer copying the helper into the project:

```bash
python .agent/skills/scientific-plot-maker/scripts/install_plot_style.py
```

When uncertain about the visual result, generate a local preview:

```bash
python .agent/skills/scientific-plot-maker/scripts/preview_plot_style.py
```

Search examples before reading the whole examples file:

```bash
python .agent/scripts/search_reference.py .agent/skills/scientific-plot-maker/references/plot_examples.py histogram scatter errorbar
```

## Completion checklist

- The figure uses the shared visual language.
- Text is readable at paper scale.
- Labels, units, legends, and titles are technically correct.
- Grid and spines are restrained.
- Output is deterministic when file output is requested.
- Verification includes `python .agent/scripts/agent_check.py` after Python code edits.
