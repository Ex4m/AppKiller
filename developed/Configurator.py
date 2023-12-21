import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import re
import pickle
import os

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
        self.numbering = numbering
        
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)  # Nastaví šířku rámečku

        self.edit1 = QLineEdit()
        self.edit1.setPlaceholderText('i.e. Perl.exe')
        self.edit2 = QLineEdit()
        self.edit2.setPlaceholderText('i.e. serverApp')

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
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 400, 300, 300)
        self.setWindowTitle("App Killer")

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon = QIcon(script_dir + '/PerlKillerIco.ico')
        self.setWindowIcon(icon)
        
        self.sections = []

        self.mainLayout = QVBoxLayout(self)
        self.sectionLayout = QVBoxLayout(self)
        self.menuLayout = QVBoxLayout(self)
        
        self.lowerMenuLayout = QHBoxLayout(self)
        self.lowerUpperMenuLayout = QHBoxLayout(self)

        self.add_section()  # 1st sekce
        self.add_section()  # 2nd sekce
        
        self.rem_button = QPushButton('Remove Last Section')
        self.rem_button.clicked.connect(self.remove_section)
        self.lowerUpperMenuLayout.addWidget(self.rem_button)
        
        self.sec_button = QPushButton('Add Section')
        self.sec_button.clicked.connect(self.add_section)
        self.lowerMenuLayout.addWidget(self.sec_button)
        

        self.exp_button = QPushButton('Export')
        self.exp_button.clicked.connect(self.export)
        self.lowerMenuLayout.addWidget(self.exp_button)
        
        self.menuLayout.addLayout(self.lowerUpperMenuLayout)
        self.menuLayout.addLayout(self.lowerMenuLayout)
        
        self.mainLayout.addLayout(self.sectionLayout)
        self.mainLayout.addLayout(self.menuLayout)
        self.setLayout(self.mainLayout)

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
                    MessageHandler.show_error(f'{section.numbering}. section\n cannot be active and not filled.')
                    return False
                if not re.search(r'\.exe$', section.edit1.text()):
                    MessageHandler.show_warning(f'{section.numbering}. section\n App to kill need to contain .exe as well.')
                
        return True

                    
    def export(self):
        if not self.checkCompletness():
            return 
        config_data = []
        
        for section in self.sections:
            if section.checkbox.isChecked():
                config_data.append({
                    'section_number': section.edit1.text(),
                    'app_path': section.edit2.text()
                })
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(script_dir, 'AKconfig.pkl') 

            with open(file_path, 'wb') as file:
                pickle.dump(config_data, file)

            MessageHandler.show_information('Configuration exported successfully.')            
        except Exception as error:
            MessageHandler.show_error(f"There was some kind of export error - {error}")
            
            
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
    def show_information(message, parent=None ):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(message)
        msg_box.exec_()
    
    @staticmethod 
    def show_question(message, parent=None ):
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Question")
        msg_box.setText(message)
        msg_box.exec_()
        
    
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()