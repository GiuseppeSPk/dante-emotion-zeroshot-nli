"""
Configuration - Dante Emotion Analysis

Centralized configuration for all project settings.
Modify this file to change models, paths, and parameters.
"""

from pathlib import Path

# =============================================================================
# PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CANTO_FILE = DATA_DIR / "canto_i_inferno.txt"
LEXICON_FILE = DATA_DIR / "emotion_lexicons" / "italian_emotions.json"
OUTPUT_DIR = PROJECT_ROOT / "output"
MODELS_DIR = PROJECT_ROOT / "models"  # For downloaded models

# Create directories
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# =============================================================================
# MODELS CONFIGURATION
# =============================================================================

# --- Word Embeddings ---
# --- Models Configuration ---
# Models are downloaded automatically by the transformers pipeline.

# -----------------------------------------------------------------------------

# =============================================================================
# EMOTION CATEGORIES
# =============================================================================

# Zero-Shot NLI Categories (Dante-specific)
EMOTION_CATEGORIES = [
    "paura",       # fear
    "tristezza",   # sadness  
    "rabbia",      # anger
    "speranza",    # hope
    "smarrimento", # bewilderment
]

# Color palette for visualizations
EMOTION_COLORS = {
    "paura": "#8B0000",      # dark red (Blood/Hell)
    "tristezza": "#4169E1",  # royal blue (Cold/Passive)
    "rabbia": "#FF4500",     # orange red (Aggression)
    "speranza": "#00CED1",   # dark turquoise (Bright/Divine)
    "smarrimento": "#808080", # gray (Fog/Confusion)
}

# =============================================================================
# ANALYSIS PARAMETERS
# =============================================================================

# Tercet structure
VERSES_PER_TERCET = 3
TOTAL_TERCETS_CANTO_I = 46
TOTAL_VERSES_CANTO_I = 136

# Transformer settings
MAX_SEQUENCE_LENGTH = 128
BATCH_SIZE = 8
CONFIDENCE_THRESHOLD = 0.3

# Embedding settings
EMBEDDING_DIM = 300  # FastText/Word2Vec dimension

# =============================================================================
# VISUALIZATION
# =============================================================================

FIGURE_SIZE = (14, 6)
HEATMAP_SIZE = (16, 8)
DPI = 150

# =============================================================================
# CANTO I KEY MOMENTS (for annotations)
# =============================================================================

CANTO_I_EVENTS = {
    1: "Selva oscura (Dark forest)",
    6: "Colle illuminato (Illuminated hill)",
    11: "Lonza (Leopard)",
    15: "Leone (Lion)",
    17: "Lupa (She-wolf)",
    22: "Virgilio appare (Virgil appears)",
    27: "Riconoscimento (Recognition)",
    38: "Profezia Veltro (Veltro prophecy)",
    46: "Inizio viaggio (Journey begins)"
}
