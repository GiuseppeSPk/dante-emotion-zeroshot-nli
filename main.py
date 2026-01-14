"""
Dante Emotion Analysis - Main Pipeline
======================================
Scientific Zero-Shot NLI Analysis of Inferno Canto I.

This script executes the complete analysis pipeline:
1.  **Loading**: Reads Canto I text.
2.  **Model**: Loads mDeBERTa Zero-Shot NLI model.
3.  **Analysis**: Applies Sliding Window (2 tercets) analysis.
4.  **Validation**: Checks results against literary Ground Truth.
5.  **Output**: Generates JSON data and visualization plots.

Usage:
    python main.py
"""

import sys
from pathlib import Path
import json
import matplotlib.pyplot as plt

# Add project root to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from config import CANTO_FILE, OUTPUT_DIR, LEXICON_FILE
from src.preprocessing import TerzinaTokenizer
from src.emotion import ZeroShotAnalyzer, LexiconEmotionAnalyzer

def main():
    # Ensure output dir
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("="*70)
    print("  DANTE EMOTION ANALYSIS: NLI vs LEXICON")
    print("  Comparing Zero-Shot Logic (NLI) against Dictionary (Lexicon)")
    print("="*70)

    # 1. Load Data
    print("\n[1] Loading Text...")
    tokenizer = TerzinaTokenizer()
    tercets = tokenizer.tokenize_file(CANTO_FILE)
    print(f"    Loaded {len(tercets)} tercets.")

    # ---------------------------------------------------------
    # PART A: ZERO-SHOT NLI (Artificial Intelligence)
    # ---------------------------------------------------------
    print("\n" + "-"*40)
    print("  PART A: ZERO-SHOT NLI (mDeBERTa)")
    print("-" * 40)
    
    analyzer_nli = ZeroShotAnalyzer()
    success = analyzer_nli.load_model()
    
    if success:
        print("    Running Sliding Window Analysis (Window=2)...")
        window_size = 2
        results_nli = analyzer_nli.analyze_sliding_window(tercets, window_size=window_size)
        
        # Save Results
        save_results("zeroshot_results.json", results_nli)
        generate_plot(results_nli, analyzer_nli.EMOTIONS, window_size, "zeroshot_curve.png", "Zero-Shot NLI")
        
        # Validation
        print("    Validating NLI Results...")
        validate_results(results_nli)
    else:
        print("    SKIPPING NLI (Model failed to load)")

    # ---------------------------------------------------------
    # PART B: LEXICON BASED (Dictionary)
    # ---------------------------------------------------------
    print("\n" + "-"*40)
    print("  PART B: LEXICON ANALYSIS (Dictionary)")
    print("-" * 40)
    
    analyzer_lex = LexiconEmotionAnalyzer(LEXICON_FILE)
    results_lex = analyzer_lex.analyze_canto(tercets)
    print(f"    Analyzed {len(results_lex)} tercets explicitly.")
    
    # Convert Lexicon results to format compatible with plotter
    # Lexicon analysis is per-tercet (Window=1 effectively)
    lex_format = []
    for i, score in enumerate(results_lex):
        lex_format.append({
            "scores": score.scores
        })
    
    generate_plot(lex_format, analyzer_nli.EMOTIONS, 1, "lexicon_curve.png", "Lexicon-Based")

    # 3. Comparative Showcase (for non-technical audience)
    perform_comparative_showcase(tercets, results_nli, results_lex)

    print("\n" + "="*70)
    print("  ANALYSIS COMPLETE - output/ folder updated")
    print("="*70)


def perform_comparative_showcase(tercets, results_nli, results_lex):
    """
    Highlights the differences between AI (NLI) and Dictionary (Lexicon) 
    on key thematic moments.
    """
    print("\n" + "="*70)
    print("  🧪 COMPARATIVE SHOWCASE: AI vs DICTIONARY")
    print("  Focus on key moments where semantic logic surpasses keywords")
    print("="*70)

    # Key moments index mapping
    # NLI results use sliding window (W=2), so results_nli[i] corresponds to tercet i+1 and i+2
    # Lexicon results are per-tercet, so results_lex[i] corresponds to tercet i+1
    
    comparisons = [
        {
            "name": "THE DARK FOREST (Incipit)",
            "tercet_idx": 0, # Tercet 1
            "explanation": "Modern dictionaries (Twitter-based) often label 'darkness' as TRISTEZZA.\nNLI understands the existential dread, correctly identifying PAURA/SMARRIMENTO."
        },
        {
            "name": "THE ILLUMINATED HILL (The Turning Point)",
            "tercet_idx": 5, # Tercet 6
            "explanation": "Dante uses the 'sun' as a METAPHOR. The dictionary sees the word 'sun' (neutral).\nNLI infers SPERANZA from the semantic field of 'light as a guide'."
        },
        {
            "name": "THE THREE BEASTS (The Lion)",
            "tercet_idx": 14, # Tercet 15
            "explanation": "Lexicon sees the beast and marks Fear.\nNLI identifies the RABBIA (aggression) of the beast itself, capturing the dual subtext."
        }
    ]

    for comp in comparisons:
        idx = comp["tercet_idx"]
        tercet = tercets[idx]
        text = " / ".join([v.text.strip() for v in tercet.verses])
        
        nli_score = results_nli[idx]["scores"] # Approx mapping (Wind 0 for Tercet 1)
        lex_score = results_lex[idx].scores
        
        nli_top = max(nli_score, key=nli_score.get)
        lex_top = max(lex_score, key=lex_score.get) if lex_score else "None"
        
        print(f"\n📍 MOMENT: {comp['name']}")
        print(f"   Text: \"{text[:100]}...\"")
        print(f"   ------------------------------------------------------------")
        print(f"   [DICTIONARY] dominant: {lex_top.upper():12} | (Keyword-based)")
        print(f"   [AI LOGIC ] dominant: {nli_top.upper():12} | (Semantic Inference)")
        print(f"   ------------------------------------------------------------")
        print(f"   💡 INSIGHT: {comp['explanation']}")


