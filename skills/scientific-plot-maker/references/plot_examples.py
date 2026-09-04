"""Compact examples using the publication plotting style."""

import matplotlib.pyplot as plt
import numpy as np

from publication_plot_style import (
    PALETTE,
    add_boxplot_legend,
    create_figure,
    create_two_panel_figure,
    draw_reference_boxplot,
    save_figure,
    style_axes,
    style_legend,
)


def example_scatter(output_path: str) -> None:
    """Create a styled scatter plot example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    x = np.linspace(0.0, 1.0, 40)
    y = 0.2 + 0.7 * x + 0.04 * np.sin(8.0 * np.pi * x)
    figure, axes = create_figure()
    axes.scatter(x, y, s=34, color=PALETTE["primary"], alpha=0.82, edgecolors="white", linewidths=0.6, label="Samples")
    axes.plot(x, 0.2 + 0.7 * x, color=PALETTE["reference"], linewidth=1.3, label="Trend")
    style_axes(axes, "Normalized model size", "Validation loss", grid_axis="both")
    style_legend(axes)
    save_figure(figure, output_path)
    plt.close(figure)


def example_line(output_path: str) -> None:
    """Create a styled line plot example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    epoch = np.arange(1, 21)
    loss = 0.9 * np.exp(-epoch / 7.0) + 0.08
    figure, axes = create_figure()
    axes.plot(epoch, loss, color=PALETTE["primary"], linewidth=1.8, marker="o", markersize=4.2, label="Validation")
    style_axes(axes, "Epoch", "Loss", grid_axis="y")
    style_legend(axes)
    save_figure(figure, output_path)
    plt.close(figure)


def example_histogram(output_path: str) -> None:
    """Create a styled histogram example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    rng = np.random.default_rng(7)
    values = rng.normal(loc=0.0, scale=1.0, size=400)
    figure, axes = create_figure()
    axes.hist(values, bins=24, color=PALETTE["primary"], alpha=0.82, edgecolor="white", linewidth=0.7, label="Runs")
    style_axes(axes, "Standardized score", "Count", grid_axis="y")
    style_legend(axes, location="upper right")
    save_figure(figure, output_path)
    plt.close(figure)


def example_boxplot(output_path: str) -> None:
    """Create a styled boxplot example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    rng = np.random.default_rng(11)
    groups = [rng.normal(0.42, 0.04, 40), rng.normal(0.36, 0.05, 40), rng.normal(0.31, 0.03, 40)]
    figure, axes = create_figure()
    draw_reference_boxplot(axes, groups, ["A", "B", "C"])
    style_axes(axes, "Configuration", "Loss", grid_axis="y")
    add_boxplot_legend(axes)
    save_figure(figure, output_path)
    plt.close(figure)


def example_errorbar(output_path: str) -> None:
    """Create a styled error-bar plot example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([0.51, 0.47, 0.43, 0.40, 0.39])
    error = np.array([0.03, 0.025, 0.02, 0.02, 0.018])
    figure, axes = create_figure()
    axes.errorbar(x, y, yerr=error, color=PALETTE["primary"], marker="o", markersize=4.5, linewidth=1.6, capsize=3.0, label="Mean ± CI")
    style_axes(axes, "Trial", "Metric", grid_axis="y")
    style_legend(axes)
    save_figure(figure, output_path)
    plt.close(figure)


def example_comparison_scatter(output_path: str) -> None:
    """Create a styled two-panel comparison scatter example.

    Args:
        output_path: Destination path for the generated figure.

    Returns:
        None.

    Raises:
        OSError: If the figure cannot be saved.
    """
    x = np.linspace(0.1, 1.0, 35)
    figure, axes = create_two_panel_figure()
    axes[0].scatter(x, 0.7 - 0.4 * x, s=32, color=PALETTE["primary"], alpha=0.82, edgecolors="white", linewidths=0.6)
    axes[1].scatter(x, 0.5 - 0.2 * x, s=32, color=PALETTE["secondary"], alpha=0.82, edgecolors="white", linewidths=0.6)
    style_axes(axes[0], "Model size", "Loss", title="Search space A", grid_axis="both")
    style_axes(axes[1], "Model size", "Loss", title="Search space B", grid_axis="both")
    save_figure(figure, output_path)
    plt.close(figure)
