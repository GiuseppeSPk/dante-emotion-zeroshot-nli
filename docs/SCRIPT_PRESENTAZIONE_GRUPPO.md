# 🎓 Script di Presentazione Bilanciato: Dante Emotion Analysis
**Tempo Totale:** 20 minuti circa (6-7 min per ogni relatore)
**Struttura:** 3 Slide a testa (Totale 9 Slide)

---

## 🎤 PARTE 1: Introduzione e Inquadramento (Agata)

### Slide 1: Dante Alighieri e l'Universo della "Commedia"
*   **Profilo dell'Autore**: Dante (1265-1321) è il pilastro della letteratura italiana e l'architetto del volgare.
*   **Il Catalizzatore**: L'esilio (1302) come missione di salvezza universale che genera l'opera.
*   **Nobilitazione del Volgare**: Elevare la lingua quotidiana per trattare i temi più alti dello scibile umano.

### Slide 2: L'Architettura del Viaggio e il Labirinto Emotivo
*   **La Struttura**: 100 canti in terzine incatenate. Un realismo sensoriale che invita all'analisi dei dati.
*   **Il Prologo (Canto I)**: Inizia *in medias res* nella "selva oscura". 
*   **Simboli Emotivi**: La **Paura** del naufrago, la **Speranza** del colle illuminato, il **Terrore** delle tre fiere. Trasformiamo l'esegesi tradizionale in analisi basata sui dati.

### Slide 3: Dagli Archivi Digitali alla Distant Reading
*   **Stato dell'Arte**: Citare *The Dartmouth Dante Project* (commentari) e *Digital Dante* (fruizione multimediale). 
*   **Distant Reading**: Passiamo dalla lettura ravvicinata alla "lettura a distanza" usando algoritmi per pattern non visibili a occhio nudo (conferma statistica dalle intuizioni).
*   **La Geografia delle Parole (Word Embeddings)**: Immaginiamo ogni parola come un punto in una mappa 3D. Possiamo calcolare matematicamente la "vicinanza" semantica tra concetti (es: quanto "paura" è vicina a "selva" nel sistema di Dante).
*   **📊 Visualizzazione: [Voyant Tools - Word Cloud]**: Una "istantanea" statistica delle frequenze lessicali del Canto I. È il primo livello della Distant Reading: il testo trattato come un insieme di dati (Bag of Words).

---

## 💻 PARTE 2: Logica e Risultati (Tecnico - Giuseppe)

### Slide 4: Sentiment Analysis ed Emotion Detection (Baseline)
*   **L'Obiettivo**: Mappare l'intensità emotiva delle **terzine** dantesche (unità minima della narrazione).
*   **Il Metodo Lessicale (Dizionario)**: Il nostro punto di partenza. Un sistema che scansiona le parole all'interno di ogni **terzina** e le confronta con un database. (Vedi: `data/emotion_lexicons/italian_emotions.json`).
*   **Le 5 Emozioni Cardine**: Sono state scelte categorie che mappano il "viaggio" del Canto I:
    - **Paura e Smarrimento**: Lo stato psicologico e morale della selva.
    - **Speranza**: Il motore narrativo scatenato dalla vista del colle.
    - **Rabbia**: L'aggressività delle tre fiere che sbarrano la strada.
    - **Tristezza**: La sofferenza esistenziale dell'incipit.
*   **Il Limite**: Molto trasparente ma rigido: se Dante non usa termini esatti, il dizionario non "vede".
*   **📊 Visualizzazione: [lexicon_curve.png]**: Questo è il nostro punto di partenza. Il grafico rappresenta la **frequenza puramente statistica** di parole chiave emotive. Se una terzina contiene la parola "paura", la curva sale; se l'emozione è espressa tramite una metafora o un'immagine (come la luce sul colle), la curva resta piatta. È la fotografia del limite del dizionario: vede le parole, ma non il significato.

