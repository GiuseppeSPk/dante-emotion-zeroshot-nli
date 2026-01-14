# 🎓 Guida alla Presentazione: Reverse Engineering d'Analisi

Questo documento serve per coinvolgere l'aula e spiegare come l'AI "ragiona" sul testo dantesco.

---

## 🌲 CASO 1: L'Incipit e lo Smarrimento (Terzine 1-2)

### 1. Il Testo (Originale)
> Nel mezzo del cammin di nostra vita  
> mi ritrovai per una selva oscura,  
> ché la diritta via era smarrita.  
> 
> Ahi quanto a dir qual era è cosa dura  
> esta selva selvaggia e aspra e forte  
> che nel pensier rinova la paura!

### 2. Il Testo (Normalizzato)
*(da qui è passato python - Normalizzazione Ortografica)*  
> Nel mezzo del **cammino** di nostra vita  
> mi ritrovai per una selva oscura,  
> **perché** la diritta via era smarrita.  
> 
> Ahi quanto a **dire** **quale** era è cosa dura  
> **questa** selva selvaggia e aspra e forte  
> che nel **pensiero** **rinnova** la paura!

---

### 🗣️ Domande per l'Aula (Interazione)
1. **Analisi Lessicale**: "Quale emozione vi trasmette questa terzina? Quali parole singole vi colpiscono di più?" *(Keywords: oscura, smarrita, paura)*
2. **Analisi Logica**: "È vero che in questa terzina possiamo riscontrare uno stato di **Paura** o **Smarrimento**?" *(Domanda posta come ipotesi NLI)*

---

### 📊 Risultato del Triplo Confronto
| Osservatore | Etichetta Assegnata | Spiegazione (Reverse Engineering) |
| :--- | :--- | :--- |
| **Modello Base (Social)** | 🔴 **TRISTEZZA** | Errore di dominio. Sui social "oscura" e "smarrita" sono filtrate come malinconia/tristezza. |
| **Modello NLI (Logica)** | 🟢 **SMARRIMENTO** | Vittoria della logica. Il modello non guarda solo le parole, ma capisce che "selva + via smarrita" implica l'ipotesi "Smarrimento". |
| **Noi (Umani)** | 🟢 **PAURA / SMARRIMENTO** | Interpretazione allegorica dello stato di peccato e terrore fisico. |

---
---

## ☀️ CASO 2: Il Colle e la Speranza (Terzine 5-6)

### 1. Il Testo (Originale)
> Ma poi ch'i' fui al piè d'un colle giunto,  
> là dove terminava quella valle  
> che m'avea di paura il cor compunto,  
> 
> guardai in alto e vidi le sue spalle  
> vestite già de' raggi del pianeta  
> che mena dritto altrui per ogne calle.

### 2. Il Testo (Normalizzato)
*(da qui è passato python - Normalizzazione Ortografica)*  
> Ma poi **che** **io** fui al **piede** d'un colle giunto,  
> là dove terminava quella valle  
> che **mi** **aveva** di paura il **cuore** compunto,  
> 
> guardai in alto e vidi le sue spalle  
> vestite già **dei** raggi del pianeta  
> che mena dritto altrui per **ogni** calle.

---

### 🗣️ Domande per l'Aula (Interazione)
1. **Analisi Lessicale**: "Qui compare la parola 'paura'. È ancora questa l'emozione dominante o il quadro è cambiato?"
2. **Analisi Logica**: "È vero che in questa terzina possiamo riscontrare dell'ottimismo o della **Speranza**?" *(Ipotesi: Raggi del sole = Speranza?)*

---

