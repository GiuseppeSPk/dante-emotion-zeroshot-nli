"""
Visualization Module - Dante Emotion Analysis

This package contains tools for visualizing
emotion analysis results.
"""

from .plots import (
    plot_emotion_curve,
    plot_emotion_heatmap,
    save_all_plots
)

__all__ = [
    "plot_emotion_curve",
    "plot_emotion_heatmap",
    "save_all_plots",
]
