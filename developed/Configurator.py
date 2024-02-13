import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import re
import pickle
import os
import shutil
import sys


class Section(QFrame):
    def __init__(self, numbering):
        super().__init__()
        self.numbering = numbering

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)  # Nastaví šířku rámečku

        self.edit1 = QLineEdit()
        self.edit1.setPlaceholderText('i.e. Perl.exe')
        self.edit2 = QLineEdit()
        self.edit2.setPlaceholderText('i.e. serverApp (optional)')

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
            self.label.setText(label_text + 'Active')
            # self.removeBlurEffect()
            self.setStyleSheet("background-color: #d0ffd0;")
        else:
            self.label.setText(label_text + 'Inactive')
            # self.addBlurEffect()
            self.setStyleSheet("background-color: #ffd0d0;")

    def toggle_widgets_enabled(self):
        # Metoda pro povolení/disablování vstupních polí podle stavu checkboxu
        enable_widgets = self.checkbox.isChecked()
        self.edit1.setEnabled(enable_widgets)
        self.edit2.setEnabled(enable_widgets)
        if enable_widgets:
            # Pokud jsou povolené, odebrat efekty rozmazání
            self.removeBlurEffect(self.edit1)
            self.removeBlurEffect(self.edit2)
        else:
            self.addBlurEffect(self.edit1)
            self.addBlurEffect(self.edit2)

    def addBlurEffect(self, widget):
        # Přidání efektu rozmazání pouze na konkrétní widget
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(1.5)  # Nastavte poloměr rozmazání podle potřeby
        widget.setGraphicsEffect(blur)

    def removeBlurEffect(self, widget):
        # Odebrání efektu rozmazání z konkrétního widgetu
        widget.setGraphicsEffect(None)