### 📊 Risultato del Triplo Confronto
| Osservatore | Etichetta Assegnata | Spiegazione (Reverse Engineering) |
| :--- | :--- | :--- |
| **Modello Base (Social)** | 🔴 **PAURA / NEUTRALE** | Il modello "inciampa" sulla parola *paura* (v. 28) e non capisce il valore simbolico dei *raggi del pianeta*. |
| **Modello NLI (Logica)** | 🟢 **SPERANZA** | Il modello associa semanticamente la luce e l'ascesa al concetto di Speranza, ignorando il rumore lessicale della parola "paura" passata. |
| **Noi (Umani)** | 🟢 **SPERANZA / RIFUGIO** | Il colle illuminato come prima possibilità di salvezza. |

---

## 📈 Performance Generale sul Primo Canto

La differenza di performance tra i due approcci non è solo qualitativa, ma quantitativa:

*   **Gap Linguistico (Vocabolario)**:
    - **Modello Base (Social)**: **5.7%** di parole sconosciute (UNK). Il modello "non vede" termini arcaici essenziali.
    - **Modello NLI (mDeBERTa)**: **< 1%** di parole sconosciute. La tokenizzazione "sub-word" multilingua permette di gestire perfettamente il volgare dantesco.
*   **Affidabilità Interpretativa**:
    - Il **Lexicon** (Dizionario) ha bisogno che la parola sia scritta esplicitamente (es. "paura").
    - L'**NLI** riconosce la **Speranza** anche quando Dante usa una metafora (i "raggi del pianeta").

---

## �️ Gestione dei Dataset e Pre-processing

Per ottenere questi risultati, abbiamo gestito tre tipologie di dati:

### 1. Il Corpus d'Analisi (Input)
*   **Dato**: Inferno, Canto I (Edizione critica Petrocchi).
*   **Trattamento**: 
    - **Tokenizzazione Metrica**: Il testo è stato diviso in **terzine** (46 unità) rispettando la struttura originale.
    - **Sliding Window**: Le terzine sono state analizzate in gruppi di 2 (finestra scorrevole) per mantenere il contesto sintattico (e.g., il soggetto di una terzina che agisce nella successiva).
    - **Normalizzazione**: Passaggio obbligatorio per 'avvicinare' Dante all'italiano moderno dei modelli (e.g., *avea* → *aveva*).

### 2. Il Lexicon Emozionale (Baseline)
*   **Dato**: `italian_emotions.json` (Dizionario proprietario).
*   **Trattamento**: Abbiamo personalizzato un dataset standard aggiungendo categorie specifiche dantesche (**Smarrimento**, **Speranza**) e mappando keyword arcaiche direttamente nel JSON (*oscura, perigliosa, smarrita*).

### 3. I Dati di Addestramento del Modello (Intelligence)
*   **Dato**: Dataset **MNLI** (Multi-Genre NLI) e **XNLI** (Cross-lingual NLI).
*   **Utilizzo**: Questi sono i milioni di esempi di "ragionamento logico" su cui è stato pre-addestrato il modello `mDeBERTa`. 
    - Grazie a questi dataset, il modello non ha bisogno di conoscere Dante in anticipo (Zero-Shot); conosce già come la lingua italiana esprime logicamente un'emozione.

---

## �🔑 La Chiave del Progetto: Perché l'NLI?

### Cos'è l'NLI (Natural Language Inference)
Tecnicamente, non stiamo facendo "Sentiment Analysis" ma **Entailment** (Implicazione Logica).
Data una *Premessa P* (la terzina) e un'*Ipotesi H* ("Questo testo esprime Speranza"), il modello calcola quanto la premessa **comporta** logicamente l'ipotesi.

### Cosa ci permette di fare (Il Succo)
1.  **Tecnicamente**: Superiamo il bisogno di un dataset di addestramento su testi medievali. Usiamo la **logica universale** del linguaggio invece della statistica delle parole.
2.  **Risultato**: Riusciamo a mappare emozioni **implicite**. Dante non è un utente Twitter che usa emoji; Dante usa il **Correlativo Oggettivo**. La luce *è* speranza, la selva *è* smarrimento. L'NLI è l'unico strumento in grado di "leggere tra le righe" di queste metafore secolari.

