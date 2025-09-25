File Renamer
============
<p align="left">
  <img src="https://github.com/Axel0689/file_renamer/blob/c586a1b64cff37f024cfe484938689021576eed0/assets/icon.png", width="400" height="400">
</p>

> App desktop per rinominare file in modo personalizzato con estensione automatica.

&nbsp;

Funzionalità
------------
- Seleziona più file
- Aggiungi un prefisso personalizzato
- Scegli un modello (es: `{prefix}_{counter}_{basename}`) 
- **✨ Estensione mantenuta automaticamente** - Non serve più aggiungere `{ext}` manualmente
- Imposta il numero di inizio contatore
- Imposta il numero di zeri nel contatore  
- Scegli il formato data tra 5 opzioni disponibili
- Vedi anteprima in tempo reale dei nuovi nomi
- Rinomina i file direttamente con conferma
- Supporto per temi Dark/Light
- Barra di stato con feedback operazioni

Placeholder disponibili
-----------------------
| Placeholder | Descrizione | Esempio |
|-------------|-------------|---------|
| `{original}` | Nome base senza estensione | `documento` |
| `{basename}` | Nome base senza estensione | `documento` |
| `{counter}` | Contatore numerico con zeri prefissati | `001`, `002` |
| `{prefix}` | Prefisso personalizzato dal campo input | `MyPrefix` |
| `{date}` | Data formattata secondo le opzioni | `2025-09-25` |
| ~~`{ext}`~~ | ~~Estensione del file~~ | **Gestita automaticamente** ✅ |

Esempio modello
---------------
**Prima (v0.1):**
```
{prefix}_{date}_{counter}{ext}
```

**Ora (v0.2):**
```
{prefix}_{date}_{counter}
```
*L'estensione viene aggiunta automaticamente!*

**Risultato finale:** `MyPrefix_2025-09-25_001.pdf`

Formati data disponibili
------------------------
- `AAAA-MM-GG` → `2025-09-25`
- `GG-MM-AAAA` → `25-09-2025`
- `ISO 8601` → `20250925`
- `MM/GG/AAAA` → `09/25/2025`
- `Custom` → Formato personalizzato

Requisiti
---------
- Python 3.6+
- PyQt5

Installa le dipendenze:
```bash
pip install pyqt5
```

Avvio
-----
```bash
python rename_app.py
```

Esecuzione da file .exe
-----------------------
È possibile usare anche la versione `.exe` senza Python installato, presente in **RELEASES**.

Screenshots
-----------
*Anteprima dell'interfaccia con tema dark/light disponibili*

Updates
-------
- ${\color{red}(25.09.2025)}$
  - **${\color{green}v0.2 (Release 2)}$**
    - ✨ **Estensione automatica**: Non serve più specificare `{ext}` nel pattern
    - 🔄 **Placeholder aggiornati**: `{original}` ora restituisce solo il nome senza estensione
    - 🎨 **UI migliorata**: Placeholder aggiornato con indicazione dell'estensione automatica
    - 📋 **Menu Insert**: Rimosso `{ext}` dal menu dropdown
    - 🐛 **Coerenza**: `{original}` e `{basename}` ora sono identici

- ${\color{red}(25.03.2025)}$
  - **${\color{green}v0.1 (Release 1)}$**
    - 🚀 Prima versione con tutte le funzionalità base

Roadmap
-------
- [ ] Supporto per regex nei pattern
- [ ] Batch processing migliorato
- [ ] Undo/Redo delle operazioni
- [ ] Salvataggio template personalizzati
- [ ] Supporto drag & drop

Contributing
------------
Contributi benvenuti! Apri una issue o pull request per suggerimenti e miglioramenti.

Licenza
-------
MIT License - Vedi file `LICENSE` per dettagli.

Autore
------
**Alessandro Bagnuoli**  
GitHub: [@axel0689](https://github.com/axel0689)

---
⭐ Lascia una stella se il progetto ti è utile!
