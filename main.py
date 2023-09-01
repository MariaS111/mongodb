from functools import partial
from PyQt5 import uic
import backend
from context_manager import MongoDBConnection
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox


class WelcomeWindow(QMainWindow):

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi("WelcomeWindow.ui", self)


class LoginWindow(QMainWindow):

    def __init__(self, users, shelves):
        super(LoginWindow, self).__init__()
        self.shelf_window = None
        uic.loadUi("LoginWindow.ui", self)
        self.users = users
        self.shelves = shelves
        self.signInButton.clicked.connect(self.login)

    def login(self):
        username = self.nameInput.text()
        password = self.passwordInput.text()
        if username and password:
            response = backend.login(self.users, username, password)
            if response:
                print(response)
                # self.message.setText(response['_id'])
                self.shelf_window = ShelfWindow(self.shelves, response['_id'])
                self.shelf_window.show()
                self.shelf_window.show_books_from_shelf()
                self.close()
            else:
                self.message.setText('User doesn\'t exists')
        else:
            self.message.setText('No credential provided')


class ShelfWindow(QMainWindow):

    def __init__(self, shelves, user):
        super(ShelfWindow, self).__init__()
        uic.loadUi("ShelfWindow.ui", self)
        self.shelves = shelves
        self.user = user

    def show_books_from_shelf(self):
        response = backend.get_shelf(self.shelves, self.user)
        # self.vertical_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        print(response)
        row, column = 0, 0

        for key, value in response.items():
            if key == 'books':
                for i in range(len(response['books'])):
                    vertical_layout = QVBoxLayout()
                    for k, v in response['books'][i].items():
                        label = QLabel(f"{k}: {v}")
                        vertical_layout.addWidget(label)
                    radio_button = QCheckBox()
                    radio_button.setText('Mark as read')
                    vertical_layout.addWidget(radio_button)
                    self.grid_layout.addLayout(vertical_layout, row, column)
                    column += 1
                    if column == 5:
                        column = 0
                        row += 1
        self.scrollArea.setLayout(self.grid_layout)

        # self.widget = QWidget()
        # self.widget.setLayout(self.vertical_layout)
        # self.setCentralWidget(self.widget)


class RegisterWindow(QMainWindow):
    def __init__(self, users, shelves):
        super(RegisterWindow, self).__init__()
        uic.loadUi("RegisterWindow.ui", self)
        self.users = users
        self.shelves = shelves
        self.signUpButton.clicked.connect(self.register)

    def register(self):
        username = self.nameInput.text()
        password = self.passwordInput.text()
        password2 = self.password2Input.text()
        if username and password and password2 and password == password2:
            response = backend.register(self.users, self.shelves, username, password)
            if response:
                self.message.setText(response['name'])
            else:
                self.message.setText('This name is already taken or password is less than 8 characters')
        else:
            self.message.setText('Fill all fields correctly and try again')


class MainWindow:

    def __init__(self, users,  books, shelves):
        self.users_collection = users
        self.books_collection = books
        self.shelves_collection = shelves
        self.register_window = None
        self.welcome_window = None
        self.login_window = None

    def show_main_window(self):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.loginButton.clicked.connect(self.show_login_window)
        self.welcome_window.registerButton.clicked.connect(self.show_register_window)
        self.welcome_window.show()

    def show_login_window(self):
        self.login_window = LoginWindow(self.users_collection, self.shelves_collection)
        self.login_window.show()

    def show_register_window(self):
        self.register_window = RegisterWindow(self.users_collection, self.shelves_collection)
        self.register_window.show()


if __name__ == '__main__':
    uri = "mongodb://localhost:27017/"
    with MongoDBConnection(uri) as client:
        db = client['MongoTest']
        users_collection = db['users']
        books_collection = db['books']
        shelves_collection = db['shelves']
        app = QApplication(sys.argv)
        window = MainWindow(users_collection, books_collection, shelves_collection)
        window.show_main_window()
        sys.exit(app.exec_())