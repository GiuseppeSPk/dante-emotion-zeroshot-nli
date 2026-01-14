"""
Old Italian Normalizer - Dante Emotion Analysis

This module implements orthographic normalization from 14th-century
Italian to modern Italian, necessary for using contemporary NLP models.

METHODOLOGICAL MOTIVATION:
==========================
NLP models (Word2Vec, BERT, etc.) are trained on modern corpora.
Dante's vocabulary presents systematic differences:

    1. LATIN SPELLINGS: "huomo" → "uomo", "et" → "e"
    2. COMPLEX ELISIONS: "ch'i'" → "che io", "com'io" → "come io"  
    3. VERB FORMS: "avea" → "aveva", "fea" → "faceva"
    4. ARCHAIC LEXICON: "pièta" → "pietà", "vèr" → "verso"

LIMITATIONS:
============
- Normalization is APPROXIMATE and loses semantic nuances
- Not all forms are mapped (partial vocabulary)
- Meaning can differ even with the same modern spelling
  (e.g., 14th-century "gentile" ≠ modern "gentile")

These limitations are INTRINSIC to the approach and must be
explicitly documented in the analysis results.
"""

import re
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class NormalizationResult:
    """
    Normalization result with metadata.
    
    Attributes:
        original: Original form
        normalized: Normalized form
        rule_applied: Name of rule applied (if any)
        confidence: Confidence level (0.0-1.0)
    """
    original: str
    normalized: str
    rule_applied: Optional[str] = None
    confidence: float = 1.0
    
    @property
    def was_modified(self) -> bool:
        """True if the word was modified."""
        return self.original.lower() != self.normalized.lower()


