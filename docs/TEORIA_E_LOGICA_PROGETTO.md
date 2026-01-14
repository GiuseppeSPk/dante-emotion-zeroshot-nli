# 🧠 Guida Teorica e Metodologica: Dante Emotion Analysis

Questo documento riassume la logica del progetto per permetterti di padroneggiare ogni scelta tecnica durante la discussione d'esame.

---

## 1. Il Ruolo del Dataset Originale (MNLI/XNLI)

**Il concetto chiave:** Non tutti i modelli IA sono uguali.
*   **Modelli Social (Es. FEEL-IT):** Sono addestrati su dataset di Twitter per imparare i label *"Gioia"* o *"Rabbia"*. Se non trovano parole moderne o hashtag, falliscono.
*   **Modello NLI (mDeBERTa):** È addestrato su dataset chiamati **MNLI (Multi-Genre NLI)** e **XNLI (Cross-lingual NLI)**. Questi dataset insegnano al modello la **LOGICA UNIVERSALE**, non le emozioni.

### I Label originali del modello
Il modello `mDeBERTa` è nato per classificare tre stati logici tra due frasi:
1.  **Entailment (Consegue)**: La frase A implica la frase B.
2.  **Neutral (Irrilevante)**: La frase A non dice nulla sulla frase B.
3.  **Contradiction (Contraddice)**: La frase A nega la frase B.

**La nostra scelta:** Sfruttiamo questa capacità di "ragionamento" per testare le emozioni senza aver mai addestrato il modello su Dante. Questo trasforma il modello da semplice classificatore a **Critico Logico**.

---

## 2. Il Paradigma "Zero-Shot": Dalla Statistica alla Logica

Nel progetto, abbiamo abbandonato la "Sentiment Analysis" tradizionale per l'approccio **Zero-Shot NLI**.

### Come funziona nel codice:
Data una terzina (**Premessa P**), il codice genera delle ipotesi (**Ipotesi H**) usando le **nostre categorie dantesche**:
*   **H1**: *"Questo testo esprime Paura"*
*   **H2**: *"Questo testo esprime Smarrimento"*
*   **H3**: *"Questo testo esprime Speranza"*

**Criterio di Judgement:** Il modello calcola il punteggio di **Entailment** per ogni ipotesi. 
> *Se il modello stabilisce che la terzina "implica logicamente" l'ipotesi "Speranza", noi usiamo quel punteggio di verità come misura dell'intensità emotiva.*

**Perché è rivoluzionario?** Perché ci permette di creare label personalizzati (come "Smarrimento") che non esistono in nessun dataset standard di IA, ma che il modello riconosce grazie alla sua comprensione profonda della lingua.

---

## 3. L'AI come Critico: Perché queste ipotesi e non "tutto"?

Hai sollevato un dubbio fondamentale: *"Perché solo queste emozioni? Non stiamo perdendo sfumature? Perché non far giudicare a mDeBERTa la risposta del modello Twitter?"*

### A. Selezione vs Rumore (Il "Mondo Chiuso")
In informatica, aggiungere etichette all'infinito (es. 100 emozioni diverse) non aumenta la precisione, ma il **rumore**. 
*   **Problema**: Se chiediamo a un modello se un testo esprime "nostalgia del passato", "malinconia senile" o "tristezza", i punteggi si divideranno tra queste categorie simili, rendendo il grafico illeggibile.
*   **Scelta**: Abbiamo selezionato un **Set Chiuso di 5 Pivot** (Paura, Smarrimento, Speranza, Rabbia, Tristezza) che fungono da "Ancore Narrative". Ogni altra sfumatura viene "attratta" verso l'ancora più vicina. È una scelta di **Pertinenza Letteraria**.

