import sys

from qroundprogressbar import QRoundProgressBar

from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton

class WorkerThread(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            sleep(0.1)
            self.progress.emit(i)

class DemoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.roundBar = QRoundProgressBar()
        self.roundBar.setFixedSize(300, 300)
        self.roundBar.setMaximum(100)
        self.roundBar.setMinimum(0)
        self.roundBar.setRange(0, 100)
        self.roundBar.setFormat("Value: %p")

        button = QPushButton("Start")
        button.clicked.connect(self.onStart)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.roundBar)

        self.setLayout(layout)

        self.longTask = WorkerThread()
        self.longTask.progress.connect(self.reportProgress)

    def onStart(self):
        self.longTask.start()

    def reportProgress(self, i):
        self.roundBar.setValue(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DemoWidget()
    widget.show()
    sys.exit(app.exec())
