# Computational Emotion Detection in Inferno Canto I
## Technical Documentation for Dante Emotion Analysis

---

## 1. Introduction

This document presents the computational analysis of emotions in Dante Alighieri's *Inferno* (Canto I). The goal is not to replace traditional literary interpretation, but to **complement** it with quantitative tools that reveal emotional patterns across the text.

### 1.1 Objective
Track the **emotional evolution** of Canto I through computational methods, comparing:
- A **Lexicon-based** approach (transparent and interpretable)
- A **Zero-Shot NLI** approach (AI-powered logical inference)

### 1.2 Methodological Innovation
This project overcomes the limitations of traditional classification by adopting a **Natural Language Inference (NLI)** paradigm: instead of labeling text based on keywords, we query the model about the truth of interpretive hypotheses (e.g., *"Is it true that this verse expresses bewilderment?"*). This captures deep semantic nuances even without Dante-specific training.

---

## 2. Methodology

### 2.1 Text Analyzed
- **Source**: Inferno Canto I (136 verses, 46 tercets)
- **Structure**: Analysis by tercet (minimum narrative unit)
- **Edition**: Petrocchi critical edition

### 2.2 Method 1: Lexicon-Based Analysis

**How it works**:
1. Start with a dictionary of words associated with emotions
2. For each tercet, count words belonging to each emotional category
3. Calculate emotional intensity as proportion of emotional words to total

**Categories used** (Dante-specific adaptation):
- Fear (*Paura*)
- Sadness (*Tristezza*)
- Anger (*Rabbia*)
- Hope (*Speranza*)
- Bewilderment (*Smarrimento*) - Custom category for Dante

**Advantages**:
- Fully transparent: every classification can be verified
- Adaptable: we included Dante-specific vocabulary ("selva", "smarrita", "lupa")

**Limitations**:
- Cannot capture context (negation inverts meaning)
- Misses semantic nuances and metaphors
- Fails when emotions are expressed implicitly

### 2.3 Method 2: Zero-Shot NLI

**Model**: `mDeBERTa-v3-base-mnli-xnli` (Multilingual DeBERTa trained on NLI tasks)

**How it works**:
1. For each text window (2 tercets), we construct hypotheses: *"This text expresses [emotion]"*
2. The model computes entailment probability for each emotion
3. Results are aggregated across a sliding window for narrative continuity

**Key Innovation**: 
- **Zero-Shot** means no fine-tuning on Dante was required
- The model applies universal logical reasoning to medieval Italian
- Captures implicit emotions through semantic inference

**Advantages**:
- Understands metaphorical and allegorical language
- Detects emotions not explicitly named in text
- Handles archaic vocabulary through multilingual training

---

## 3. Technical Implementation

### 3.1 Sliding Window Analysis
- **Window Size**: 2 tercets (6 verses)
- **Overlap**: 1 tercet (creates narrative continuity)
- **Total Windows**: 45 analysis points across Canto I

### 3.2 Text Normalization
A custom `normalizer.py` script modernizes archaic orthography:
- `ch'i'` → `che io` (elision expansion)
- `avea` → `aveva` (verb modernization)
- `huomo` → `uomo` (Latin spelling removal)

**Note**: Normalization is essential for Lexicon (which requires exact matches) but accessory for NLI (which handles variation natively).

### 3.3 Emotion Categories
| Emotion | Italian | Literary Function in Canto I |
|---------|---------|------------------------------|
| Fear | Paura | Dark forest, beasts encounters |
| Bewilderment | Smarrimento | Opening crisis, spiritual loss |
| Hope | Speranza | Illuminated hill, Virgil's promise |
| Anger | Rabbia | The lion's aggression |
| Sadness | Tristezza | Existential suffering |

---

## 4. Results

### 4.1 Lexicon vs NLI Comparison

| Narrative Moment | Lexicon Result | NLI Result | Ground Truth |
|------------------|----------------|------------|--------------|
| Dark Forest (T1-5) | Low signal | **Bewilderment** peak | ✅ Fear/Bewilderment |
| Illuminated Hill (T6-8) | Silence | **Hope** peak | ✅ Hope |
| Three Beasts (T11-20) | Fear only | Fear + **Anger** | ✅ Mixed emotions |
| Virgil Appears (T22+) | Low signal | Hope rising | ✅ Redemption arc |

### 4.2 Key Finding
The NLI model successfully identifies the *"objective correlative"* (T.S. Eliot): when Dante describes the sun's rays on the hill, the model infers **Hope** even though the word never appears. The Lexicon, constrained to explicit keywords, remains silent.

### 4.3 Anger Detection
The model detected **Anger** peaks at tercets 20-21, corresponding to the *"bestia sanza pace"* (the relentless she-wolf). This captures the beast's aggression through semantic inference rather than keyword matching.

---

## 5. Visualization

The analysis produces:
- **Emotion Evolution Curve**: Smoothed line plot showing all 5 emotions across 46 tercets
- **Intensity Heatmap**: "Semantic barcode" revealing emotional density patterns
- **Event Markers**: Key narrative moments annotated on the timeline

---

## 6. Conclusion

This computational analysis demonstrates that **Zero-Shot NLI** significantly outperforms traditional lexicon-based methods for literary emotion detection, particularly for:
- Historical texts with archaic vocabulary
- Metaphorical and allegorical content
- Implicit emotional expression

The approach positions AI not as a replacement for the literary critic, but as a *"telescope"* that reveals patterns invisible to close reading alone.

---

## 7. Technical Stack

- **Model**: HuggingFace `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`
- **Framework**: PyTorch, Transformers
- **Visualization**: Matplotlib, Seaborn
- **Text Processing**: Custom TerzinaTokenizer

---

## References

- Alighieri, D. (c. 1320). *Divina Commedia* (Petrocchi critical edition)
- Laurer, M. et al. (2022). mDeBERTa for Cross-lingual NLI
- Moretti, F. (2013). *Distant Reading*
- Ekman, P. (1992). Basic Emotions Theory
