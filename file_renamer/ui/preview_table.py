"""
Widget tabella anteprima riutilizzabile.
"""

from PyQt5.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class PreviewTable(QTableWidget):
    """Tabella che mostra coppie (nome originale, nuovo nome)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Originale", "Nuovo Nome"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()

    def update_preview(self, pairs: list[tuple[str, str]]):
        """Mostra le coppie (nome originale, nuovo nome)."""
        self.setUpdatesEnabled(False)
        try:
            self.setRowCount(len(pairs))
            for row, (old_name, new_name) in enumerate(pairs):
                self.setItem(row, 0, QTableWidgetItem(old_name))
                self.setItem(row, 1, QTableWidgetItem(new_name))
        finally:
            self.setUpdatesEnabled(True)

    def clear_preview(self):
        self.setRowCount(0)
