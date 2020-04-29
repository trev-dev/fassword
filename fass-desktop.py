import sys
import pdb
from fassword.utils import (
    load_data,
    save_data,
    create_storage,
    encrypt
)
from widgets.Passwords import CreatePassword, VerifyMaster
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem
)


class Fassword(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Fassword - A Password Manager"
        self.position = (50, 50)
        self.dimens = (500, 500)
        self.create_password = CreatePassword()
        self.data = load_data()
        self.entries = QListWidget()
        self.unlocked = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.position, *self.dimens)

        if not self.data:
            self.create_password.initUI(master=True)
            self.create_password.password_signal.connect(self.new_master)
        else:
            self.verify_master = VerifyMaster(
                self.data['key'],
                self.data['master']
            )
            self.verify_master.unlock_signal.connect(self.unlock_storage)
            self.verify_master.initUI()

    def new_master(self, password):
        self.create_password.hide()
        master, key = encrypt(password)
        save_data(create_storage(master, key))
        self.refresh()
        self.show()

    def refresh(self):
        self.data = load_data()
        columns = QGridLayout()
        top = QVBoxLayout()
        bottom = QVBoxLayout()

        for entry in self.data['entry']:
            self.entries.addItem(QListWidgetItem(entry))

        top_label = QLabel('Entries')
        top.addWidget(top_label)
        top.addWidget(self.entries)
        top.addStretch(1)

        bottom_label = QLabel('Options')
        bottom.addWidget(bottom_label)
        bottom.addStretch(1)

        columns.addLayout(top, 0, 0)
        columns.addLayout(bottom, 1, 0)
        self.setLayout(columns)

    def unlock_storage(self, unlock):
        if unlock:
            self.unlocked = True
            self.refresh()
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    run = Fassword()
    sys.exit(app.exec_())
