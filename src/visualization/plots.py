"""
Plotting Functions - Dante Emotion Analysis

This module implements visualizations for emotion analysis:
1. Emotion curve (line plot)
2. Emotions × tercets heatmap
3. Embedding space (t-SNE scatter plot)

NOTE ON VISUALIZATION:
======================
Visualizations are designed to:
- Communicate results clearly
- Highlight structural patterns in text
- Be insertable in the final paper

Each plot includes annotations highlighting key moments
of Canto I (beasts, Virgil, etc.).
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Any
import warnings

# Style configuration
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

# Colors for emotions
EMOTION_COLORS = {
    "paura": "#8B0000",      # dark red
    "tristezza": "#4169E1",  # royal blue
    "gioia": "#FFD700",      # gold
    "rabbia": "#FF4500",     # orange red
    "sorpresa": "#9932CC",   # purple
    "disgusto": "#228B22",   # forest green
    "speranza": "#87CEEB",   # sky blue
}

# Canto I annotations (significant events)
CANTO_I_ANNOTATIONS = {
    1: "Dark forest",
    6: "Illuminated hill",
    11: "Lonza",
    15: "Lion",
    17: "She-wolf",
    22: "Virgil appears",
    27: "Virgil recognized",
    38: "Veltro prophecy",
    46: "Journey begins"
}


def plot_emotion_curve(
    results: List[Dict],
    emotions: Optional[List[str]] = None,
    title: str = "Emotion Curve - Inferno Canto I",
    figsize: tuple = (14, 6),
    annotate: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Generate emotion curve chart.
    
    Shows emotion evolution throughout the canto,
    with annotations for key moments.
    
    Args:
        curve: EmotionCurve object
        emotions: List of emotions to plot (None = all)
        title: Chart title
        figsize: Figure dimensions
        annotate: Whether to add event annotations
        save_path: Path to save (None = only display)
        
    Returns:
        Matplotlib Figure object
    """
    # Prepare data
    x = np.arange(len(results))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each emotion
    for emotion in emotions:
        y = [r['scores'].get(emotion, 0.0) for r in results]
        color = EMOTION_COLORS.get(emotion, "#666666")
        ax.plot(x, y, label=emotion.capitalize(), color=color, linewidth=2, marker='o', markersize=4)
    
    # Key event annotations
    if annotate:
        for pos, label in CANTO_I_ANNOTATIONS.items():
            if pos in x:
                ax.axvline(x=pos, color='gray', linestyle='--', alpha=0.3)
                ax.annotate(
                    label,
                    xy=(pos, ax.get_ylim()[1]),
                    xytext=(0, 5),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8,
                    rotation=45,
                    alpha=0.7
                )
    
    # Styling
    ax.set_xlabel("Tercet Number", fontsize=12)
    ax.set_ylabel("Emotional Intensity", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    
    # Methodological note
    fig.text(
        0.02, 0.02,
        "Note: Lexicon-based analysis. Results are approximate for Old Italian.",
        fontsize=8, style='italic', alpha=0.6
    )
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[INFO] Chart saved: {save_path}")
    
    return fig


def plot_emotion_heatmap(
    results: List[Dict],
    emotions: List[str],
) -> plt.Figure:
    """
    Generate emotion heatmap by tercet.
    
    Compact visualization showing distribution
    of all emotions across all tercets simultaneously.
    
    Args:
        curve: EmotionCurve object
        title: Chart title
        figsize: Figure dimensions
        save_path: Path to save
        
    Returns:
        Matplotlib Figure object
    """
    try:
        import seaborn as sns
    except ImportError:
        warnings.warn("seaborn not installed. Using base matplotlib.")
        sns = None
    
    # Prepare data matrix
    positions = np.arange(len(results))
    
    data = np.zeros((len(emotions), len(positions)))
    for i, emotion in enumerate(emotions):
        data[i, :] = [r['scores'].get(emotion, 0.0) for r in results]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if sns:
        sns.heatmap(
            data,
            xticklabels=positions,
            yticklabels=[e.capitalize() for e in emotions],
            cmap='RdYlBu_r',
            ax=ax,
            cbar_kws={'label': 'Intensity'},
            linewidths=0.5
        )
    else:
        im = ax.imshow(data, aspect='auto', cmap='RdYlBu_r')
        ax.set_xticks(range(len(positions)))
        ax.set_xticklabels(positions)
        ax.set_yticks(range(len(emotions)))
        ax.set_yticklabels([e.capitalize() for e in emotions])
        plt.colorbar(im, ax=ax, label='Intensity')
    
    ax.set_xlabel("Tercet Number", fontsize=12)
    ax.set_ylabel("Emotion", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Highlight key tercets
    key_tercets = [1, 11, 17, 22]
    for pos in key_tercets:
        if pos in positions:
            idx = positions.index(pos)
            ax.axvline(x=idx, color='white', linewidth=2, alpha=0.7)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[INFO] Heatmap saved: {save_path}")
    
    return fig


# Embedding space visualization removed (requires missing src/embeddings module)


def save_all_plots(
    results_nli: List[Dict],
    results_lex: List[Dict],
    emotions: List[str],
    output_dir: str
) -> Dict[str, str]:
    """
    Generate and save all plots.
    
    Convenience function to create all plots at once.
    
    Args:
        curve: EmotionCurve object
        embeddings: DanteEmbeddings object
        output_dir: Output directory
        words_for_embedding: Words for embedding plot
        
    Returns:
        Dictionary {plot_name: file_path}
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved = {}
    
    # 1. Emotion curve (NLI)
    path1 = str(output_dir / "zeroshot_curve.png")
    plot_emotion_curve(results_nli, emotions, title="Zero-Shot NLI Curve", save_path=path1)
    saved["zeroshot_curve"] = path1
    
    # 2. Emotion curve (Lexicon)
    path2 = str(output_dir / "lexicon_curve.png")
    plot_emotion_curve(results_lex, emotions, title="Lexicon-Based Curve", save_path=path2)
    saved["lexicon_curve"] = path2
    
    # 3. Heatmap
    path3 = str(output_dir / "zeroshot_heatmap.png")
    plot_emotion_heatmap(results_nli, emotions, save_path=path3)
    saved["zeroshot_heatmap"] = path3
    
    print(f"[INFO] All charts saved in: {output_dir}")
    return saved


# =============================================================================
# Demo/Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("VISUALIZATION TEST")
    print("=" * 60)
    
    # Import necessary modules
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    from src.emotion.emotion_curve import EmotionCurve, EmotionPoint
    from src.embeddings.word2vec_analysis import DanteEmbeddings
    
    # Create demo curve
    curve = EmotionCurve(emotion_categories=["paura", "speranza", "tristezza"])
    
    demo_data = [
        (1, {"paura": 0.6, "speranza": 0.1, "tristezza": 0.2}),
        (6, {"paura": 0.3, "speranza": 0.5, "tristezza": 0.1}),
        (11, {"paura": 0.6, "speranza": 0.15, "tristezza": 0.1}),
        (17, {"paura": 0.8, "speranza": 0.0, "tristezza": 0.15}),
        (22, {"paura": 0.4, "speranza": 0.4, "tristezza": 0.1}),
        (27, {"paura": 0.2, "speranza": 0.6, "tristezza": 0.1}),
    ]
    
    for pos, scores in demo_data:
        curve.add_point(EmotionPoint(position=pos, scores=scores))
    
    # Test curve
    print("\n📊 Generating emotion curve...")
    fig = plot_emotion_curve(curve, annotate=True)
    plt.show()
    
    print("\n✓ Test complete. Close windows to terminate.")
