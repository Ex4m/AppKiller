import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import re


def app_killer(exe_to_kill, path_contains):
    terminated_count = 0

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if exe_to_kill in proc.info['name'] and path_contains in proc.info['exe']:
                print(
                    f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
                psutil.Process(proc.info['pid']).terminate()
                terminated_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip any errors when retrieving process information
            pass

    print(f"Terminated {terminated_count} processes.")


# Terminate the NiceTaskbar.exe process if its path contains "test"
app_killer("NiceTaskbar.exe", "9am")


class Section(QFrame):
    def __init__(self, numbering):
        super().__init__()

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)  # Nastaví šířku rámečku

        self.edit1 = QLineEdit('Perl.exe')
        self.edit2 = QLineEdit('serverApp')

        # Vytvoření grid layoutu pro jednu sekci
        self.layout = QGridLayout(self)

        self.label = QLabel(str(numbering) + '. Inactive')
        self.checkbox = QCheckBox()

        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.checkbox, 0, 1)
        self.layout.addWidget(QLabel('Exe to Kill:'), 1, 0)
        self.layout.addWidget(self.edit1, 1, 1)
        self.layout.addWidget(QLabel('Path contains:'), 2, 0)
        self.layout.addWidget(self.edit2, 2, 1)

        # Nastavení počátečního stavu checkboxu a vstupních polí
        self.checkbox.setChecked(True)
        self.toggle_widgets_enabled()
        self.toggle_checkbox()  # Přidá 'Active' nebo 'Inactive' do textu

        # Přidání reakce na kliknutí na checkbox (až po inicializaci)
        self.checkbox.clicked.connect(self.toggle_checkbox)
        # Volání toggle_checkbox pro inicializaci textu a efektů
        self.toggle_checkbox()

    def toggle_checkbox(self):
        # Metoda pro přepnutí stavu checkboxu
        self.toggle_widgets_enabled()
        label_text = re.sub(r'\b(?:Active|Inactive)\b',
                            '', str(self.label.text()))
        if self.checkbox.isChecked():
            self.label.setText(label_text + ' Active')
            self.removeBlurEffect()
            self.setStyleSheet("background-color: #d0ffd0;")
        else:
            self.label.setText(label_text + ' Inactive')
            self.addBlurEffect()
            self.setStyleSheet("background-color: #ffd0d0;")

    def toggle_widgets_enabled(self):
        # Metoda pro povolení/disablování vstupních polí podle stavu checkboxu
        enable_widgets = self.checkbox.isChecked()
        self.edit1.setEnabled(enable_widgets)
        self.edit2.setEnabled(enable_widgets)

    def addBlurEffect(self):
        # Přidání efektu rozmazání
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(1.5)  # Nastavte poloměr rozmazání podle potřeby
        self.setGraphicsEffect(blur)

    def removeBlurEffect(self):
        # Odebrání efektu rozmazání
        self.setGraphicsEffect(None)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 400, 300, 300)
        self.setWindowTitle("App Killer")

        self.sections = []

        self.mainLayout = QVBoxLayout(self)
        self.lowerMenuLayout = QHBoxLayout(self)

        self.add_section()  # 1st sekce
        self.add_section()  # 2nd sekce

        self.sec_button = QPushButton('Add Section')
        self.sec_button.clicked.connect(self.add_section)
        self.lowerMenuLayout.addWidget(self.sec_button)

        self.exp_button = QPushButton('Export')
        self.exp_button.clicked.connect(self.export_exe)
        self.lowerMenuLayout.addWidget(self.exp_button)
        self.mainLayout.addLayout(self.lowerMenuLayout)
        self.setLayout(self.mainLayout)

    def add_section(self):
        section = Section(len(self.sections) + 1)
        section.setMaximumHeight(80)
        self.mainLayout.insertWidget(self.mainLayout.count() - 1, section)
        self.sections.append(section)

    def export_exe(self):
        pass


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()