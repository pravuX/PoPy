import sys
import os

def notify():
    # sleep(1)
    notification = Notify()
    notification.title = "PoPy - Notify"
    notification.message = "Session Completed"
    notification.send()
    os.system("mpv --really-quiet alarm_clock.mp3")

from time import sleep

from notifypy import Notify

from functools import partial
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import (
        QApplication,
        QComboBox,
        QVBoxLayout,
        QMainWindow,
        QPushButton,
        QWidget,)

from qroundprogressbar import QRoundProgressBar

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self, setTime):
        for i in range(setTime, 0, -1):
            sleep(1)
            self.progress.emit(i-1)
        notify()
        self.finished.emit()

# View
class PoPy(QMainWindow):
    """PoPyUI extends QMainWindow"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setTime = 25
        self._createViews()
        self._connectSignals()

    def _createViews(self):
        self.setWindowTitle("PoPy - Pomodoro Timer")
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        _layout = QVBoxLayout()

        self.stBtn = QPushButton("Start Session")

        self.progressDonut = QRoundProgressBar()
        self.progressDonut.setBarStyle(QRoundProgressBar.BarStyle.DONUT)
        self.progressDonut.setValue(0)
        self.progressDonut.setFixedSize(235, 235)
        self.progressDonut.setFormat(self._getTime(self.setTime))
        self.progressDonut.setDataColors([(0., QtGui.QColor.fromRgb(191,97,106)), (0.25, QtGui.QColor.fromRgb(208,135,112)), (0.5, QtGui.QColor.fromRgb(235,203,139)), (0.75, QtGui.QColor.fromRgb(163,190,140)), (1., QtGui.QColor.fromRgb(191,97,106))])

        self.cmbBox = QComboBox()
        self.cmbBox.addItems(["25", "55", "5"])

        _layout.addWidget(self.cmbBox)
        _layout.addWidget(self.progressDonut)
        _layout.addWidget(self.stBtn)

        self._centralWidget.setLayout(_layout)

    def _updateSetTime(self, currTxt):
        self.setTime = int(currTxt) * 60
        self.progressDonut.setFormat(self._getTime(self.setTime))

    def _getTime(self, time):
        """time is in seconds"""
        mins = str(time // 60)
        secs = str(time % 60)
        fmt_min = "0" + mins if len(mins) == 1 else mins
        fmt_sec = "0" + secs if len(secs) == 1 else secs
        return f"{fmt_min}:{fmt_sec}"


    def _timer(self):
        time = self.setTime
        # Create a new thread and a worker.
        self._thread = QThread()
        self.worker = Worker()

        # Move worker to the new _thread for performing tasks outside
        # the event loop.
        self.worker.moveToThread(self._thread)

        # Connect signals to relevant slots.
        self._thread.started.connect(partial(self.worker.run, time))
        self.worker.finished.connect(self._thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self.worker.progress.connect(self.reportProgress)

        self._thread.start()

        # Prevents User from starting multiple sessions simulataneously
        # and reenables the button at the end of session
        def reset():
            self.stBtn.setEnabled(True)
            self.cmbBox.setEnabled(True)

        self.stBtn.setEnabled(False)
        self.cmbBox.setEnabled(False)
        self._thread.finished.connect(reset)

    def reportProgress(self, timeLeft):
        progress = self.setTime-timeLeft
        self.progressDonut.setRange(0, self.setTime)
        self.progressDonut.setValue(progress)
        self.progressDonut.setFormat(self._getTime(timeLeft))

    def _connectSignals(self):
        self.cmbBox.currentTextChanged.connect(
                lambda currTxt: self._updateSetTime(currTxt))
        self.stBtn.clicked.connect(self._timer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pomodoro = PoPy()
    pomodoro.show()
    sys.exit(app.exec_())
