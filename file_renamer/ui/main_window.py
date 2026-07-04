"""
Finestra principale dell'applicazione File Renamer v0.3.
"""

import os

from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from file_renamer.ui.pattern_tab import PatternTab
from file_renamer.ui.preview_table import PreviewTable
from file_renamer.ui.drop_zone import DropZone
from file_renamer.utils.undo_stack import UndoStack, RenameOperation, RenameTransaction

DARK_STYLE = """
QMainWindow {
    background-color: #000026;
    color: white;
}
QWidget {
    background-color: #000026;
    color: white;
}
QLabel {
    color: white;
}
QListWidget, QLineEdit, QComboBox, QSpinBox {
    background-color: #031326;
    color: white;
    border: 2px solid #3a3a3a;
    padding: 8px;
    selection-color: white;
    selection-background-color: #3498db;
}
QTableWidget {
    background-color: #031326;
    color: white;
    gridline-color: #404040;
    alternate-background-color: #333333;
}
QTableWidget::item:selected {
    background-color: #3498db;
    color: white;
}
QHeaderView::section {
    background-color: #1a1a3a;
    color: white;
    border: 1px solid #404040;
    padding: 5px;
}
QPushButton {
    background-color: #66667d;
    border-radius: 8px;
    padding: 8px 16px;
    color: white;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #2980b9;
}
QComboBox {
    padding: 4px 12px;
}
QSpinBox {
    padding: 4px 10px;
}
QMenuBar {
    background-color: #000026;
    color: white;
}
QMenuBar::item:selected {
    background-color: #3498db;
    color: white;
}
QMenuBar::item:pressed {
    background-color: #2980b9;
    color: white;
}
QMenu {
    background-color: #1a1a3a;
    color: white;
    border: 1px solid #404040;
}
QMenu::item:selected {
    background-color: #3498db;
    color: white;
}
QMessageBox {
    background-color: #000026;
    color: white;
}
QMessageBox QLabel {
    color: white;
}
QMessageBox QPushButton {
    background-color: #3498db;
    color: white;
    border-radius: 5px;
    padding: 5px 10px;
}
QMessageBox QPushButton:hover {
    background-color: #2980b9;
}
QStatusBar {
    color: white;
    background-color: #000026;
}
QTabWidget::pane {
    border: 1px solid #3a3a3a;
}
QTabBar::tab {
    background-color: #1a1a3a;
    color: white;
    padding: 8px 20px;
    border: 1px solid #3a3a3a;
}
QTabBar::tab:selected {
    background-color: #3498db;
}
QLabel#dropZoneLabel {
    border: 2px dashed #5a5a7a;
    border-radius: 10px;
    padding: 18px;
    color: #aaaacc;
    font-size: 13px;
}
QLabel#dropZoneCount {
    color: #aaaacc;
    font-size: 11px;
}
"""