class MainWindow(QWidget):
    def __init__(self, width=300, height=300):
        super().__init__()
        self.width = width
        self.height = height

        centerPoint = QDesktopWidget().availableGeometry().center()
        center_x = int(centerPoint.x() - self.width / 2)
        center_y = int(centerPoint.y() - self.height / 2)

        self.setGeometry(center_x,
                         center_y, self.width, self.height)
        self.setWindowTitle("App Killer")

        script_dir = self.get_dir_based_on_file()
        icon_name = 'PerlKillerIco.ico'

        icon_path = self.locate_file(icon_name, script_dir)

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

        self.sections = []

        self.mainLayout = QVBoxLayout(self)

        self.sectionLayout = QVBoxLayout()
        self.menuLayout = QVBoxLayout()
        self.lowerMenuLayout = QHBoxLayout()
        self.lowerUpperMenuLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.sectionLayout)
        self.mainLayout.addLayout(self.menuLayout)
        self.menuLayout.addLayout(self.lowerUpperMenuLayout)
        self.menuLayout.addLayout(self.lowerMenuLayout)

        self.add_section()  # 1st sekce
        self.add_section()  # 2nd sekce

        self.sec_button = QPushButton('Add Section')
        self.sec_button.clicked.connect(self.add_section)
        self.lowerUpperMenuLayout.addWidget(self.sec_button)

        self.rem_button = QPushButton('Remove Last Section')
        self.rem_button.clicked.connect(self.remove_section)
        self.lowerUpperMenuLayout.addWidget(self.rem_button)

        self.exp_button = QPushButton('Export as')
        self.exp_button.clicked.connect(self.export)
        self.lowerMenuLayout.addWidget(self.exp_button)
       
        self.help_button = QPushButton('Help')
        self.help_button.clicked.connect(self.help)
        # self.help_button.setFixedWidth(120)
        self.lowerMenuLayout.addWidget(self.help_button)
        self.setLayout(self.mainLayout)
        
    def get_dir_based_on_file(self):
        if getattr(sys, 'frozen', False):
            # for .exe
            script_dir = os.path.dirname(sys.executable)
        else:
            # for .py
            script_dir = os.path.dirname(os.path.realpath(__file__))
        
        return script_dir
        
    def add_section(self):
        section = Section(len(self.sections) + 1)
        section.setMaximumHeight(80)
        self.sectionLayout.addWidget(section)
        self.sections.append(section)

    def remove_section(self):
        if self.sections:
            section = self.sections.pop()
            section.setParent(None)
            section.deleteLater()

    def checkCompletness(self):
        for section in self.sections:
            if section.checkbox.isChecked():
                if section.edit1.text() == '':
                    MessageHandler.show_error(
                        f'{section.numbering}. section\n cannot be active and not filled.')
                    return False
                if not re.search(r'\.exe$', section.edit1.text()):
                    MessageHandler.show_warning(
                        f'{section.numbering}. section\n App to kill need to contain .exe as well.')
                    return False

        return True

    def help(self):
        note = []
        note.append(';;  -->  for split paths within one cell             ')
        str_note = "".join(note)
        MessageHandler.show_information(str_note)
        
    def locate_file(self, file, current_directory):
        for root, directory, files in os.walk(current_directory):
            if file in files:
                return os.path.join(root, file)
        return None

    def create_directory(self, directory_name, current_directory):
        target_directory = os.path.join(current_directory, directory_name)

        try:
            os.makedirs(target_directory, exist_ok=True)
            print(
                f"Directory '{directory_name}' created on path: {target_directory}")
            return target_directory

        except OSError as e:
            print(f"Failed to create folder: '{directory_name}': {e}")

    def locate_directory(self, directory_name, current_directory):
        target_directory = os.path.join(current_directory, directory_name)

        if os.path.exists(target_directory) and os.path.isdir(target_directory):
            return target_directory
        else:
            depe_dir = self.create_directory("dependencies", current_directory)
            return depe_dir

    def export(self):
        if not self.checkCompletness():
            return
        config_data = []
        question = MessageHandler.show_question(
            "Do you want to save the file as ... ?", None)
        if question:
            new_name = MessageHandler.show_question_with_input(
                "Enter file name:", None, "AppKiller")

        for section in self.sections:
            if section.checkbox.isChecked():
                config_data.append({
                    'section_number': section.numbering,
                    'exe_to_kill': section.edit1.text().lower(),
                    'app_path': section.edit2.text().lower()

                })
                print(config_data)
        try:
            defName = ''
            script_dir = self.get_dir_based_on_file()

            depe_dir = self.locate_directory("dependencies", script_dir)

            if question:
                defName = new_name
                file_path = os.path.join(depe_dir, f"{defName}.pkl")
            else:
                defName = 'AKconfig'
                file_path = os.path.join(depe_dir, f"{defName}.pkl")

            with open(file_path, 'wb') as file:
                pickle.dump(config_data, file)

            MessageHandler.show_information(
                f'Configuration exported successfully to this destination:\n{file_path}\n ')

            # Find and copy AppKiller.exe
            exe_source = self.locate_file('AppKiller.exe', script_dir)
            if exe_source:
                exe_destination = os.path.join(script_dir, f"{defName}.exe")
                shutil.copy(exe_source, exe_destination)
                MessageHandler.show_information(
                    f'AppKiller.exe found and copied to:\n{exe_destination}')
            else:
                MessageHandler.show_warning('AppKiller.exe not found.')

        except Exception as error:
            MessageHandler.show_error(
                f"There was some kind of export error - {error}")


class MessageHandler:
    @staticmethod
    def show_warning(message, parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def show_error(message, parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def show_information(message, parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def show_question(message, parent=None, ):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Question")
        msg_box.setText(message)

        yes_button = msg_box.addButton(QMessageBox.Yes)
        no_button = msg_box.addButton(QMessageBox.No)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            return True
        else:
            return False

    @staticmethod
    def show_question_with_input(message, parent=None, default_name=''):
        input_text, ok_pressed = QInputDialog.getText(
            parent, "Question", f"{message}\n", QLineEdit.Normal, default_name)

        if ok_pressed and input_text:
            return input_text
        else:
            return None


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


# def app_killer(exe_to_kill, path_contains):
#     terminated_count = 0

#     for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
#         try:
#             # Kontrola, zda je klíčové slovo obsaženo v názvu procesu, v cestě k exe souboru nebo v argumentech
#             if exe_to_kill in proc.info['name'].lower():
#                 if path_contains in proc.info['exe'].lower() or any(path_contains in arg.lower() for arg in proc.info['cmdline']):
#                     print(
#                         f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
#                 psutil.Process(proc.info['pid']).terminate()
#                 terminated_count += 1
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             # Skip any errors when retrieving process information
#             pass

#     print(f"Terminated {terminated_count} processes.")


# # Terminate the NiceTaskbar.exe process if its path contains "test"
# app_killer("perl.exe", "server")
