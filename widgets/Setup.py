from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class Setup(QWidget):
    password_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.title = "Setup Fassword"
        self.position = (150, 200)
        self.dimens = (300, 200)
        self.password = QLineEdit()
        self.confirm = QLineEdit()
        self.feedback = QLabel()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.position, *self.dimens)
        self.setFixedSize(*self.dimens)

        password_label = QLabel('Choose a master password')
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

        self.setLayout(vbox)

    def submit_handler(self):
        if self.password.text() != self.confirm.text():
            self.feedback.setText('Passwords do not match!')
        elif not self.password.text():
            self.feedback.setText('You must choose a password.')
        else:
            self.feedback.clear()
            self.password_signal.emit(self.password.text())