### Slide 5: Transformers e Zero-Shot NLI (L'Analisi Logica)
*   **Il salto tecnologico**: Usiamo **mDeBERTa-v3**, un modello che non conta parole isolate ma esegue **inferenze logiche (NLI)** in modalità **Zero-Shot**.
*   **L'Analogia**: Il modello è come un "lettore estremamente attento" che analizza il contesto dell'intera terzina.
*   **L'Unità di Analisi**: Non analizziamo versi singoli, ma **blocchi di 2 terzine** alla volta (Sliding Window). Questo permette all'AI di avere il contesto necessario per capire le metafore.
*   **Natural Language Inference**: Non chiediamo all'AI di "etichettare", ma poniamo domande: *"È vero che questa finestra di testo implica Speranza?/Paura?/Tristezza?/Rabbia?/Smarrimento?", ogni emozione viene passata come parametro per ogni terzina analizzata. Superando così il database rigido dei social.

### Slide 6: Risultati Finali: La Logica NLI in Azione
*   **📊 Visualizzazione: [zeroshot_curve.png] e [Heatmap]**: Qui mostriamo la visione d'insieme del Canto I.
*   **Il Racconto Emotivo**: La curva dell'NLI analizza tutti i 46 punti narrativi, creando un grafico fluido che segue l'evoluzione psicologica del protagonista.
*   **Riempire i Silenzi**: Notate come l'IA trovi il senso profondo anche dove il dizionario restava "muto".
*   **Heatmap di Intensità**: Una "istantanea" visiva che evidenzia le zone di massima tensione emotiva del Canto.
*   **Conclusione Tecnica**: Il modello ha mappato con successo il Canto I, validando l'efficacia dell'approccio Zero-Shot.

---

## 🏁 PARTE 3: Strategia e Casi Studio (Rebecca)

### Slide 7: Bias del Moderno e Normalizzazione Ortografica
*   **Il Problema**: L'AI è addestrata sull'italiano di oggi. Forme come "avea" o "et" sono "rumore".
*   **Lo Script custom (`normalizer.py`)**: Abbiamo creato un ponte che modernizza il testo. Alcuni esempi reali:
    - **Elisioni**: *ch'i'* → *che io*; *perch'io* → *perché io*
    - **Forme Verbali**: *avea* → *aveva*; *fea* → *faceva*
    - **Grafie Latine**: *huomo* → *uomo*; *et* → *e*
    - **Lessico Arcaico**: *pièta* → *pietà*; *ogne* → *ogni*
*   **Perché lo facciamo?** 
    *   Per il **Dizionario** è vitale (altrimenti non trova nulla). 
    *   Per l'**AI** è accessorio (lei capisce anche l'originale). 
    *   Lo usiamo su entrambi per un **confronto scientifico onesto**.

### Slide 8: Caso Studio 1 - La Selva e lo Smarrimento (Interattiva)
*   **Testo**: *"Nel mezzo del cammin..."*
*   **Domanda all'Aula**: *"Quale emozione vi trasmette questa terzina? Paura o Smarrimento?"*
*   **Reverse Engineering**: 
    *   Il **Modello Social** sbaglia e dice *Tristezza*. 
    *   L'**NLI** indovina e dice *Smarrimento*. 
    *   **Perché?** L'AI capisce la logica situazionale del perdersi, non solo le parole singole.

### Slide 9: Caso Studio 2 e Conclusioni
*   **Testo**: *"vidi le sue spalle vestite già de' raggi del pianeta..."*
*   **Domanda all'Aula**: *"Qui non compare la parola Speranza. Come fa l'AI a trovarla?"*
*   **Il Risultato**: L'AI riconosce il **Correlativo Oggettivo**: Luce = Speranza.
*   **Conclusione Finale**: La tecnologia non sostituisce il critico, ma diventa il suo "cannocchiale". Gli LLM del futuro allineeranno Dante alle tecnologie d'avanguardia.