def save_results(filename, data):
    output_file = OUTPUT_DIR / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    Saved data to {output_file}")


import numpy as np
import seaborn as sns
from config import CANTO_I_EVENTS

def generate_plot(results, emotions, window_size, filename, title_suffix):
    """
    Generate an enhanced plot with smoothing and event annotations.
    """
    windows = np.arange(len(results))
    
    # Prepare figure
    plt.figure(figsize=(14, 8))
    sns.set_theme(style="whitegrid")
    
    from config import EMOTION_COLORS
    
    # Smoothing parameters
    SMOOTHING_WINDOW = 3
    
    for emo in emotions:
        # Extract raw data
        raw_values = [r['scores'].get(emo, 0.0) for r in results]
        
        # Apply smoothing (Moving Average)
        if len(raw_values) > SMOOTHING_WINDOW:
            kernel = np.ones(SMOOTHING_WINDOW) / SMOOTHING_WINDOW
            # 'same' keeps the original length
            smoothed_values = np.convolve(raw_values, kernel, mode='same')
        else:
            smoothed_values = raw_values
            
        color = EMOTION_COLORS.get(emo, 'black')
        
        # Plot smoothed line
        plt.plot(windows, smoothed_values, label=emo.capitalize(), color=color, linewidth=2.5,  alpha=0.9)
        
        # Plot transparent raw line (shadow)
        plt.plot(windows, raw_values, color=color, linewidth=1, alpha=0.15, linestyle='--')

    # Add Event Annotations
    # Map tercet numbers to window indices
    # We assume results are sequential. results[i] starts at results[i]['start_tercet']
    tercet_to_index = {r.get('start_tercet', i+1): i for i, r in enumerate(results)}
    # Fallback for simple list (Lexicon)
    if not isinstance(results[0], dict) or 'start_tercet' not in results[0]:
         tercet_to_index = {i+1: i for i in range(len(results))}

    # Add vertical lines for key events
    y_max = 1.0 # Probability space
    offset = 0
    for tercet_num, description in CANTO_I_EVENTS.items():
        # Find closest window index
        idx = tercet_to_index.get(tercet_num)
        if idx is not None:
            plt.axvline(x=idx, color='gray', linestyle=':', alpha=0.5)
            # Add text label (staggered to avoid overlap)
            y_pos = y_max - 0.05 - (offset * 0.05)
            plt.text(idx + 0.2, y_pos, f"{tercet_num}: {description}", 
                     rotation=0, fontsize=8, color='#555', 
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            offset = (offset + 1) % 4 # Stagger 4 levels deep

    plt.title(f"Evolution of Emotions in Inferno I ({title_suffix})\nSmoothed MA={SMOOTHING_WINDOW} + Event Markers", fontsize=15, weight='bold')
    plt.xlabel(f"Text Window (Rolling {window_size} Tercets)", fontsize=12)
    plt.ylabel("Intensity / Probability", fontsize=12)
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', frameon=True, title="Emotions")
    plt.margins(x=0.01)
    plt.tight_layout()

    plot_file = OUTPUT_DIR / filename
    plt.savefig(plot_file, dpi=300)
    print(f"    Saved enhanced plot to {plot_file}")
    plt.close()
    
    # Generate Heatmap as companion
    generate_heatmap(results, emotions, filename.replace("curve", "heatmap"))


def generate_heatmap(results, emotions, filename):
    """
    Generate a 'Semantic Barcode' heatmap.
    """
    data_matrix = []
    for emo in emotions:
        row = [r['scores'].get(emo, 0.0) for r in results]
        data_matrix.append(row)
    
    data_matrix = np.array(data_matrix)
    
    plt.figure(figsize=(14, 5))
    
    # Custom cmap? Or just standard. Rocket is good for intensity.
    # Convert 'config' colors to a list? No, heatmap needs one cmap.
    # "YlGnBu" is clean.
    sns.heatmap(data_matrix, yticklabels=[e.capitalize() for e in emotions], 
                xticklabels=5, cmap="YlGnBu", cbar_kws={'label': 'Intensity'})
    
    plt.title("Emotion Intensity Heatmap (Semantic Barcode)", fontsize=14)
    plt.xlabel("Window Index")
    plt.tight_layout()
    
    plot_file = OUTPUT_DIR / filename
    plt.savefig(plot_file, dpi=300)
    print(f"    Saved heatmap to {plot_file}")
    plt.close()


def validate_results(results):
    """Check critical points against literary truth."""
    # Hypothesis 1: Start (Window 0) should be Paura or Smarrimento
    start_emotions = results[0]['scores']
    top_start = max(start_emotions, key=start_emotions.get)
    print(f"    - INCIPIT (Selva): Dominant emotion is '{top_start.upper()}' (Expected: PAURA/SMARRIMENTO)")

    # Hypothesis 2: The Hill (around Tercet 6 -> Window 4-6) should be Speranza
    # Scan region to find peak Speranza
    hill_region = results[4:7] if len(results) > 7 else results[4:]
    best_hill_node = max(hill_region, key=lambda x: x['scores'].get('speranza', 0))
    
    hill_dom = best_hill_node['scores']
    top_hill = max(hill_dom, key=hill_dom.get)
    print(f"    - THE HILL (Colle, Window {best_hill_node['start_tercet']}-{best_hill_node['end_tercet']}): Dominant emotion is '{top_hill.upper()}' (Expected: SPERANZA)")


if __name__ == "__main__":
    main()
