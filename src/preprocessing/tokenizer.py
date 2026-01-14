"""
Old Italian Tokenizer - Dante Emotion Analysis

This module implements tokenization for Dante's text,
respecting the metrical structure of terza rima.

METHODOLOGICAL NOTE:
====================
Standard tokenizers (spaCy, NLTK) are trained on modern Italian
and systematically fail on typical 14th-century Italian forms:

    - Complex elisions: "ch'i'" (che io), "com'io" (come io)
    - Enclisis: "ritrovai" (mi ritrovai), "smarrita" (era smarrita)
    - Latin spellings: "et" (e), "huomo" (uomo)

For this reason, we implement a custom tokenizer that explicitly
handles these cases, documenting the choices made.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Generator
from pathlib import Path


@dataclass
class Token:
    """
    Representation of a single token.
    
    Attributes:
        text: Original form of the token
        normalized: Normalized form (modern Italian)
        position: Position in the verse (0-indexed)
        verse_num: Verse number in the canto
        tercet_num: Tercet number
    """
    text: str
    normalized: Optional[str] = None
    position: int = 0
    verse_num: int = 0
    tercet_num: int = 0
    
    def __repr__(self) -> str:
        if self.normalized and self.normalized != self.text:
            return f"Token('{self.text}' → '{self.normalized}')"
        return f"Token('{self.text}')"


@dataclass 
class Verse:
    """
    Representation of a verse.
    
    Attributes:
        text: Complete text of the verse
        tokens: List of tokens
        number: Verse number in the canto (1-indexed)
        tercet: Tercet number (1-indexed)
        position_in_tercet: Position in the tercet (1, 2, or 3)
    """
    text: str
    tokens: List[Token]
    number: int
    tercet: int
    position_in_tercet: int
    
    def __repr__(self) -> str:
        return f"Verse({self.number}: '{self.text[:30]}...')"


@dataclass
class Tercet:
    """
    Representation of a tercet.
    
    Terza rima is the fundamental metrical structure of the Commedia:
    ABA BCB CDC... where each tercet shares a rhyme with the next.
    
    Attributes:
        verses: List of 3 verses
        number: Tercet number (1-indexed)
    """
    verses: List[Verse]
    number: int
    
    @property
    def text(self) -> str:
        """Complete text of the tercet."""
        return "\n".join(v.text for v in self.verses)
    
    @property
    def all_tokens(self) -> List[Token]:
        """All tokens in the tercet."""
        return [t for v in self.verses for t in v.tokens]


class TerzinaTokenizer:
    """
    Specialized tokenizer for the Divine Comedy.
    
    Handles the terza rima metrical structure and peculiarities
    of 14th-century Italian.
    
    Usage Example:
    --------------
    >>> tokenizer = TerzinaTokenizer()
    >>> tercets = tokenizer.tokenize_file("data/canto_i_inferno.txt")
    >>> for tercet in tercets:
    ...     print(f"Tercet {tercet.number}: {len(tercet.all_tokens)} tokens")
    
    KNOWN LIMITATIONS:
    ------------------
    - The elision "ch'i'" is split into ["ch'", "i'"] instead of ["che", "io"]
    - Some contracted verb forms may not be recognized
    - Internal verse punctuation may cause incorrect splits
    """
    
    # Pattern to recognize tercet number: [1], [2], etc.
    TERCET_MARKER = re.compile(r'^\[(\d+)\]$')
    
    # Base tokenization pattern
    # Handles internal apostrophes (elisions)
    TOKEN_PATTERN = re.compile(r"[\w']+|[^\w\s]", re.UNICODE)
    
    # Punctuation to preserve as separate tokens
    PUNCTUATION = set('.,;:!?»«"\'()-')
    
    def __init__(self, normalize: bool = True):
        """
        Initialize the tokenizer.
        
        Args:
            normalize: If True, apply ancient→modern normalization
        """
        self.normalize = normalize
        self._normalizer = None
        
        if normalize:
            from .normalizer import OldItalianNormalizer
            self._normalizer = OldItalianNormalizer()
    
    def tokenize_file(self, filepath: str | Path) -> List[Tercet]:
        """
        Tokenize an entire file (canto).
        
        Args:
            filepath: Path to the text file
            
        Returns:
            List of Tercet objects
        """
        filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.tokenize_canto(text)
    
    def tokenize_canto(self, text: str) -> List[Tercet]:
        """
        Tokenize the text of an entire canto.
        
        Expected format:
            [1]
            verse 1
            verse 2
            verse 3
            
            [2]
            verse 4
            ...
        
        Args:
            text: Complete canto text
            
        Returns:
            List of tokenized tercets
        """
        tercets = []
        current_tercet_num = 0
        current_verses = []
        verse_counter = 0
        
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip comments/headers
            if line.startswith('#'):
                continue
            
            # Check if it's a tercet marker [N]
            match = self.TERCET_MARKER.match(line)
            if match:
                # Save previous tercet if complete
                if current_verses:
                    tercets.append(Tercet(
                        verses=current_verses,
                        number=current_tercet_num
                    ))
                    current_verses = []
                
                current_tercet_num = int(match.group(1))
                continue
            
            # It's a normal verse
            verse_counter += 1
            position_in_tercet = ((verse_counter - 1) % 3) + 1
            
            verse = self._tokenize_verse(
                line, 
                verse_num=verse_counter,
                tercet_num=current_tercet_num,
                position_in_tercet=position_in_tercet
            )
            current_verses.append(verse)
        
        # Add the last tercet (or single final verse)
        if current_verses:
            tercets.append(Tercet(
                verses=current_verses,
                number=current_tercet_num
            ))
        
        return tercets
    
    def _tokenize_verse(
        self, 
        text: str, 
        verse_num: int = 0,
        tercet_num: int = 0,
        position_in_tercet: int = 0
    ) -> Verse:
        """
        Tokenize a single verse.
        
        Args:
            text: Verse text
            verse_num: Verse number in the canto
            tercet_num: Tercet number
            position_in_tercet: Position in the tercet (1-3)
            
        Returns:
            Verse object with tokens
        """
        raw_tokens = self.TOKEN_PATTERN.findall(text)
        
        tokens = []
        for i, raw in enumerate(raw_tokens):
            # Skip isolated punctuation for now
            if raw in self.PUNCTUATION:
                continue
                
            normalized = None
            if self.normalize and self._normalizer:
                normalized = self._normalizer.normalize_word(raw)
            
            token = Token(
                text=raw,
                normalized=normalized,
                position=i,
                verse_num=verse_num,
                tercet_num=tercet_num
            )
            tokens.append(token)
        
        return Verse(
            text=text,
            tokens=tokens,
            number=verse_num,
            tercet=tercet_num,
            position_in_tercet=position_in_tercet
        )


# =============================================================================
# Convenience Functions
# =============================================================================

def tokenize_verse(text: str, normalize: bool = True) -> List[Token]:
    """
    Tokenize a single verse (convenience function).
    
    Args:
        text: Verse text
        normalize: Whether to apply normalization
        
    Returns:
        List of Token objects
    """
    tokenizer = TerzinaTokenizer(normalize=normalize)
    verse = tokenizer._tokenize_verse(text)
    return verse.tokens


def tokenize_canto(filepath: str | Path) -> List[Tercet]:
    """
    Tokenize an entire canto from file (convenience function).
    
    Args:
        filepath: Path to the file
        
    Returns:
        List of Tercet objects
    """
    tokenizer = TerzinaTokenizer()
    return tokenizer.tokenize_file(filepath)


# =============================================================================
# Demo/Test
# =============================================================================

if __name__ == "__main__":
    # Test on an iconic verse
    test_verse = "Nel mezzo del cammin di nostra vita"
    tokens = tokenize_verse(test_verse)
    
    print("=" * 60)
    print("TOKENIZER TEST - First verse of Inferno")
    print("=" * 60)
    print(f"Verse: {test_verse}")
    print(f"Tokens: {tokens}")
    print()
    
    # Test on verse with elisions
    test_elision = "ché la diritta via era smarrita"
    tokens_elision = tokenize_verse(test_elision)
    
    print(f"Verse with elision: {test_elision}")
    print(f"Tokens: {tokens_elision}")
