from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from criteria import Criteria
from requests_file import Requests
from file_operations import FileOperations
from input_validation import ErrorHandling
import time
import webbrowser

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rent apartment finder in Helsinki")
        self.setGeometry(100, 100, 950, 950)
        self.criteria = None
        self.requests = None
        self.file_operations = FileOperations()
        self.errors = ErrorHandling()
        self.starting_parametres()

    def starting_parametres(self):

        self.price = QLineEdit(self, placeholderText="Enter the max rent per month (as a positive integer)")
        self.price.setFont(QFont('Arial', 11))

        self.price.setGeometry(0, 20, 850, 30)
        self.price.setValidator(QIntValidator(0, 100000))

        self.code = QLineEdit(self, placeholderText="Enter the postal codes of preferred districts separated by comma. e.g. 00100, 00120")
        self.code.setFont(QFont('Arial', 11))

        self.code.setGeometry(0, 50, 850, 30)

        self.size = QLineEdit(self, placeholderText="Enter min m^2 of the apartment (as a positive integer)")
        self.size.setFont(QFont('Arial', 11))

        self.size.setGeometry(0, 80, 850, 30)
        self.size.setValidator(QIntValidator(0, 100000))
        self.button = QPushButton("Proceed", clicked=lambda: self.button_press_event())
        self.button.setGeometry(850, 80, 90, 30)
        self.layout().addWidget(self.button) #add widgets of the first parametres that are asked. Validate integer inputs

    def button_press_event(self):
        price = self.price.text()
        code = self.code.text()
        size = self.size.text()
        try:
            self.errors.validate_string_input(code)
            self.criteria = Criteria(price, code, size)
            self.requests = Requests(price, code, size, self.criteria, self.file_operations)

            time.sleep(5)
            self.num_of_apartments_msgbox(1)
            self.added_parametres()
        except ValueError as e:
            self.error_msgboxes(str(e)) #validate the postal code input, if input is okay, pass the parametres to other files

    def num_of_apartments_msgbox(self, int):
        self.msgbox = QMessageBox()
        if self.criteria.return_num_of_apartments() == 0:
            self.msgbox.setIcon(QMessageBox.Information)
            self.msgbox.setText("Didn't find any suitable apartments. Perhaps you should change your parametres?")
        elif int == 1:
            self.msgbox.setIcon(QMessageBox.Information)
            self.msgbox.setText(f"Found {self.criteria.return_num_of_apartments()} apartments!")
        elif int == 2:
            if len(self.file_operations.return_apartment_urls()) == 0:
                self.msgbox.setIcon(QMessageBox.Information)
                self.msgbox.setText("Didn't find any suitable apartments. Perhaps you should change your parametres?")
            else:
                response = self.msgbox.question(window, "Apartments found", f"Found {len(self.file_operations.return_apartment_urls())} apartment(s)! Open the url(s)?", self.msgbox.Yes | self.msgbox.No)
                if response == self.msgbox.Yes:
                    for i in self.file_operations.return_apartment_urls():
                        webbrowser.open(i)
                    self.msgbox.setVisible(False)
                elif response == self.msgbox.No:
                    self.msgbox.setText("You can open the URLs from the button on the right side")
        self.msgbox.setFont(QFont("Arial", 14))

        self.msgbox.setGeometry(200, 500, 650, 100)
        self.msgbox.setStyleSheet("color: black; background: white")
        self.layout().addWidget(self.msgbox) #message box for informing the user how many apartments were found

    def error_msgboxes(self, error):
        self.errorbox = QMessageBox()
        self.errorbox.setIcon(QMessageBox.Warning)
        self.errorbox.setText(error)
        self.errorbox.setFont(QFont("Arial", 14))

        self.errorbox.setGeometry(200, 500, 650, 100)
        self.errorbox.setStyleSheet("color: black; background: white")
        self.layout().addWidget(self.errorbox) #error messagebox if some of the inputs wasn't written correctly


    def added_parametres(self):
        self.floor = QLineEdit(self, placeholderText="In what floor should the apartment be? E.g. higher or equal to [floor] 4")
        self.floor.setFont(QFont('Arial', 11))
        self.floor.setGeometry(0, 200, 850, 30)
        self.floor.setValidator(QIntValidator(0, 20))
        self.layout().addWidget(self.floor)

        options = ["Tyydyttävä", "Hyvä", "Erinomainen"]
        self.condition = QComboBox()
        [self.condition.addItem(f"{i}") for i in options]
        self.condition_label = QLabel("What condition should the apartment be in:")
        self.condition_label.setGeometry(0, 230, 850, 30)

        self.condition_label.setFont(QFont('Arial', 11))
        self.layout().addWidget(self.condition_label)
        self.condition.setGeometry(0, 260, 850, 30)
        self.layout().addWidget(self.condition)

        yes_no = ["Yes", "No"]
        self.balcony = QComboBox()
        [self.balcony.addItem(f"{i}") for i in yes_no]
        self.balcony_label = QLabel("Should the apartment have a balcony?")
        self.balcony_label.setGeometry(0, 290, 850, 30)

        self.balcony_label.setFont(QFont('Arial', 11))
        self.layout().addWidget(self.balcony_label)
        self.balcony.setGeometry(0, 320, 850, 30)
        self.layout().addWidget(self.balcony)

        self.year_built = QLineEdit(self, placeholderText="How new the building should be? E.g. it should've been built after year 2000")
        self.year_built.setFont(QFont('Arial', 11))
        self.year_built.setGeometry(0, 350, 850, 30)
        self.year_built.setValidator(QIntValidator(1750, 2022))
        self.layout().addWidget(self.year_built)

        self.confirm = QPushButton("Proceed", clicked=lambda: self.confirmed_input())
        self.confirm.setGeometry(850, 350, 90, 30)
        self.progress_bar()
        self.layout().addWidget(self.confirm) #get more parametres from the user so we can filter the apartments even more

    def progress_bar(self):
        self.progress = QProgressBar()
        self.progress.setRange(0, self.criteria.return_num_of_apartments())
        self.progress.setGeometry(200, 550, 400, 100)
        self.layout().addWidget(self.progress)

        self.progress_label = QLabel()
        self.progress_label.setGeometry(170, 450, 600, 100)
        self.progress_label.setFont(QFont("Arial", 12))
        self.layout().addWidget(self.progress_label)

        self.progress.hide() #widgets for the progress bar and a label for it

    def confirmed_input(self):
        floor = self.floor.text()
        condition = self.condition.currentText()
        balcony = self.balcony.currentText()
        year_built = self.year_built.text()

        self.criteria.floor = int(floor)
        self.criteria.condition = condition
        self.criteria.balcony = balcony
        self.criteria.year_built = int(year_built)

        self.progress_label.setText("Checking if the apartments fulfil your criteria...")
        self.progress.show()
        for value in self.requests.get_requests_to_apartments():
            self.progress.setValue(value)

        self.progress.hide()
        self.progress_label.setText("")
        self.num_of_apartments_msgbox(2) #user confirms the added parametres, show the progress bar and when the GET requests are done, show many apartments were found and if the user wants to open the URLs
        if len(self.file_operations.return_apartment_urls()) > 0:
            self.open_apartment_file()

    def open_apartment_file(self):
        self.apartments = QPushButton("Open the URLs", clicked=lambda: self.open_urls())
        self.apartments.setFont(QFont("Arial", 13))
        self.apartments.setGeometry(700, 650, 250, 50)
        self.layout().addWidget(self.apartments)

    def open_urls(self):
        for i in self.file_operations.return_apartment_urls():
            webbrowser.open(i)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
