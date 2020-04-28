from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from fassword.utils import (
    encrypt,
    decrypt
)


class VerifyMaster(QWidget):
    unlock_signal = pyqtSignal(bool)

    def __init__(self, key, master):
        super().__init__()
        self.key = key
        self.master = master
        self.title = "Unlock Passwords"
        self.position = (150, 200)
        self.dimens = (300, 150)
        self.password = QLineEdit()
        self.button = QPushButton('Confirm')
        self.feedback = QLabel()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.position, *self.dimens)
        self.setFixedSize(*self.dimens)

        self.input_label = QLabel('Enter Master Password:')
        self.password.setEchoMode(QLineEdit.Password)
        self.button.clicked.connect(self.button_handler)
        self.password.returnPressed.connect(self.button_handler)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        layout.addWidget(self.feedback)
        self.setLayout(layout)
        self.show()

    def button_handler(self):
        password = decrypt(self.master, self.key)

        if password == self.password.text():
            self.feedback.setText('')
            self.unlock_signal.emit(True)
            self.hide()
        else:
            self.feedback.setText('Incorrect Password!')


class CreatePassword(QWidget):
    password_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.title = "Create Password"
        self.position = (150, 200)
        self.dimens = (300, 200)
        self.password = QLineEdit()
        self.confirm = QLineEdit()
        self.feedback = QLabel()

    def initUI(self, master=False):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.position, *self.dimens)
        self.setFixedSize(*self.dimens)

        prompt = 'Choose a new password'

        if master:
            prompt = 'Choose a master password'

        password_label = QLabel(prompt)
        confirm_label = QLabel('Confirm your password')
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm.setEchoMode(QLineEdit.Password)
        submit = QPushButton('Submit')
        vbox = QVBoxLayout()

        vbox.addWidget(password_label)
        vbox.addWidget(self.password)
        vbox.addWidget(confirm_label)
        vbox.addWidget(self.confirm)
        vbox.addWidget(submit)
        vbox.addWidget(self.feedback)

        submit.clicked.connect(self.submit_handler)
        self.password.returnPressed.connect(self.submit_handler)
        self.confirm.returnPressed.connect(self.submit_handler)

        self.setLayout(vbox)
        self.show()

    def submit_handler(self):
        if self.password.text() != self.confirm.text():
            self.feedback.setText('Passwords do not match!')
        elif not self.password.text():
            self.feedback.setText('You must choose a password.')
        else:
            self.feedback.clear()
            self.password_signal.emit(self.password.text())
