# PROMPT PER GAMMA AI: Progetto Dante Emotion Analysis

Copia e incolla il testo sottostante in Gamma AI utilizzando l'opzione **"Text to Presentation"**.

---

# Titolo: Dante Emotion Analysis: Il Viaggio di mDeBERTa nell'Inferno
**Sottotitolo:** Tra Letteratura e Intelligenza Artificiale Zero-Shot
**Tema suggerito:** Moderno, Accademico, Toni scuri con accenti oro/neon (Stile Dantesco Tecnologico)

---

## Slide 1: Dante Alighieri e l'Architettura della Commedia (Agata)
*   **Contesto**: Dante (1265-1321), padre della lingua italiana.
*   **Il Catalizzatore**: L'esilio come missione di salvezza universale.
*   **Visione**: Elevare il volgare per esplorare l'animo umano.
*   **Visual suggerito**: Immagine di Dante o incisione antica della Commedia.

## Slide 2: Il Prologo: Il Labirinto Emotivo del Canto I (Agata)
*   **Incipit**: "Nel mezzo del cammin..." - un viaggio in medias res.
*   **Simboli**: La Selva (Smarrimento), il Colle (Speranza), le Fiere (Rabbia/Paura).
*   **Obiettivo**: Trasformare l'esegesi tradizionale in analisi computazionale dei dati.
*   **Visual suggerito**: Mappa dell'Inferno o rappresentazione della selva oscura.

## Slide 3: Dagli Archivi Digitali alla Distant Reading (Agata)
*   **Distant Reading**: Analisi di pattern non visibili a occhio nudo tramite algoritmi.
*   **Word Embeddings**: La "Geografia delle Parole". Mappatura matematica della vicinanza semantica (es. Selva vs Paura).
*   **Digital Humanities**: Il ponte tra filologia classica e computer science.
*   **Visual suggerito**: Diagramma astratto di cluster di parole o word cloud.

## Slide 4: Baseline: Il Metodo Lessicale (Giuseppe)
*   **Obiettivo**: Mappare l'intensità emotiva delle **terzine** (unità minima narrativa).
*   **Dizionario (Lexicon)**: Scansione meccanica di parole chiave emotive.
*   **Le 5 Emozioni Cardine**: Paura, Smarrimento, Speranza, Rabbia, Tristezza.
*   **📊 Risultato**: La curva del dizionario è "cieca" alle metafore e spesso tace.
*   **Visual suggerito**: Caricare l'immagine `lexicon_curve.png` o grafico a barre semplice.

## Slide 5: L'Analisi Logica: Transformers e Zero-Shot NLI (Giuseppe)
*   **La Svolta**: Utilizzo di **mDeBERTa-v3** per inferenze logiche.
*   **Zero-Shot**: Il modello non è addestrato su Dante, ma applica una logica universale.
*   - **Unità di Analisi**: Blocchi di 2 terzine (Sliding Window) per gestire il contesto.
*   **NLI in Azione**: Domande logiche: *"Questo testo implica Speranza/Paura?"*.
*   **Visual suggerito**: Icone di un cervello neurale o schema Transformers.

## Slide 6: Demo Dati Reali: La Vittoria dell'AI (Giuseppe)
*   **Dataset**: Analisi di 46 unità narrative.
*   **Successo**: L'AI riconosce la **Speranza** nel sole sul colle tramite il "correlativo oggettivo" (Luce = Speranza).
*   **📊 Visualizzazione**: Mostrare `zeroshot_curve.png` e la Heatmap dell'intensità emotiva.
*   **Visual suggerito**: Affiancare il grafico della curva e la heatmap.

## Slide 7: Bias del Moderno e Normalizzazione Ortografica (Rebecca)
*   **Gap Linguistico**: L'AI è addestrata sull'italiano del 2024, Dante scrive nel 1300.
*   **Il Ponte (`normalizer.py`)**: Modernizzazione del testo (es. *huomo* → *uomo*, *avea* → *aveva*).
*   **Ratio**: Essenziale per il Dizionario, accessoria per l'AI. Applicata a entrambi per onestà scientifica.
*   **Visual suggerito**: Tabella "Prima vs Dopo" con esempi di normalizzazione.

## Slide 8: Caso Studio 1: Lo Smarrimento nella Selva (Rebecca)
*   **Testo**: *"Nel mezzo del cammin di nostra vita..."*
*   **Sfida**: Paura o Smarrimento?
*   **Risultato**: I modelli social dicono "Tristezza" (Bias). L'NLI indovina "Smarrimento".
*   **Perché?**: L'AI capisce la logica del perdersi, non solo le singole parole "triste".
*   **Visual suggerito**: Split screen: Modello Social vs Modello NLI.

## Slide 9: Conclusioni e Orizzonti Future (Rebecca)
*   **Risultati**: Rilevamento di emozioni profonde e invisibili al dizionario.
*   **Visione**: L'AI come "cannocchiale" per il critico letterario, non come sostituto.
*   **Sguardo al Futuro**: LLM specifici per lingue antiche e filologia digitale.
*   **Visual suggerito**: Immagine simbolica di un libro antico connesso a circuiti digitali.
