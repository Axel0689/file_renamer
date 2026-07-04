"""
Tab con le opzioni di rinomina tramite pattern (funzionalita v0.2).
"""

import os

from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QPushButton,
    QSpinBox,
    QWidget,
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from file_renamer.core.renamer import (
    CORE_PLACEHOLDERS,
    PLACEHOLDERS,
    build_new_name,
    get_date_str,
)

DATE_FORMATS = [
    "AAAA-MM-GG",
    "GG-MM-AAAA",
    "ISO 8601",
    "MM/GG/AAAA",
    "Custom (es: %Y%m%d)",
]


class PatternTab(QWidget):
    """Widget con i controlli per la rinomina tramite pattern placeholder."""

    preview_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()

        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.setInterval(150)
        self._preview_timer.timeout.connect(self.preview_requested)

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setLabelAlignment(Qt.AlignLeft)

        # Prefisso
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Prefisso (es: MyPrefix)")
        layout.addRow("Prefisso:", self.prefix_input)

        # Pattern + bottone Insert
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText(
            "Modello (es: {prefix}_{counter}_{basename}) — L'estensione viene mantenuta automaticamente"
        )
        self.insert_btn = QPushButton("Insert")
        self.insert_btn.setMenu(self._create_placeholder_menu())
        self.insert_btn.setFixedSize(120, 35)

        pattern_row = QHBoxLayout()
        pattern_row.addWidget(self.pattern_input)
        pattern_row.addWidget(self.insert_btn)
        layout.addRow("Modello:", pattern_row)

        # Inizio contatore
        self.start_spin = QSpinBox()
        self.start_spin.setRange(1, 9999)
        self.start_spin.setValue(1)
        layout.addRow("Inizio contatore:", self.start_spin)

        # Zeri prefissati
        self.zero_spin = QSpinBox()
        self.zero_spin.setRange(0, 4)
        self.zero_spin.setValue(3)
        layout.addRow("Zeri prefissati:", self.zero_spin)

        # Formato data
        self.date_combo = QComboBox()
        self.date_combo.addItems(DATE_FORMATS)
        layout.addRow("Formato data:", self.date_combo)

    def _connect_signals(self):
        self.prefix_input.textChanged.connect(self._debounce)
        self.pattern_input.textChanged.connect(self._debounce)
        self.start_spin.valueChanged.connect(self._debounce)
        self.zero_spin.valueChanged.connect(self._debounce)
        self.date_combo.currentIndexChanged.connect(self._debounce)

    def _debounce(self):
        self._preview_timer.start()

    def _create_placeholder_menu(self) -> QMenu:
        menu = QMenu(self)
        for placeholder in CORE_PLACEHOLDERS:
            description = PLACEHOLDERS.get(placeholder, placeholder)
            action = QAction(f"{placeholder}  —  {description}", self)
            action.triggered.connect(
                lambda _, value=placeholder: self._insert_placeholder(value)
            )
            menu.addAction(action)
        return menu

    def _insert_placeholder(self, placeholder: str):
        self.pattern_input.insert(placeholder)
        self.preview_requested.emit()

    def build_new_names(self, files: list[str]) -> list[tuple[str, str]]:
        """Restituisce coppie (nome_originale, nuovo_nome) per tutti i file."""
        pattern = self.pattern_input.text()
        start = self.start_spin.value()
        zeros = self.zero_spin.value()
        prefix = self.prefix_input.text()
        date_str = get_date_str(self.date_combo.currentText())

        pairs = []
        for idx, file_path in enumerate(files, start=start):
            filename = os.path.basename(file_path)
            base, ext = os.path.splitext(filename)
            new_name = build_new_name(base, ext, idx, zeros, prefix, pattern, date_str)
            pairs.append((filename, new_name))
        return pairs

    def get_settings(self) -> dict:
        """Serializza le impostazioni correnti (per Template System)."""
        return {
            "prefix": self.prefix_input.text(),
            "pattern": self.pattern_input.text(),
            "counter_start": self.start_spin.value(),
            "zero_padding": self.zero_spin.value(),
            "date_format": self.date_combo.currentText(),
        }

    def load_settings(self, data: dict):
        """Ripristina le impostazioni da un dict (dal Template System)."""
        self.prefix_input.setText(data.get("prefix", ""))
        self.pattern_input.setText(data.get("pattern", ""))
        self.start_spin.setValue(data.get("counter_start", 1))
        self.zero_spin.setValue(data.get("zero_padding", 3))
        idx = self.date_combo.findText(data.get("date_format", "AAAA-MM-GG"))
        if idx >= 0:
            self.date_combo.setCurrentIndex(idx)
