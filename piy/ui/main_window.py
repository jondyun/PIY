from piy.slicer.superslicer import slice_stl
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QFileDialog, QComboBox

from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QWidget, QVBoxLayout,
    QLabel, QFileDialog, QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIY")
        self.stl_path = None
        self.printer_ini = None

        # Status label
        self.status_label = QLabel("No STL loaded")

        # Load STL button
        load_button = QPushButton("Load STL")
        load_button.clicked.connect(self.load_stl)

        # Printer selection dropdown
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["Printer1", "Printer2"])
        self.printer_combo.setCurrentIndex(0)  # select Printer1 by default
        self.select_printer()  # set self.printer_ini immediately

        # Slice button
        self.slice_button = QPushButton("Slice")
        self.slice_button.setEnabled(False)
        self.slice_button.clicked.connect(self.slice_stl)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(load_button)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Select Printer:"))
        layout.addWidget(self.printer_combo)
        layout.addWidget(self.slice_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_stl(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select STL file", "", "STL Files (*.stl)"
        )
        if file_path:
            self.stl_path = file_path
            self.status_label.setText(f"Loaded: {file_path}")
            self.slice_button.setEnabled(True)

    def select_printer(self):
        printer_name = self.printer_combo.currentText()

        # Map dropdown name to actual INI file
        if printer_name == "Printer1":
            # Use your Desktop test.ini for testing
            self.printer_ini = "/Users/jdyun/Desktop/test.ini"
        elif printer_name == "Printer2":
            # Add another test INI or leave None
            self.printer_ini = None

        self.status_label.setText(
            f"Loaded: {self.stl_path or 'No STL'}\nPrinter: {printer_name}"
        )

    def slice_stl(self):
        if not self.stl_path or not self.printer_ini:
            self.status_label.setText("Select STL and printer first!")
            return

        self.status_label.setText(f"Slicing {self.stl_path} with {self.printer_ini}...")
        QApplication.processEvents()  # update UI immediately

        result = slice_stl(self.stl_path, self.printer_ini)
        self.status_label.setText(f"Slicing finished!\n{result[:200]}...")  # show first 200 chars

    def slice_stl_button_pressed(self):
        if not self.stl_path or not self.printer_ini:
            self.status_label.setText("Select STL and printer first!")
            return

        self.status_label.setText(f"Slicing {self.stl_path} with {self.printer_ini}...")
        QApplication.processEvents()  # refresh UI

        result = slice_stl(self.stl_path, self.printer_ini)
        self.status_label.setText(result)