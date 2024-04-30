from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCharts import *
from PySide6.QtStateMachine import *
from PySide6.QtWidgets import QWidget
from qtconsole.rich_jupyter_widget import RichJupyterWidget
import sys

# import sys
# from qtpy import QtWidgets

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = "python"


class IPythonConsole(QMainWindow):
    """A window that contains a single Qt console."""

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        """Start a kernel, connect to it, and create a RichJupyterWidget to use it"""
        kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
        kernel_manager.start_kernel()
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()
        jupyter_widget = RichJupyterWidget()
        jupyter_widget.set_default_style("linux")  # "lightbg"
        jupyter_widget.kernel_manager = kernel_manager
        jupyter_widget.kernel_client = kernel_client
        self.jupyter_widget = jupyter_widget
        self.setCentralWidget(self.jupyter_widget)

    def shutdown_kernel(self):
        print("Shutting down kernel...")
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IPythonConsole()
    window.show()
    sys.exit(app.exec_())
