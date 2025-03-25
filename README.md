File Renamer
============

<p align="left">
  <img src="https://github.com/Axel0689/file_renamer/blob/c586a1b64cff37f024cfe484938689021576eed0/assets/icon.png", width="400" height="400">
</p>

App desktop per rinominare file in modo personalizzato.

Funzionalità
------------

- Seleziona più file
- Aggiungi un prefisso
- Scegli un modello (es: {prefix}_{counter}_{basename}{ext})
- Imposta il numero di zeri nel contatore
- Scegli il formato data
- Vedi anteprima dei nuovi nomi
- Rinomina i file direttamente

Placeholder disponibili
-----------------------

- {original} → nome originale
- {basename} → nome senza estensione
- {counter} → contatore numerico
- {prefix} → prefisso personalizzato
- {date} → data corrente
- {ext} → estensione del file

Esempio modello
---------------

{prefix}_{date}_{counter}{ext}

Requisiti
---------

- Python 3
- PyQt5

Installa le dipendenze:

    pip install pyqt5

Avvio
-----

    python file_renamer.py

Esecuzione da file .exe
-----------------------

È possibile usare anche la versione `.exe` senza Python installato, presente in RELEASE.

Autore
------

Alessandro Bagnuoli  
GitHub: @axel0689