### B. mDeBERTa come "Giudice" dei Modelli Social
Potremmo effettivamente chiedere a mDeBERTa: *"È vero che questa terzina esprime Tristezza (come dice il modello Twitter)?"*. 
*   **Nel Progetto**: Lo abbiamo fatto implicitamente. Analizzando il testo con le due metodologie (Lexicon vs NLI), abbiamo "messo in tribunale" il modello Twitter. 
*   **La Prova**: Se il modello Twitter dice "Tristezza" e il nostro NLI assegna 0.90 a "Paura" e 0.05 a "Tristezza", abbiamo ottenuto la **validazione empirica dell'errore**. Non serve che l'AI parli col modello Twitter; i dati mostrano che la logica (NLI) batte la statistica (Twitter).

---

## 4. Scelte Tecniche: Perché proprio mDeBERTa?

Abbiamo selezionato **mDeBERTa-v3** non per caso, ma per tre caratteristiche tecniche "fuoriclasse":

1.  **Disentangled Attention**: A differenza del BERT classico, separa il contenuto della parola dalla sua posizione. Questo permette al modello di gestire bene la sintassi poetica dantesca (iperbati, inversioni), che confonderebbe modelli più semplici.
2.  **Multilinguismo (m-)**: Essendo stato addestrato su centinaia di lingue (incluso il latino e l'italiano), il modello possiede una "mappa semantica" che include radici arcaiche. Questo gli permette di capire Dante meglio di un modello addestrato solo sull'italiano di oggi.
3.  **Sub-word Tokenization**: Se il modello non conosce una parola specifica (es. *pièta*), non si blocca ma la scompone in frammenti (token). Spesso la radice di un frammento è sufficiente per attivare la logica NLI.

---

## 5. Il Ruolo della Normalizzazione (`normalizer.py`): Due Pesi e Due Misure

Un punto cruciale della nostra metodologia è l'uso differenziato della pulizia del testo tra i due studi:

### A. Fondamentale per l'Analisi Lessicale (Dizionario)
L'approccio lessicale è un sistema di **"cerca e conta"**. Se nel dizionario abbiamo "paura" e Dante scrive "paura", il sistema lo conta. Ma se scrive "avea" (invece di "aveva") o "et" (invece di "e"), il dizionario fallisce perché cerca una corrispondenza esatta delle lettere.
*   **Risultato**: Qui la normalizzazione è **vitale**. Senza di essa, il grafico lessicale sarebbe piatto e privo di dati reali (falsi negativi).

### B. Accessoria per l'AI (mDeBERTa)
Grazie alla potenza dei Transformer e alla sub-word tokenization citata sopra, mDeBERTa è in grado di processare il **testo originale**. La sua capacità logica gli permette di "superare" gli arcaicismi ortografici intuendo il senso.
*   **Risultato**: Abbiamo mantenuto lo script di normalizzazione non perché fosse obbligatorio per l'IA, ma per garantire un **confronto onesto** e scientifico tra i due metodi, permettendo al Dizionario di "giocare al massimo delle sue potenzialità".

---

## 6. Perché questa è una "Analisi Superiore"?

Se il professore ti chiede: *"Perché non hai usato un semplice dizionario o un modello già pronto (es. FEEL-IT)?"*, la tua risposta deve essere:

1.  **LOGICA > STATISTICA**: I modelli come FEEL-IT (Sentiment classico) sono schiavi del dominio Twitter. L'NLI usa l'inferenza logica universale.
2.  **ADATTAMENTO Ermeneutico**: Abbiamo creato i nostri label (Smarrimento, Speranza) iniettando sensibilità letteraria in un motore di logica pura.
3.  **GESTIONE DEL CONTESTO**: La nostra *Sliding Window* di 2 terzine permette di catturare emozioni che nascono in un verso e terminano nel successivo, cosa impossibile per un'analisi parola-per-parola.

---

## 🔑 La tua linea difensiva in 3 concetti:
1.  **LOGICA > STATISTICA**: Usiamo l'inferenza (NLI) invece del semplice conteggio di parole.
2.  **CONTESTO > ETICHETTA**: La sliding window preserva la narrazione dantesca.
3.  **ADATTAMENTO > RIGIDITÀ**: La normalizzazione aiuta il passato (Dizionario) a parlare col presente, mentre l'IA (DeBERTa) usa la logica per colmare il gap.
