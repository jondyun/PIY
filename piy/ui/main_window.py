from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QLabel, QFileDialog, QComboBox, QSlider, QHBoxLayout
)
from PySide6.QtCore import Qt

from piy.slicer.superslicer import slice_stl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIY - Simple Slicer Frontend")
        self.setMinimumSize(500, 400)

        self.stl_path = None
        self.printer_ini = None
        self.infill_percent = 20

        # ---------- Status Label ----------
        self.status_label = QLabel("No STL loaded")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")

        # ---------- Load STL Button ----------
        load_button = QPushButton("Load STL")
        load_button.clicked.connect(self.load_stl)
        load_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; border-radius: 6px;"
        )

        # ---------- Printer Dropdown ----------
        self.printer_combo = QComboBox()
        self.printer_combo.addItems([
            "PIY Light Duty 2.0",
            "Ender 3 (Stock)"
        ])
        self.printer_combo.currentTextChanged.connect(self.select_printer)
        self.printer_combo.setStyleSheet(
            "font-size: 14px; padding: 4px; min-width: 180px;"
        )

        # ---------- Infill Slider ----------
        self.infill_label = QLabel(f"Infill: {self.infill_percent}%")
        self.infill_label.setStyleSheet("font-weight: bold;")
        self.infill_slider = QSlider(Qt.Horizontal)
        self.infill_slider.setRange(0, 100)
        self.infill_slider.setValue(self.infill_percent)
        self.infill_slider.valueChanged.connect(self.update_infill)
        self.infill_slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #ddd; border-radius: 4px; }
            QSlider::handle:horizontal { background: #2196F3; width: 20px; border-radius: 10px; }
        """)

        infill_layout = QVBoxLayout()
        infill_layout.addWidget(self.infill_label)
        infill_layout.addWidget(self.infill_slider)

        # ---------- Slice Button ----------
        self.slice_button = QPushButton("Slice")
        self.slice_button.setEnabled(False)
        self.slice_button.clicked.connect(self.slice)
        self.slice_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; padding: 10px; border-radius: 8px;"
        )

        # ---------- Layout ----------
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(load_button)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Select Printer:"))
        layout.addWidget(self.printer_combo)
        layout.addLayout(infill_layout)
        layout.addWidget(self.slice_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ---------- Defaults ----------
        self.select_printer()

    # ---------- Event Handlers ----------
    def load_stl(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select STL file", "", "STL Files (*.stl)"
        )
        if file_path:
            self.stl_path = file_path
            self.status_label.setText(f"Loaded STL:\n{file_path}")
            self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
            self.slice_button.setEnabled(True)

    def select_printer(self):
        printer_name = self.printer_combo.currentText()
        if printer_name == "PIY Light Duty 2.0":
            self.printer_ini = "/Users/jdyun/Desktop/piy_light_duty_2_0.ini"
        elif printer_name == "Ender 3 (Stock)":
            self.printer_ini = "/Users/jdyun/Desktop/creality_ender3.ini"

        self.status_label.setText(
            f"STL: {self.stl_path or 'None'}\nPrinter: {printer_name}\nInfill: {self.infill_percent}%"
        )
        self.status_label.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")

    def update_infill(self, value):
        self.infill_percent = value
        self.infill_label.setText(f"Infill: {value}%")

    def slice(self):
        if not self.stl_path or not self.printer_ini:
            self.status_label.setText("Select STL and printer first!")
            self.status_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
            return

        self.status_label.setText(f"Slicing with {self.infill_percent}% infill...")
        QApplication.processEvents()

        try:
            slice_stl(
                self.stl_path,
                self.printer_ini,
                infill_percent=self.infill_percent
            )
            self.status_label.setText("Slicing finished ✅")
            self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        except Exception as e:
            self.status_label.setText(f"Slicing failed:\n{e}")
            self.status_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")

print("LOADED main_window.py FROM:", __file__)