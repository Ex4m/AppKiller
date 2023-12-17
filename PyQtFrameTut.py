from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(800, 400, 300, 300)
    window.setWindowTitle("Audio Switcher")

    layout = QVBoxLayout()

    label = QLabel("Press the button below")
    textbox = QTextEdit()
    button = QPushButton("Press me")
    button.clicked.connect(lambda: on_clicked(textbox.toPlainText()))

    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    window.setLayout(layout)

    window.show()
    app.exec_()


def on_clicked(msg):
    message = QMessageBox()
    message.setText(msg)
    message.exec_()


if __name__ == '__main__':
    main()
