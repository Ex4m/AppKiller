from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys


# def main():
#     app = QApplication([])
#     window = QWidget()
#     window.setGeometry(800, 400, 300, 300)
#     window.setWindowTitle("Audio Switcher")

#     layout = QVBoxLayout()

#     label = QLabel("Press the button below")
#     textbox = QTextEdit()
#     button = QPushButton("Press me")
#     button.clicked.connect(lambda: on_clicked(textbox.toPlainText()))

#     layout.addWidget(label)
#     layout.addWidget(textbox)
#     layout.addWidget(button)

#     window.setLayout(layout)

#     window.show()
#     app.exec_()


# def on_clicked(msg):
#     message = QMessageBox()
#     message.setText(msg)
#     message.exec_()


# if __name__ == '__main__':
#     main()


from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QDesktopWidget
import sys
from PyQt5.QtCore import Qt


class AudioSwitcherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 400, 150)  # Default size
        self.center_window()

        self.init_ui()

    def center_window(self):
        screen_center = QDesktopWidget().availableGeometry().center()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen_center)
        self.move(window_rect.topLeft())

    def init_ui(self):
        self.setWindowTitle("Test Window")

        layout = QVBoxLayout()

        label = QLabel(
            "This is popup window text")
        label.setAlignment(Qt.AlignCenter)
        button = QPushButton("OK")
        button.setMaximumWidth(80)

        layout.addWidget(label)
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignCenter)

        self.setLayout(layout)

    def on_clicked(self, msg):
        handler = MessageHandler(min_width=400, min_height=150)
        handler.show_warning(msg)


class MessageHandler(QWidget):
    def __init__(self, parent=None, min_width=200, min_height=100):
        super().__init__()
        self.parent = parent
        self.min_width = min_width
        self.min_height = min_height

        self.setGeometry(0, 0, self.min_width, self.min_height)
        self.center_window()

        self.init_ui()

    def center_window(self):
        screen_center = QDesktopWidget().availableGeometry().center()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen_center)
        self.move(window_rect.topLeft())

    def init_ui(self):
        self.message_box = QMessageBox(self.parent)
        self.message_box.setWindowTitle("Warning")
        self.message_box.setIcon(QMessageBox.Warning)

        central_widget = QWidget(self.message_box)
        layout = QVBoxLayout(central_widget)

        message_label = QLabel()
        layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.message_box.accept)
        layout.addWidget(ok_button)

        self.message_box.setStandardButtons(QMessageBox.NoButton)
        self.message_box.setDefaultButton(ok_button)

        self.message_box.setMinimumWidth(self.min_width)
        self.message_box.setMinimumHeight(self.min_height)

    def show_warning(self, message):
        self.message_label.setText(message)
        self.message_box.adjustSize()
        self.message_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = AudioSwitcherApp()
    main_app.show()
    sys.exit(app.exec_())
