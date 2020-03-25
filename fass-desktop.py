import sys
from fassword.entries import init_data
from fassword.utils import load_data
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
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
        hbox = QVBoxLayout()

        hbox.addWidget(password_label)
        hbox.addWidget(self.password)
        hbox.addWidget(confirm_label)
        hbox.addWidget(self.confirm)
        hbox.addWidget(submit)
        hbox.addWidget(self.feedback)

        submit.clicked.connect(self.submit_handler)

        self.setLayout(hbox)

    def submit_handler(self):
        if self.password.text() != self.confirm.text():
            self.feedback.setText('Passwords do not match!')
        elif not self.password.text():
            self.feedback.setText('You must choose a password.')
        else:
            self.feedback.clear()
            self.password_signal.emit(self.password.text())


class Fassword(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Fassword - A Password Manager"
        self.position = (50, 50)
        self.dimens = (500, 500)
        self.data = load_data()
        self.setup = Setup()
        self.setup.password_signal.connect(self.new_master)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.position, *self.dimens)
        self.show()
        if not self.data:
            self.setup.show()

    def new_master(self, password):
        print(password)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    run = Fassword()
    sys.exit(app.exec_())
