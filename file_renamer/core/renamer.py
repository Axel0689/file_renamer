"""
Logica di rinomina pura — zero dipendenze Qt.
"""

import datetime
import os
import re

# Placeholder disponibili nel modo pattern, con la loro descrizione
PLACEHOLDERS = {
    "{original}": "Nome originale del file (senza estensione)",
    "{basename}": "Nome base senza estensione",
    "{counter}": "Contatore numerico con zeri prefissati",
    "{prefix}": "Prefisso personalizzato",
    "{date}": "Data corrente (formato selezionato)",
    # Metadata — disponibili solo se i pacchetti opzionali sono installati
    "{camera}": "Modello fotocamera (da EXIF)",
    "{location}": "Luogo (da GPS/metadata)",
    "{author}": "Autore (da PDF/documento)",
    "{resolution}": "Risoluzione video",
    "{duration}": "Durata media",
    "{ai_category}": "Categoria rilevata dall'AI",
}

# Placeholder base (sempre disponibili)
CORE_PLACEHOLDERS = ["{original}", "{basename}", "{counter}", "{prefix}", "{date}"]

# Placeholder metadata (richiedono pacchetti opzionali)
METADATA_PLACEHOLDERS = [
    "{camera}",
    "{location}",
    "{author}",
    "{resolution}",
    "{duration}",
    "{ai_category}",
]


DATE_FORMAT_MAP = {
    "AAAA-MM-GG": "%Y-%m-%d",
    "GG-MM-AAAA": "%d-%m-%Y",
    "ISO 8601": "%Y%m%d",
    "MM/GG/AAAA": "%m/%d/%Y",
}


def get_date_str(date_format: str) -> str:
    """Restituisce la data corrente nel formato selezionato."""
    date_pattern = DATE_FORMAT_MAP.get(date_format, "%Y%m%d")
    return datetime.date.today().strftime(date_pattern)


def build_new_name(
    base: str,
    ext: str,
    idx: int,
    zeros: int,
    prefix: str,
    pattern: str,
    date_str: str,
    metadata: dict | None = None,
) -> str:
    """
    Costruisce il nuovo nome file applicando i placeholder al pattern.
    L'estensione viene aggiunta automaticamente.
    """
    replacements = {
        "{original}": base,
        "{basename}": base,
        "{counter}": f"{idx:0{zeros}d}",
        "{prefix}": prefix,
        "{date}": date_str,
    }

    if metadata:
        replacements.update(
            {
                placeholder: metadata.get(placeholder[1:-1], "")
                for placeholder in METADATA_PLACEHOLDERS
            }
        )

    new_name = pattern
    for key, value in replacements.items():
        new_name = new_name.replace(key, value)

    return new_name + ext


def build_regex_name(
    filename: str,
    pattern: str,
    replacement: str,
    flags: int = 0,
) -> str:
    """
    Applica una sostituzione regex al filename (solo il nome, senza estensione).
    Restituisce il nome completo con estensione invariata.
    """
    base, ext = os.path.splitext(filename)
    try:
        new_base = re.sub(pattern, replacement, base, flags=flags)
    except re.error:
        new_base = base
    return new_base + ext
