from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox, QSizePolicy
import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


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


def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(800, 400, 300, 300)
    window.setWindowTitle("Resizable Sizer")

    sections = []

    def app_section(numbering):
        # Funkce pro vytvoření jedné sekce
        edit1 = QLineEdit('Perl.exe')
        edit2 = QLineEdit('serverApp')

        # Vytvoření horizontálního uspořádání
        sectionLayout = QHBoxLayout()
        l0_v_layout = QVBoxLayout()
        l1_v_layout = QVBoxLayout()
        l2_v_layout = QVBoxLayout()

        l0_v_layout.addWidget(QLabel(str(numbering) + '.'))
        l0_v_layout.addWidget(QCheckBox())
        l1_v_layout.addWidget(QLabel('Exe to Kill:'))
        l1_v_layout.addWidget(edit1)
        l2_v_layout.addWidget(QLabel('Path contains:'))
        l2_v_layout.addWidget(edit2)

        sectionLayout.addLayout(l0_v_layout)
        sectionLayout.addLayout(l1_v_layout)
        sectionLayout.addLayout(l2_v_layout)

        return sectionLayout

    numbering = 1

    def add_section():
        # Funkce pro přidání další sekce
        nonlocal numbering
        sectionLayout = app_section(numbering)
        sectionWidget = QWidget()
        sectionWidget.setLayout(sectionLayout)
        sectionWidget.setMaximumHeight(55)
        mainLayout.insertWidget(mainLayout.count() - 1,
                                sectionWidget)  # Vložení před tlačítko
        sections.append(sectionWidget)
        numbering += 1

    mainLayout = QVBoxLayout()

    # Přidat tlačítko na začátek layoutu pro přidání sekce
    button = QPushButton('Add Section')
    button.clicked.connect(add_section)
    mainLayout.addWidget(button)

    add_section()  # 1st def sekce
    add_section()  # 2nd def sekce

    # Nastavení maximální výšky pro QHBoxLayout
    # section_h_layout = QHBoxLayout()
    # section_h_layout.addLayout(app_section())
    # mainLayout.addLayout(section_h_layout)

    # Nastavení uspořádání pro hlavní okno
    window.setLayout(mainLayout)

    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
