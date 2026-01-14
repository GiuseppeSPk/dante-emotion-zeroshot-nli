"""
Lexicon-Based Emotion Detection - Dante Emotion Analysis

This module implements dictionary-based Emotion Detection,
the simplest and most interpretable approach.

METHODOLOGY:
============
The lexicon-based approach works as follows:

1. Load a dictionary of words associated with emotions
2. For each verse/tercet, count occurrences of emotional words
3. Calculate a score for each emotion category
4. Aggregate to obtain the text's emotional profile

ADVANTAGES:
- Transparent and interpretable
- No training required
- Easily adaptable (just modify the dictionary)

DISADVANTAGES:
- Doesn't capture context (negations, irony)
- Limited to dictionary vocabulary
- Problematic for Old Italian (see below)

CRITICAL LIMITATION FOR DANTE:
==============================
⚠️ Sentiment/emotion dictionaries are built on modern Italian.
   Many Dante's words are not present or have different meanings.
   
   Example: "pièta" (Old Italian) is not in modern dictionaries,
   but "pietà" is. Normalization helps, but doesn't fully solve it.

MITIGATION:
===========
We created a custom dictionary (italian_emotions.json) that includes:
- Standard modern keywords
- Dante-specific keywords from Canto I
- Weights to reflect importance in Dante's context
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class EmotionScore:
    """
    Emotion score for a textual unit (verse, tercet).
    
    Attributes:
        scores: Dictionary {emotion: score}
        dominant: Dominant emotion
        total_matches: Total number of matches
        matched_words: Words that matched
    """
    scores: Dict[str, float] = field(default_factory=dict)
    dominant: Optional[str] = None
    total_matches: int = 0
    matched_words: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Calculate dominant emotion
        if self.scores:
            self.dominant = max(self.scores, key=self.scores.get)
    
    def to_vector(self, categories: List[str]) -> List[float]:
        """Convert to numeric vector for plotting."""
        return [self.scores.get(cat, 0.0) for cat in categories]
    
    def __repr__(self) -> str:
        if self.dominant:
            return f"EmotionScore(dominant={self.dominant}, score={self.scores.get(self.dominant, 0):.2f})"
        return "EmotionScore(no emotions detected)"


class LexiconEmotionAnalyzer:
    """
    Lexicon-based emotion analyzer.
    
    Usage Example:
    --------------
    >>> analyzer = LexiconEmotionAnalyzer()
    >>> analyzer.load_lexicon("data/emotion_lexicons/italian_emotions.json")
    >>> 
    >>> score = analyzer.analyze_text("mi ritrovai per una selva oscura")
    >>> print(score.dominant)  # "paura"
    >>> print(score.matched_words)  # ["selva", "oscura"]
    
    METHODOLOGICAL NOTE:
    ====================
    Matching is case-insensitive and applies automatic normalization
    to handle Dante's forms.
    """
    
    def __init__(self, lexicon_path: Optional[str] = None):
        """
        Initialize the analyzer.
        
        Args:
            lexicon_path: Path to the JSON dictionary file
        """
        self.lexicon: Dict[str, Dict] = {}
        self.word_to_emotion: Dict[str, List[str]] = {}
        self.categories: List[str] = []
        
        # Normalizer for archaic forms
        from ..preprocessing.normalizer import OldItalianNormalizer
        self._normalizer = OldItalianNormalizer()
        
        # Statistics
        self._total_analyzed = 0
        self._total_matches = 0
        
        if lexicon_path:
            self.load_lexicon(lexicon_path)
    
    def load_lexicon(self, path: str):
        """
        Load emotion dictionary from JSON file.
        
        Expected format:
        {
            "paura": {
                "keywords_modern": ["paura", "terrore", ...],
                "keywords_dante": ["smarrita", "oscura", ...]
            },
            ...
        }
        
        Args:
            path: Path to JSON file
        """
        path = Path(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove metadata
        if "_metadata" in data:
            del data["_metadata"]
        
        self.lexicon = data
        self.categories = list(data.keys())
        
        # Build reverse index: word → [emotions]
        self._build_word_index()
        
        total_keywords = sum(
            len(e.get("keywords_modern", [])) + len(e.get("keywords_dante", []))
            for e in self.lexicon.values()
        )
        print(f"[INFO] Lexicon loaded: {len(self.categories)} categories, {total_keywords} keywords")
    
    def _build_word_index(self):
        """Build reverse index word → emotions."""
        self.word_to_emotion.clear()
        
        for emotion, data in self.lexicon.items():
            # Modern keywords
            for word in data.get("keywords_modern", []):
                word_lower = word.lower()
                if word_lower not in self.word_to_emotion:
                    self.word_to_emotion[word_lower] = []
                self.word_to_emotion[word_lower].append(emotion)
            
            # Dante keywords
            for word in data.get("keywords_dante", []):
                word_lower = word.lower()
                if word_lower not in self.word_to_emotion:
                    self.word_to_emotion[word_lower] = []
                self.word_to_emotion[word_lower].append(emotion)
    
    def analyze_text(
        self, 
        text: str,
        normalize: bool = True
    ) -> EmotionScore:
        """
        Analyze a text and return emotional score.
        
        Args:
            text: Text to analyze (verse, tercet, etc.)
            normalize: Whether to apply ancient→modern normalization
            
        Returns:
            EmotionScore with emotion distribution
        """
        self._total_analyzed += 1
        
        # Tokenize (simple split for performance)
        words = text.lower().split()
        
        # Clean punctuation
        import re
        words = [re.sub(r'[^\w]', '', w) for w in words]
        words = [w for w in words if w]
        
        # Count matches per emotion
        emotion_counts: Dict[str, int] = defaultdict(int)
        matched_words = []
        
        for word in words:
            # Try direct match
            emotions = self._lookup_word(word)
            
            # If not found, try normalized form
            if not emotions and normalize:
                normalized = self._normalizer.normalize_word(word)
                if normalized != word:
                    emotions = self._lookup_word(normalized)
            
            if emotions:
                matched_words.append(word)
                for emotion in emotions:
                    emotion_counts[emotion] += 1
        
        self._total_matches += len(matched_words)
        
        # Normalize scores (proportion over total words)
        total_words = len(words) if words else 1
        scores = {
            emotion: count / total_words
            for emotion, count in emotion_counts.items()
        }
        
        return EmotionScore(
            scores=scores,
            total_matches=len(matched_words),
            matched_words=matched_words
        )
    
    def _lookup_word(self, word: str) -> List[str]:
        """Look up a word in the dictionary."""
        return self.word_to_emotion.get(word.lower(), [])
    
    def analyze_tercet(
        self, 
        verses: List[str]
    ) -> EmotionScore:
        """
        Analyze a complete tercet.
        
        Args:
            verses: List of 3 verses
            
        Returns:
            Aggregated EmotionScore for the tercet
        """
        combined_text = " ".join(verses)
        return self.analyze_text(combined_text)
    
    def analyze_canto(
        self, 
        tercets
    ) -> List[EmotionScore]:
        """
        Analyze an entire canto tercet by tercet.
        
        Args:
            tercets: List of Tercet objects from tokenizer
            
        Returns:
            List of EmotionScore, one per tercet
        """
        results = []
        
        for tercet in tercets:
            verses = [v.text for v in tercet.verses]
            score = self.analyze_tercet(verses)
            results.append(score)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Return analysis statistics."""
        return {
            "texts_analyzed": self._total_analyzed,
            "total_matches": self._total_matches,
            "avg_matches_per_text": (
                self._total_matches / self._total_analyzed 
                if self._total_analyzed > 0 else 0
            ),
            "lexicon_size": len(self.word_to_emotion),
            "categories": self.categories
        }
    
    def explain_score(self, score: EmotionScore) -> str:
        """
        Generate textual explanation of the score.
        
        Useful for documenting and interpreting results.
        
        Args:
            score: EmotionScore to explain
            
        Returns:
            Explanatory string
        """
        if not score.scores:
            return "No emotions detected in text."
        
        lines = ["Emotion analysis:"]
        
        # Sort by descending score
        sorted_emotions = sorted(
            score.scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for emotion, value in sorted_emotions:
            bar = "█" * int(value * 20)  # Visual bar
            lines.append(f"  {emotion:12} {bar} ({value:.2%})")
        
        if score.matched_words:
            lines.append(f"\nMatched words: {', '.join(score.matched_words)}")
        
        return "\n".join(lines)


# =============================================================================
# Convenience Function
# =============================================================================

def analyze_verse_emotions(
    verse: str,
    lexicon_path: Optional[str] = None
) -> EmotionScore:
    """
    Analyze emotions in a verse (convenience function).
    
    Args:
        verse: Verse text
        lexicon_path: Path to dictionary (optional)
        
    Returns:
        EmotionScore
    """
    import sys
    from pathlib import Path
    
    # Default path
    if lexicon_path is None:
        root = Path(__file__).parent.parent.parent
        lexicon_path = str(root / "data" / "emotion_lexicons" / "italian_emotions.json")
    
    analyzer = LexiconEmotionAnalyzer(lexicon_path)
    return analyzer.analyze_text(verse)


# =============================================================================
# Demo/Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LEXICON EMOTION ANALYZER TEST")
    print("=" * 60)
    
    # Path to lexicon
    from pathlib import Path
    root = Path(__file__).parent.parent.parent
    lexicon_path = root / "data" / "emotion_lexicons" / "italian_emotions.json"
    
    analyzer = LexiconEmotionAnalyzer(str(lexicon_path))
    
    # Test on iconic verses
    test_verses = [
        "mi ritrovai per una selva oscura",  # Expected: Fear
        "guardai in alto e vidi le sue spalle",  # Neutral/hope
        "ch'ella mi fa tremar le vene e i polsi",  # Strong fear
        "sì ch'a bene sperar m'era cagione",  # Hope
    ]
    
    print("\n📊 Verse analysis:")
    for verse in test_verses:
        score = analyzer.analyze_text(verse)
        print(f"\n'{verse}'")
        print(analyzer.explain_score(score))
    
    # Statistics
    print("\n" + "=" * 60)
    print("📈 Statistics:")
    for key, value in analyzer.get_statistics().items():
        print(f"  {key}: {value}")
