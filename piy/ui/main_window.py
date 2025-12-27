from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QComboBox,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from piy.slicer.superslicer import slice_stl
from piy.ui.stl_viewer import STLViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIY – Simple Slicer")
        self.setMinimumSize(900, 600)

        # ---------- State ----------
        self.stl_path = None
        self.printer_ini = None
        self.infill_percent = 20

        # ---------- Root Widget ----------
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout()
        root.setLayout(main_layout)

        # ============================================================
        # LEFT PANEL (Controls)
        # ============================================================
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)

        # Status
        self.status_label = QLabel("Load an STL to begin")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1976D2;"
        )

        # Load STL
        load_button = QPushButton("Load STL")
        load_button.clicked.connect(self.load_stl)
        load_button.setStyleSheet(
            "background:#4CAF50; color:white; padding:8px; border-radius:6px;"
        )

        # Printer selector
        printer_label = QLabel("Printer")
        printer_label.setStyleSheet("font-weight: bold;")

        self.printer_combo = QComboBox()
        self.printer_combo.addItems([
            "PIY Light Duty 2.0",
            "Ender 3 (Stock)"
        ])
        self.printer_combo.currentTextChanged.connect(self.select_printer)

        # Infill slider
        self.infill_label = QLabel(f"Infill: {self.infill_percent}%")
        self.infill_label.setStyleSheet("font-weight: bold;")

        self.infill_slider = QSlider(Qt.Horizontal)
        self.infill_slider.setRange(0, 100)
        self.infill_slider.setValue(self.infill_percent)
        self.infill_slider.valueChanged.connect(self.update_infill)
        self.infill_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)

        # Slice button
        self.slice_button = QPushButton("Slice")
        self.slice_button.setEnabled(False)
        self.slice_button.clicked.connect(self.slice)
        self.slice_button.setStyleSheet(
            "background:#2196F3; color:white; padding:10px; border-radius:8px;"
        )

        # Assemble controls
        controls_layout.addWidget(load_button)
        controls_layout.addWidget(self.status_label)
        controls_layout.addSpacing(10)
        controls_layout.addWidget(printer_label)
        controls_layout.addWidget(self.printer_combo)
        controls_layout.addSpacing(10)
        controls_layout.addWidget(self.infill_label)
        controls_layout.addWidget(self.infill_slider)
        controls_layout.addStretch()
        controls_layout.addWidget(self.slice_button)

        # ============================================================
        # RIGHT PANEL (STL Viewer)
        # ============================================================
        self.viewer = STLViewer()

        # ============================================================
        # Layout Split
        # ============================================================
        main_layout.addLayout(controls_layout, stretch=1)
        main_layout.addWidget(self.viewer, stretch=3)

        # ---------- Init ----------
        self.select_printer()

    # ============================================================
    # Handlers
    # ============================================================
    def load_stl(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select STL File", "", "STL Files (*.stl)"
        )
        if not path:
            return

        self.stl_path = path
        self.viewer.load_stl(path)
        self.slice_button.setEnabled(True)

        self.update_status("STL loaded")

    def select_printer(self):
        name = self.printer_combo.currentText()

        if name == "PIY Light Duty 2.0":
            self.printer_ini = "/Users/jdyun/Desktop/piy_light_duty_2_0.ini"
        elif name == "Ender 3 (Stock)":
            self.printer_ini = "/Users/jdyun/Desktop/creality_ender3.ini"

        self.update_status("Printer selected")

    def update_infill(self, value):
        self.infill_percent = value
        self.infill_label.setText(f"Infill: {value}%")
        self.update_status()

    def slice(self):
        if not self.stl_path or not self.printer_ini:
            self.set_error("Select STL and printer first")
            return

        self.status_label.setText("Slicing…")
        QApplication.processEvents()

        try:
            slice_stl(
                self.stl_path,
                self.printer_ini,
                infill_percent=self.infill_percent
            )
            self.set_success("Slicing finished ✅")
        except Exception as e:
            self.set_error(str(e))

    # ============================================================
    # UI Helpers
    # ============================================================
    def update_status(self, prefix=None):
        text = []
        if prefix:
            text.append(prefix)
        text.append(f"STL: {self.stl_path or 'None'}")
        text.append(f"Printer: {self.printer_combo.currentText()}")
        text.append(f"Infill: {self.infill_percent}%")

        self.status_label.setText("\n".join(text))
        self.status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1976D2;"
        )

    def set_error(self, msg):
        self.status_label.setText(f"Error:\n{msg}")
        self.status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #D32F2F;"
        )

    def set_success(self, msg):
        self.status_label.setText(msg)
        self.status_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #388E3C;"
        )


print("LOADED main_window.py FROM:", __file__)