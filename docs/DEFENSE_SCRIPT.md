# 🎓 Script per la Difesa Orale: Dante Emotion Analysis

Questo documento è strutturato per guidare l'esposizione orale. Non leggerlo parola per parola, ma usa i **punti in grassetto** come ancoraggi per la memoria.

---

## 1. Intro e Obiettivo (Il "Perché")
*“Buongiorno. Il mio progetto nasce da una domanda: **L'Intelligenza Artificiale moderna può davvero 'leggere' le emozioni di Dante, o si perde nel gap linguistico di 700 anni?**”*

*   **L'Obiettivo**: Non volevo solo "fare un grafico", ma misurare la distanza semantica tra l'italiano dantesco e i modelli NLP standard.
*   **Case Study**: Inferno, Canto I. Un testo denso di emozioni esistenziali (paura, smarrimento, speranza).

---

## 2. Roadmap Tecnica (Il "Come")
*“Ho approcciato il problema in due fasi: una classica e una sperimentale.”*

### Fase A: L'Approccio Classico (Lexicon-Based)
*   **Cosa ho fatto**: Ho creato un analizzatore basato su dizionario (`LexiconEmotionAnalyzer`).
*   **Problema Riscontrato**: Il metodo è "cieco". Se Dante scrive "la dove 'l sol tace" (sinestesia per "buio"), il dizionario vede la parola "sole" e potrebbe segnare Gioia/Luce, oppure vede "tace" e non segna nulla.
*   **Risultato**: Molti falsi negativi. È un metodo robusto ma superficiale.

### Fase B: Il Fallimento Iniziale (Sentiment Analysis Standard)
*   **Tentativo**: Ho provato a usare `FEEL-IT`, un modello BERT SOTA per l'italiano.
*   **La Scoperta Critica**: Il modello è addestrato su **Twitter**.
    *   Su Twitter, "Tristezza" è spesso associata a parole di solitudine/buio.
    *   Quando il modello legge "Selva Oscura", non capisce il contesto teologico di terrore, ma vede solo "buio/solitudine" e classifica come **Tristezza**.
    *   **Dato Empirico**: Il modello Twitter ha il **5.7%** di token sconosciuti (UNK) sul testo di Dante. Perde parole chiave come "fiso" o "soavi".

---

## 3. La Soluzione: Zero-Shot NLI (Il "Cuore del Progetto")
*“Per superare questo dominio mismatch, ho cambiato paradigma: dalla Classificazione all'**Inferenza Logica**.”*

*   **La Tecnica**: Zero-Shot Natural Language Inference (NLI).
*   **Il Modello**: `mDeBERTa-v3` (Multilingue).
*   **La Differenza**: Invece di chiedere *"Classifica questo testo"*, chiedo: *"È vero che questo testo implica Paura?"*.
*   **Perché funziona**: La logica semantica è più stabile del lessico. Il modello capisce che "selva oscura" *implica* pericolo (Paura), anche se non ha mai visto la parola "selva" su Twitter.

---

## 4. Analisi dei Risultati (I Dati Reali)
*“Mostrando i grafici generati, possiamo vedere la prova empirica di questo successo.”*

### Il Grafico Zero-Shot (`zeroshot_curve.png`)
*   **Incipit**: Vediamo un picco immediato di **PAURA** (linea rossa) e **SMARRIMENTO** (linea grigia). *Il modello ha corretto l'errore "Tristezza".*
*   **Il Colle (Versi 16-18)**: Qui accade la magia. Dante descrive il colle "vestito dei raggi del pianeta". Non dice "ho speranza".
    *   Tuttavia, il modello NLI mostra un picco netto di **SPERANZA** (linea ciano).
    *   *Interpretazione*: L'IA ha dedotto l'emozione dal contesto (Luce -> Speranza), cosa impossibile per il dizionario.
*   **Le Fiere**: Picchi alternati di **RABBIA** (arancione, le bestie) e **PAURA** (Dante).

### La Visualizzazione Heatmap (`zeroshot_heatmap.png`)
*   Questa "Heatmap a codice a barre" mostra la densità emotiva. Notate come la **Paura** è un rumore di fondo costante, interrotto solo dai flash di **Speranza** (il Colle, Virgilio).

---

## 5. Conclusioni e Criticità
*“In conclusione...”*

1.  **Vittoria Metodologica**: Abbiamo dimostrato empiricamente che per testi storici, i modelli di **Ragionamento (NLI)** sono superiori ai modelli di **Classificazione Social**.
2.  **Gap Linguistico**: Esiste ed è misurabile (quel 5.7% di parole perse nel modello Twitter).
3.  **Limite**: L'analisi richiede molta potenza di calcolo rispetto al dizionario, ma offre una profondità ermeneutica che giustifica il costo.

---

### ❓ Possibili Domande del Prof (E come rispondere)

**Q: Perché ha aggiunto "Speranza" e "Smarrimento"? Ekman non le include.**
A: *"Esatto. Le categorie di Ekman sono biologiche/facciali. Per Dante servivano categorie letterarie/esistenziali. 'Smarrimento' è la parola chiave del Canto I, ignorarla sarebbe stato un errore filologico."*

**Q: Sicuro che il modello NLI non stia "tirando a indovinare"?**
A: *"Ho validato i risultati: il picco di Speranza coincide esattamente con il verso del 'Colle illuminato'. Una coincidenza così precisa su anali semantica complessa è statisticamente improbabile."*

**Q: Perché non usare un modello addestrato sul volgare del '300?**
A: *"Esistono (es. BERToldo), ma richiedono fine-tuning specifico. Il mio obiettivo era testare se l'IA Generalista SOTA può colmare il gap da sola usando la logica. La risposta è sì."*