class OldItalianNormalizer:
    """
    Normalizer for Dante's Old Italian.
    
    Applies normalization rules in priority order:
    1. Exact substitutions (dictionary)
    2. Regex patterns (elisions, suffixes)
    3. Fallback (lowercase, strip)
    
    Usage Example:
    --------------
    >>> normalizer = OldItalianNormalizer()
    >>> result = normalizer.normalize("ch'i'")
    >>> print(result)  # "che io"
    
    >>> # With metadata
    >>> result = normalizer.normalize_with_metadata("avea")
    >>> print(result.rule_applied)  # "verb_imperfect"
    """
    
    # =========================================================================
    # EXACT SUBSTITUTIONS DICTIONARY
    # =========================================================================
    
    EXACT_REPLACEMENTS: Dict[str, str] = {
        # Pronominal elisions
        "ch'i'": "che io",
        "ch'io": "che io",
        "com'io": "come io",
        "dov'io": "dove io",
        "com'i'": "come io",
        "s'io": "se io",
        "quand'io": "quando io",
        "perch'io": "perché io",
        "ond'io": "onde io",
        
        # Article/preposition elisions
        "d'un": "di un",
        "d'una": "di una",
        "a'": "ai",
        "de'": "dei",
        "ne'": "nei",
        "l'": "lo",  # or "la" - ambiguous
        "c'hanno": "che hanno",
        "l'animo": "lo animo",
        
        # Latin spellings
        "et": "e",
        "huomo": "uomo",
        "huomini": "uomini",
        
        # Verb forms (imperfect in -ea/-ia)
        "avea": "aveva",
        "parea": "pareva",
        "potea": "poteva",
        "facea": "faceva",
        "dicea": "diceva",
        "vedea": "vedeva",
        "credea": "credeva",
        "sapea": "sapeva",
        "volea": "voleva",
        "dovea": "doveva",
        "solea": "soleva",
        "giacea": "giaceva",
        "ardea": "ardeva",
        "piacea": "piaceva",
        
        # Contracted forms
        "fe'": "fece",
        "vo'": "voglio",
        "fo": "faccio",
        "die'": "diede",
        "stie'": "stette",
        
        # Specific lexicon
        "pièta": "pietà",
        "virtute": "virtù",
        "salute": "salvezza",
        "ogne": "ogni",
        "omo": "uomo",
        "fia": "sarà",
        "fue": "fu",
        "fui": "fui",  # unchanged
        
        # Deictics and adverbs
        "quivi": "qui",
        "quindi": "da qui",
        "colui": "lui",
        "costui": "questo",
        "ivi": "lì",
        "sovra": "sopra",
        "entro": "dentro",
        
        # Conjunctions
        "ché": "perché",
        "però": "perciò",
        "onde": "per cui",
        "acciò": "affinché",
    }
    
    # =========================================================================
    # REGEX PATTERNS
    # =========================================================================
    
    # List of (pattern, substitution, rule_name)
    REGEX_RULES: List[Tuple[str, str, str]] = [
        # Imperfect in -ea → -eva
        (r"(\w+)ea$", r"\1eva", "verb_imperfect_ea"),
        
        # Imperfect in -ia → -iva (less common)
        (r"(\w+)ìa$", r"\1iva", "verb_imperfect_ia"),
        
        # Participle in -uto → unchanged but flagged
        (r"(\w+)uto$", r"\1uto", "participle_uto"),
        
        # Suffix -ade → -à
        (r"(\w+)ade$", r"\1à", "suffix_ade"),
        
        # Suffix -ate → -à (libertate → libertà)
        (r"(\w+)ate$", r"\1à", "suffix_ate"),
        
        # Suffix -ute → -ù
        (r"(\w+)ute$", r"\1ù", "suffix_ute"),
        
        # Various consonant doubling
        (r"tt([aeiou])", r"t\1", "consonant_tt"),
    ]
    
    def __init__(self, case_sensitive: bool = False):
        """
        Initialize the normalizer.
        
        Args:
            case_sensitive: If True, respect uppercase/lowercase
        """
        self.case_sensitive = case_sensitive
        
        # Compile regex patterns
        self._compiled_rules = [
            (re.compile(pattern, re.IGNORECASE if not case_sensitive else 0), 
             replacement, 
             name)
            for pattern, replacement, name in self.REGEX_RULES
        ]
    
    def normalize_word(self, word: str) -> str:
        """
        Normalize a single word.
        
        Args:
            word: Word in Old Italian
            
        Returns:
            Normalized word
        """
        return self.normalize_with_metadata(word).normalized
    
    def normalize_with_metadata(self, word: str) -> NormalizationResult:
        """
        Normalize a word and return metadata.
        
        Args:
            word: Word in Old Italian
            
        Returns:
            NormalizationResult with transformation details
        """
        original = word
        lookup_key = word if self.case_sensitive else word.lower()
        
        # 1. Try exact substitution
        if lookup_key in self.EXACT_REPLACEMENTS:
            normalized = self.EXACT_REPLACEMENTS[lookup_key]
            # Preserve initial capitalization
            if word[0].isupper() and normalized:
                normalized = normalized[0].upper() + normalized[1:]
            
            return NormalizationResult(
                original=original,
                normalized=normalized,
                rule_applied="exact_match",
                confidence=0.95
            )
        
        # 2. Try regex patterns
        for pattern, replacement, rule_name in self._compiled_rules:
            if pattern.search(word):
                normalized = pattern.sub(replacement, word)
                return NormalizationResult(
                    original=original,
                    normalized=normalized,
                    rule_applied=rule_name,
                    confidence=0.7  # Less certain than exact match
                )
        
        # 3. Fallback: return cleaned original word
        normalized = word.strip()
        return NormalizationResult(
            original=original,
            normalized=normalized,
            rule_applied=None,
            confidence=0.5  # Don't know if already modern or not
        )
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize an entire text.
        
        Args:
            text: Text in Old Italian
            
        Returns:
            Normalized text
        """
        # Split preserving spaces and punctuation
        tokens = re.findall(r"[\w']+|[^\w]", text, re.UNICODE)
        
        normalized_tokens = []
        for token in tokens:
            if re.match(r"[\w']+", token):
                normalized_tokens.append(self.normalize_word(token))
            else:
                normalized_tokens.append(token)
        
        return "".join(normalized_tokens)
    
    def get_normalization_report(self, text: str) -> Dict:
        """
        Generate a detailed normalization report.
        
        Useful for debugging and methodological documentation.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics and details
        """
        words = re.findall(r"[\w']+", text, re.UNICODE)
        
        results = []
        rules_count = {}
        modified_count = 0
        
        for word in words:
            result = self.normalize_with_metadata(word)
            results.append(result)
            
            if result.was_modified:
                modified_count += 1
                rule = result.rule_applied or "unknown"
                rules_count[rule] = rules_count.get(rule, 0) + 1
        
        return {
            "total_words": len(words),
            "modified_words": modified_count,
            "modification_rate": modified_count / len(words) if words else 0,
            "rules_applied": rules_count,
            "details": results
        }


# =============================================================================
# Convenience Function
# =============================================================================

def normalize_text(text: str) -> str:
    """
    Normalize Old Italian text (convenience function).
    
    Args:
        text: Text in 14th-century Italian
        
    Returns:
        Normalized text in modern Italian (approximate)
    """
    normalizer = OldItalianNormalizer()
    return normalizer.normalize_text(text)


# =============================================================================
# Demo/Test
# =============================================================================

if __name__ == "__main__":
    normalizer = OldItalianNormalizer()
    
    print("=" * 60)
    print("NORMALIZER TEST - Old Italian → Modern")
    print("=" * 60)
    
    test_cases = [
        ("ch'i'", "che io"),
        ("avea", "aveva"),
        ("ché", "perché"),
        ("pièta", "pietà"),
        ("ogne", "ogni"),
        ("huomo", "uomo"),
    ]
    
    print("\nExact substitution tests:")
    for old, expected in test_cases:
        result = normalizer.normalize_with_metadata(old)
        status = "✓" if result.normalized == expected else "✗"
        print(f"  {status} '{old}' → '{result.normalized}' (expected: '{expected}')")
    
    # Test on complete verse
    print("\n" + "=" * 60)
    test_verse = "ché la diritta via era smarrita"
    print(f"Original verse: {test_verse}")
    print(f"Normalized verse: {normalize_text(test_verse)}")
    
    # Report
    print("\n" + "=" * 60)
    first_tercet = """Nel mezzo del cammin di nostra vita
mi ritrovai per una selva oscura,
ché la diritta via era smarrita."""
    
    report = normalizer.get_normalization_report(first_tercet)
    print(f"First tercet report:")
    print(f"  Total words: {report['total_words']}")
    print(f"  Modified words: {report['modified_words']}")
    print(f"  Rules applied: {report['rules_applied']}")
