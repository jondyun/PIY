from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIY")

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Load STL"))
        layout.addWidget(QPushButton("Slice"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)