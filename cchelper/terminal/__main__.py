from cchelper import *
from .testio import TestIO

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TestIO()
    w.show()
    w.resize(400, 400)
    app.exec()
