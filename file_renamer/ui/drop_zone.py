"""
Widget drag & drop per la selezione dei file.
"""

import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

IDLE_STYLE = (
    "border: 2px dashed #5a5a7a; border-radius: 10px; " "padding: 18px; color: #aaaacc;"
)
HOVER_STYLE = (
    "border: 2px dashed #3498db; border-radius: 10px; " "padding: 18px; color: #3498db;"
)
LOADED_STYLE = (
    "border: 2px solid #3498db; border-radius: 10px; " "padding: 18px; color: #ffffff;"
)
IDLE_TEXT = "Trascina i file qui  oppure  clicca per selezionare"


class DropZone(QWidget):
    """
    Area visuale che accetta drag & drop di file da Windows Explorer.
    Emette il segnale files_dropped con la lista dei percorsi assoluti.
    Un click sull'area apre il QFileDialog (compatibilita con v0.2).
    """

    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(90)
        self._loaded_files: list[str] = []
        self._build_ui()
        self._set_idle_state()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._label = QLabel(IDLE_TEXT)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setCursor(Qt.PointingHandCursor)
        self._label.setObjectName("dropZoneLabel")
        layout.addWidget(self._label)

        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(4, 0, 4, 0)

        self._count_label = QLabel("")
        self._count_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._count_label.setObjectName("dropZoneCount")

        self._clear_btn = QPushButton("Rimuovi tutti")
        self._clear_btn.setFixedSize(120, 28)
        self._clear_btn.setVisible(False)
        self._clear_btn.clicked.connect(self.clear)

        bottom_row.addWidget(self._count_label)
        bottom_row.addStretch()
        bottom_row.addWidget(self._clear_btn)
        layout.addLayout(bottom_row)

    # ----------------------------------------------- Stato / testo
    def _set_idle_state(self):
        """Aspetta file — bordo tratteggiato."""
        self._label.setStyleSheet(IDLE_STYLE)
        self._label.setText(IDLE_TEXT)

    def _set_hover_state(self):
        """File in ingresso — bordo evidenziato."""
        self._label.setStyleSheet(HOVER_STYLE)
        self._label.setText("Rilascia i file")

    def _set_loaded_state(self):
        """File caricati — mostra conteggio."""
        file_count = len(self._loaded_files)
        self._label.setStyleSheet(LOADED_STYLE)
        names = [os.path.basename(path) for path in self._loaded_files[:3]]
        preview = ",  ".join(names)
        if file_count > 3:
            preview += f"  … +{file_count - 3} altri"
        self._label.setText(preview)
        self._count_label.setText(f"{file_count} file selezionati")
        self._clear_btn.setVisible(True)

    # --------------------------------------------------- Drag events
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_hover_state()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if self._loaded_files:
            self._set_loaded_state()
        else:
            self._set_idle_state()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = [
            url.toLocalFile()
            for url in urls
            if url.isLocalFile() and os.path.isfile(url.toLocalFile())
        ]
        if files:
            self._load_files(files)
        else:
            self._restore_visual_state()

    # --------------------------------------------------- Mouse click
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._open_dialog()

    def _open_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Seleziona File", "", "Tutti i file (*)"
        )
        if files:
            self._load_files(files)

    # --------------------------------------------------- Public API
    def _load_files(self, files: list[str]):
        self._loaded_files = list(files)
        self._set_loaded_state()
        self.files_dropped.emit(self.current_files)

    def _restore_visual_state(self):
        if self._loaded_files:
            self._set_loaded_state()
        else:
            self._set_idle_state()

    def clear(self):
        """Rimuove tutti i file caricati e torna allo stato idle."""
        self._loaded_files = []
        self._count_label.setText("")
        self._clear_btn.setVisible(False)
        self._set_idle_state()
        self.files_dropped.emit([])

    def set_files(self, files: list[str]):
        """Imposta i file programmaticamente (senza aprire il dialog)."""
        if files:
            self._load_files(files)
        else:
            self.clear()

    @property
    def current_files(self) -> list[str]:
        return list(self._loaded_files)