LIGHT_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
    color: #2d2d2d;
}
QWidget {
    background-color: #f0f0f0;
    color: #2d2d2d;
}
QLabel {
    color: #2d2d2d;
}
QListWidget, QLineEdit, QComboBox, QSpinBox {
    background-color: white;
    color: #2d2d2d;
    border: 2px solid #d3d3d3;
    padding: 8px;
    selection-color: white;
    selection-background-color: #4CAF50;
}
QTableWidget {
    background-color: white;
    color: #2d2d2d;
    gridline-color: #e0e0e0;
    alternate-background-color: #f5f5f5;
}
QTableWidget::item:selected {
    background-color: #4CAF50;
    color: white;
}
QHeaderView::section {
    background-color: #e0e0e0;
    color: #2d2d2d;
    border: 1px solid #d3d3d3;
    padding: 5px;
}
QPushButton {
    background-color: #4CAF50;
    border-radius: 8px;
    padding: 8px 16px;
    color: white;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45a049;
}
QComboBox {
    padding: 4px 12px;
}
QSpinBox {
    padding: 4px 10px;
}
QMenuBar {
    background-color: #f0f0f0;
    color: #2d2d2d;
}
QMenuBar::item:selected {
    background-color: #4CAF50;
    color: white;
}
QMenuBar::item:pressed {
    background-color: #45a049;
    color: white;
}
QMenu {
    background-color: white;
    color: #2d2d2d;
    border: 1px solid #d3d3d3;
}
QMenu::item:selected {
    background-color: #4CAF50;
    color: white;
}
QStatusBar {
    color: #2d2d2d;
    background-color: #f0f0f0;
}
QTabWidget::pane {
    border: 1px solid #d3d3d3;
}
QTabBar::tab {
    background-color: #e0e0e0;
    color: #2d2d2d;
    padding: 8px 20px;
    border: 1px solid #d3d3d3;
}
QTabBar::tab:selected {
    background-color: #4CAF50;
    color: white;
}
QLabel#dropZoneLabel {
    border: 2px dashed #b0b0b0;
    border-radius: 10px;
    padding: 18px;
    color: #666666;
    font-size: 13px;
}
QLabel#dropZoneCount {
    color: #666666;
    font-size: 11px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer v0.3")
        self.setGeometry(100, 100, 950, 700)

        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "icon.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.selected_files: list[str] = []
        self.current_dir: str = ""
        self._undo_stack = UndoStack(self)

        self._apply_dark_theme()
        self._build_menu()
        self._build_ui()

        # Connetti i segnali undo/redo
        self._undo_stack.can_undo_changed.connect(self._undo_action.setEnabled)
        self._undo_stack.can_redo_changed.connect(self._redo_action.setEnabled)
        self._undo_stack.status_message.connect(
            lambda msg: self.status_bar.showMessage(msg, 3000)
        )

    # ------------------------------------------------------------------ Menu
    def _build_menu(self):
        menu_bar = self.menuBar()

        # Modifica (Undo/Redo)
        edit_menu = menu_bar.addMenu("Modifica")

        self._undo_action = QAction("Annulla", self)
        self._undo_action.setShortcut("Ctrl+Z")
        self._undo_action.setEnabled(False)
        self._undo_action.triggered.connect(self._undo)
        edit_menu.addAction(self._undo_action)

        self._redo_action = QAction("Ripeti", self)
        self._redo_action.setShortcut("Ctrl+Y")
        self._redo_action.setEnabled(False)
        self._redo_action.triggered.connect(self._redo)
        edit_menu.addAction(self._redo_action)

        # Tema
        theme_menu = menu_bar.addMenu("Tema")
        theme_menu.addAction("Dark Mode", self._apply_dark_theme)
        theme_menu.addAction("Light Mode", self._apply_light_theme)

        # Informazioni
        info_menu = menu_bar.addMenu("Informazioni")
        info_action = QAction("Informazioni sull'app", self)
        info_action.triggered.connect(self._show_about)
        info_menu.addAction(info_action)

    # --------------------------------------------------------------- UI Core
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Drop zone (sostituisce QListWidget + QPushButton)
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_files_changed)
        main_layout.addWidget(self.drop_zone)

        # Tab widget (Pattern | Regex — aggiunto in Fase 5)
        self.tabs = QTabWidget()
        self.pattern_tab = PatternTab()
        self.tabs.addTab(self.pattern_tab, "Modello")
        main_layout.addWidget(self.tabs)

        # Tabella anteprima
        self.preview_table = PreviewTable()
        main_layout.addWidget(self.preview_table)

        # Bottone rinomina
        self.rename_btn = QPushButton("Rinomina File")
        self.rename_btn.setFixedSize(180, 45)
        self.rename_btn.clicked.connect(self._rename_files)
        main_layout.addWidget(self.rename_btn, alignment=Qt.AlignRight)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Collega il signal di preview_requested dal tab attivo
        self.pattern_tab.preview_requested.connect(self._update_preview)

    # --------------------------------------------------------- File selection
    def _on_files_changed(self, files: list[str]):
        """Chiamato quando la DropZone emette files_dropped."""
        self.selected_files = files
        self.current_dir = os.path.dirname(files[0]) if files else ""
        self._update_preview()

    # ------------------------------------------------------------ Preview
    def _update_preview(self):
        if not self.selected_files:
            self.preview_table.clear_preview()
            return

        pairs = self.pattern_tab.build_new_names(self.selected_files)
        self.preview_table.update_preview(pairs)

    # ------------------------------------------------------------ Rename
    def _rename_files(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Errore", "Seleziona prima i file.")
            return

        confirm = QMessageBox.question(
            self,
            "Conferma",
            "Vuoi procedere con la rinomina?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        self.status_bar.showMessage("Rinomina in corso...", 3000)

        pairs = self.pattern_tab.build_new_names(self.selected_files)
        transaction = self._build_rename_transaction(pairs)
        errors = self._undo_stack.execute(transaction)
        if errors:
            self._show_rename_errors(errors)
            return

        self.selected_files = []
        self.drop_zone.clear()

    def _build_rename_transaction(
        self, pairs: list[tuple[str, str]]
    ) -> RenameTransaction:
        operations = [
            RenameOperation(
                old_path=file_path,
                new_path=os.path.join(self.current_dir, new_name),
            )
            for (_, new_name), file_path in zip(pairs, self.selected_files)
        ]
        return RenameTransaction(
            operations=operations,
            description=(
                f"{len(operations)} file — {self.pattern_tab.pattern_input.text()}"
            ),
        )

    def _show_rename_errors(self, errors: list[str]):
        QMessageBox.critical(
            self,
            "Errori durante la rinomina",
            "La rinomina e stata annullata a causa di errori:\n" + "\n".join(errors),
        )

    # ---------------------------------------------------------- Undo / Redo
    def _undo(self):
        if not self._undo_stack.undo():
            QMessageBox.warning(
                self,
                "Annulla",
                "Impossibile annullare: alcuni file potrebbero essere stati spostati o eliminati.",
            )

    def _redo(self):
        if not self._undo_stack.redo():
            QMessageBox.warning(
                self,
                "Ripeti",
                "Impossibile ripristinare: alcuni file potrebbero essere stati spostati o eliminati.",
            )

    # --------------------------------------------------------------- Temi
    def _apply_dark_theme(self):
        self.setStyleSheet(DARK_STYLE)

    def _apply_light_theme(self):
        self.setStyleSheet(LIGHT_STYLE)

    # ------------------------------------------------------------ About
    def _show_about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Informazioni")
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            "<b>File Renamer</b><br>"
            "Versione 0.3<br><br>"
            "Applicazione per la rinomina di file in modalita personalizzata.<br>"
            "Supporta placeholder, anteprima dinamica, formati di data,<br>"
            "template, undo/redo, drag &amp; drop, regex e suggerimenti AI.<br><br>"
            "<b>Crediti</b>: Sviluppata da Alessandro Bagnuoli <b>(@axel0689 - GitHub)</b>"
        )
        if self.windowIcon():
            msg.setWindowIcon(self.windowIcon())
        msg.exec_()
