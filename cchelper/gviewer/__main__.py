
from cchelper import *
from .gviewer import GViewer

if __name__ == "__main__":
    app = QApplication()
    with open(paths.data("cchelper.css"), "r") as r:
        app.setStyleSheet(r.read())
    w = GViewer(None)
    w.show()
    sys.exit(app.exec())