"""
Zero-Shot Emotion Analysis - Dante Alighieri

METHODOLOGY CHANGE (2024):
--------------------------
Instead of standard classification (trained on Twitter), we use Zero-Shot Classification based on 
Natural Language Inference (NLI). This allows us to query the model with semantic hypotheses 
rather than relying on rigid tags.

MODEL:
------
MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
- Multilingual (supports Italian)
- Trained on NLI data (logic/implication)
- Robust to domain shifts (works better on literature than Twitter models)

LOGIC:
------
We treat emotion detection as an entailment problem:
Premise: [Dante's Verse]
Hypothesis: "Questo testo esprime [EMOZIONE]"

The model calculates the probability that the hypothesis is true given the premise.
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import warnings
from config import EMOTION_CATEGORIES

@dataclass
class ZeroShotPrediction:
    text: str
    top_emotion: str
    scores: Dict[str, float]
    model_name: str
    
    @property
    def confidence(self) -> float:
        return self.scores.get(self.top_emotion, 0.0)

class ZeroShotAnalyzer:

    # Dante-specific emotion set (Defined in config.py) 
    EMOTIONS = EMOTION_CATEGORIES


    
    HYPOTHESIS_TEMPLATE = "Questo testo esprime {}." 

    def __init__(self):
        self.pipeline = None
        self.model_name = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli" # Multilingual (supports Italian), Trained on NLI data (logic/implication), Robust to domain shifts (works better on literature than Twitter models)
        self.device = -1
        self._simulation_mode = True

    def load_model(self) -> bool:
        """Load the NLI model for Zero-Shot classification."""
        try:
            from transformers import pipeline
            import torch
            
            self.device = 0 if torch.cuda.is_available() else -1
            print(f"[INFO] Loading Zero-Shot model: {self.model_name}...")
            print("       (This is a generic NLI model, not fine-tuned on Twitter)")
            
            self.pipeline = pipeline(
                "zero-shot-classification", 
                model=self.model_name,
                device=self.device
            )
            self._simulation_mode = False
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            print("        Falling back to simulation mode.")
            return False

    def analyze(self, text: str, emotions: Optional[List[str]] = None) -> ZeroShotPrediction:
        """
        Analyze text using Zero-Shot NLI.
        
        Args:
            text: The verse/tercet to analyze
            emotions: List of emotions to test (defaults to self.EMOTIONS)
        """
        labels = emotions or self.EMOTIONS
        
        if self._simulation_mode:
            return self._simulate(text, labels)
            
        try:
            # The core NLI call
            results = self.pipeline(
                text, 
                candidate_labels=labels,
                hypothesis_template=self.HYPOTHESIS_TEMPLATE,
                multi_label=False # We want the best fitting emotion distribution
            )
            
            # Unpack results
            scores = dict(zip(results['labels'], results['scores']))
            top_emotion = results['labels'][0]
            
            return ZeroShotPrediction(
                text=text[:50],
                top_emotion=top_emotion,
                scores=scores,
                model_name=self.model_name
            )
            
        except Exception as e:
            warnings.warn(f"Analysis failed: {e}")
            return self._simulate(text, labels)

    def analyze_sliding_window(self, tercets, window_size: int = 2) -> List[Dict]:
        """
        Analyze text using a sliding window of tercets.
        Context is crucial for Dante.
        """
        results = []
        
        for i in range(0, len(tercets) - window_size + 1):
            # Combine 'window_size' tercets
            window_tercets = tercets[i : i + window_size]
            
            # Join text
            window_text = " ".join([
                " ".join(v.text for v in t.verses) 
                for t in window_tercets
            ])
            
            prediction = self.analyze(window_text)
            
            results.append({
                "start_tercet": window_tercets[0].number,
                "end_tercet": window_tercets[-1].number,
                "text_snippet": window_text,
                "top_emotion": prediction.top_emotion,
                "confidence": prediction.confidence,
                "scores": prediction.scores
            })
            
        return results

    def _simulate(self, text: str, labels: List[str]) -> ZeroShotPrediction:
        """Fallback for testing without internet/GPU."""
        import random
        scores = {label: random.random() for label in labels}
        
        # Normalize
        total = sum(scores.values())
        scores = {k: v/total for k, v in scores.items()}
        
        # Simple heuristic overrides
        text_lower = text.lower()
        if "selva" in text_lower or "paura" in text_lower:
            scores["paura"] = 0.8
        if "luce" in text_lower or "colle" in text_lower:
            scores["speranza"] = 0.8
            
        top = max(scores, key=scores.get)
        return ZeroShotPrediction(text[:50], top, scores, "simulation")
