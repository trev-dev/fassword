import sys
from fassword.utils import (
    load_data,
    save_data,
    create_storage,
    encrypt
)
from widgets.Setup import Setup
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
)


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
        self.setFixedSize(*self.dimens)
        if not self.data:
            self.setup.show()
        else:
            self.show()

    def new_master(self, password):
        self.show()
        self.setup.hide()
        master, key = encrypt(password)
        save_data(create_storage(master, key))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    run = Fassword()
    sys.exit(app.exec_())
