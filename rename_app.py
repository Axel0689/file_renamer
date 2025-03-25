import sys
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit, QFileDialog,
    QWidget, QFormLayout, QSpinBox, QMessageBox, QTableWidget,
    QTableWidgetItem, QComboBox, QStatusBar, QMenu, QAction, QStyle
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon

class FileRenamer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 900, 650)
        self.setWindowIcon(QIcon("assets/icon.ico"))  # Icona della finestra
        
        self.dark_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Barra di menu
        self.menu_bar = self.menuBar()
        
        # Menu Tema
        theme_menu = self.menu_bar.addMenu("Tema")
        theme_menu.addAction("Dark Mode", self.dark_theme)
        theme_menu.addAction("Light Mode", self.light_theme)

        # Menu Informazioni
        info_menu = self.menu_bar.addMenu("Informazioni")
        info_action = QAction("Informazioni sull'app", self)
        info_action.triggered.connect(self.show_about)
        info_menu.addAction(info_action)

        # Sezione selezione file
        self.file_layout = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(120)
        self.file_list.setStyleSheet("border-radius: 8px;")
        self.file_btn = QPushButton("Seleziona File")
        self.file_btn.setFixedSize(150, 35)
        self.file_btn.clicked.connect(self.select_files)

        self.file_layout.addWidget(self.file_list)
        self.file_layout.addWidget(self.file_btn)
        self.layout.addLayout(self.file_layout)

        # Opzioni di rinomina
        self.options_layout = QFormLayout()
        self.options_layout.setLabelAlignment(Qt.AlignLeft)
        self.options_layout.setFormAlignment(Qt.AlignHCenter)

        # Campo prefisso
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Prefisso (es: MyPrefix)")
        self.prefix_input.textChanged.connect(self.update_preview)

        # Campo modello
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("Modello (es: {prefix}_{counter}_{basename}{ext})")
        self.pattern_input.textChanged.connect(self.update_preview)

        # Pulsante Insert
        self.insert_btn = QPushButton("Insert")
        self.insert_btn.setMenu(self.create_placeholder_menu())
        self.insert_btn.setFixedSize(120, 35)

        # Layout per il modello
        pattern_group = QHBoxLayout()
        pattern_group.addWidget(self.pattern_input)
        pattern_group.addWidget(self.insert_btn)

        # Widget numerici
        self.start_spin = QSpinBox()
        self.start_spin.setRange(1, 9999)
        self.start_spin.setValue(1)
        self.start_spin.valueChanged.connect(self.update_preview)

        self.zero_spin = QSpinBox()
        self.zero_spin.setRange(0, 4)
        self.zero_spin.setValue(3)
        self.zero_spin.valueChanged.connect(self.update_preview)

        self.date_combo = QComboBox()
        self.date_combo.addItems([
            "AAAA-MM-GG", "GG-MM-AAAA", "ISO 8601",
            "MM/GG/AAAA", "Custom (es: %Y%m%d)"
        ])
        self.date_combo.currentIndexChanged.connect(self.update_preview)

        # Aggiunta alle opzioni
        self.options_layout.addRow("Prefisso:", self.prefix_input)
        self.options_layout.addRow("Modello:", pattern_group)
        self.options_layout.addRow("Inizio contatore:", self.start_spin)
        self.options_layout.addRow("Zeri prefissati:", self.zero_spin)
        self.options_layout.addRow("Formato data:", self.date_combo)
        self.layout.addLayout(self.options_layout)

        # Anteprima
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["Originale", "Nuovo Nome"])
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.verticalHeader().hide()
        self.layout.addWidget(self.preview_table)

        # Pulsante di rinomina
        self.rename_btn = QPushButton("Rinomina File")
        self.rename_btn.setFixedSize(180, 45)
        self.rename_btn.clicked.connect(self.rename_files)
        self.layout.addWidget(self.rename_btn, alignment=Qt.AlignRight)

        self.selected_files = []
        self.current_dir = ""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_placeholder_menu(self):
        menu = QMenu(self)
        placeholders = [
            ("{original}", "Nome originale completo", "Inserisce il nome originale del file"),
            ("{basename}", "Nome base senza estensione", "Inserisce il nome del file senza estensione"),
            ("{counter}", "Contatore numerico", "Inserisce un contatore con zeri prefissati"),
            ("{prefix}", "Prefisso personalizzato", "Inserisce il testo del campo 'Prefisso'"),
            ("{date}", "Data corrente", "Formattata secondo l'opzione selezionata"),
            ("{ext}", "Estensione del file", "Inserisce l'estensione originale (es: .txt)")
        ]
        
        for placeholder, description, tooltip in placeholders:
            action = QAction(placeholder, self)
            action.setStatusTip(tooltip)
            action.triggered.connect(lambda _, p=placeholder: self.insert_placeholder(p))
            menu.addAction(action)
        return menu

    def insert_placeholder(self, placeholder):
        self.pattern_input.insert(placeholder)
        self.update_preview()

    def dark_theme(self):
        style = """
        QMainWindow {
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
        QMenu {
            background-color: #333333;
            color: white;
            border: 1px solid #404040;
        }
        QMenu::item:selected {
            background-color: #3498db;
        }
        /* AGGIUNTE PER I MESSAGGI */
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
        color: white;  /* Testo visibile in Dark Mode */
        background-color: #000026;
        }
        """
        self.setStyleSheet(style)

    def light_theme(self):
        style = """
        QMainWindow {
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
        color: #2d2d2d;  /* Testo visibile in Light Mode */
        background-color: #f0f0f0;
        }
        """
        self.setStyleSheet(style)

    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Seleziona File", "",
            "Tutti i file (*)", options=options
        )
        if files:
            self.selected_files = files
            self.current_dir = os.path.dirname(files[0])
            self.file_list.clear()
            self.file_list.addItems([os.path.basename(f) for f in files])
            self.update_preview()

    def update_preview(self):
        self.preview_table.setRowCount(0)
        if not self.selected_files:
            return
            
        pattern = self.pattern_input.text()
        start = self.start_spin.value()
        zeros = self.zero_spin.value()
        date_format = self.date_combo.currentText()
        
        for idx, file_path in enumerate(self.selected_files, start=start):
            filename = os.path.basename(file_path)
            base, ext = os.path.splitext(filename)
            
            date_str = datetime.datetime.now().strftime(
                "%Y-%m-%d" if date_format == "AAAA-MM-GG" else
                "%d-%m-%Y" if date_format == "GG-MM-AAAA" else
                "%Y%m%d" if date_format == "ISO 8601" else
                "%m/%d/%Y" if date_format == "MM/GG/AAAA" else
                "%Y%m%d"
            )
            
            replacements = {
                "{original}": filename,
                "{basename}": base,
                "{counter}": f"{idx:0{zeros}d}",
                "{prefix}": self.prefix_input.text(),
                "{date}": date_str,
                "{ext}": ext
            }
            
            new_name = pattern
            for key, value in replacements.items():
                new_name = new_name.replace(key, value)
                
            row_position = self.preview_table.rowCount()
            self.preview_table.insertRow(row_position)
            self.preview_table.setItem(row_position, 0, QTableWidgetItem(filename))
            self.preview_table.setItem(row_position, 1, QTableWidgetItem(new_name))
            
    def rename_files(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Errore", "Seleziona prima i file")
            return
            
        pattern = self.pattern_input.text()
        start = self.start_spin.value()
        zeros = self.zero_spin.value()
        date_format = self.date_combo.currentText()
        
        confirm = QMessageBox.question(
            self, "Conferma", "Vuoi procedere con la rinomina?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
            
        self.status_bar.showMessage("Rinomina in corso...", 3000)
        
        for idx, file_path in enumerate(self.selected_files, start=start):
            filename = os.path.basename(file_path)
            base, ext = os.path.splitext(filename)
            
            date_str = datetime.datetime.now().strftime(
                "%Y-%m-%d" if date_format == "AAAA-MM-GG" else
                "%d-%m-%Y" if date_format == "GG-MM-AAAA" else
                "%Y%m%d" if date_format == "ISO 8601" else
                "%m/%d/%Y" if date_format == "MM/GG/AAAA" else
                "%Y%m%d"
            )
            
            replacements = {
                "{original}": filename,
                "{basename}": base,
                "{counter}": f"{idx:0{zeros}d}",
                "{prefix}": self.prefix_input.text(),
                "{date}": date_str,
                "{ext}": ext
            }
            
            new_name = pattern
            for key, value in replacements.items():
                new_name = new_name.replace(key, value)
                
            new_path = os.path.join(self.current_dir, new_name)
            try:
                os.rename(file_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la rinomina di {filename}: {str(e)}")
                continue
                
        self.status_bar.showMessage("Rinomina completata!", 3000)
        self.selected_files = []
        self.file_list.clear()
        self.preview_table.setRowCount(0)

    def show_about(self):
        """Mostra la finestra di informazioni"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Informazioni")
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            "<b>File Renamer</b><br>"
            "Versione 0.1<br><br>"
            "Applicazione per la rinomina di file in modalità personalizzata.<br>"
            "Supporta placeholder, anteprima dinamica e formati di data.<br><br>"
            "<b>Crediti</b>: Sviluppata da Alessandro Bagnuoli <b>(@axel0689 - GitHub)</b>"
        )
        msg.setWindowIcon(self.windowIcon())  # Usa l'icona dell'app
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.ico"))  # Icona nella barra delle applicazioni
    window = FileRenamer()
    window.show()
    sys.exit(app.exec_())