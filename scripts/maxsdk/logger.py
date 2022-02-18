from PySide2 import QtWidgets,QtCore,QtGui
import logging

class QSignaler(QtCore.QObject):
    logRecord = QtCore.Signal(object)

class SignalHandler(logging.Handler):
    """Logging handler to emit QtSignal with log record text."""

    def __init__(self, *args, **kwargs):
        super(SignalHandler, self).__init__(*args, **kwargs)
        self.emitter = QSignaler()

    def emit(self, logRecord):
        # msg = "{0}".format(logRecord.getMessage())
        # logType = {0}.format(logRecord.)
        self.emitter.logRecord.emit(logRecord)
        QtWidgets.QApplication.processEvents()


class LoggerWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(LoggerWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        # text_browser
        self.text_browser = QtWidgets.QTextBrowser()
        layout.addWidget(self.text_browser)

        # btn_clear
        self.btn_clear = QtWidgets.QPushButton("Clear")
        self.btn_clear.clicked.connect(self.text_browser.clear)
        layout.addWidget(self.btn_clear)

    def appendLogRecord(self, logRecord):
        l = logRecord.levelno
        if l >= 40: #CRITICAL/#ERROR
            self.text_browser.setTextColor(QtGui.QColor("red"))
        elif l==30: #WARNING
            self.text_browser.setTextColor(QtGui.QColor("yellow"))
        elif l <= 20:  #INFO, DEBUG, NOTSET
            self.text_browser.setTextColor( QtGui.QColor("white"))
        self.text_browser.append(logRecord.getMessage())
        