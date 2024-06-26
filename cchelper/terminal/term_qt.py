# https://gist.github.com/ssokolow/6f93e68d2af774aebf18667a7760cd23
"""Primitive terminal emulator example made from a PyQt QTextEdit widget."""

import fcntl, locale, os, pty, struct, sys, termios
import subprocess  # nosec
from PySide6.QtCore import *
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCharts import *
from PySide6.QtStateMachine import *

# # Quick hack to limit the scope of the PyLint warning disabler
# try:
#     # pylint: disable=no-name-in-module
#     from PyQt5.QtCore import Qt, QSocketNotifier                 # type: ignore
#     from PyQt5.QtGui import QFont, QPalette, QTextCursor         # type: ignore
#     from PyQt5.QtWidgets import QApplication, QStyle, QTextEdit  # type: ignore
# except ImportError:
#     raise

# It's good practice to put these sorts of things in constants at the top
# rather than embedding them in your code
DEFAULT_TTY_CMD = ["/bin/bash"]
DEFAULT_COLS = 80
DEFAULT_ROWS = 25

# NOTE: You can use any QColor instance, not just the predefined ones.
DEFAULT_TTY_FONT = QFont("Noto", 16)
DEFAULT_TTY_FG = Qt.lightGray
DEFAULT_TTY_BG = Qt.black

# The character to use as a reference point when converting between pixel and
# character cell dimensions in the presence of a non-fixed-width font
REFERENCE_CHAR = "W"


class PrimitiveTerminalWidget(QTextEdit):
    """Simple TERM=tty terminal emulator widget

    (Uses QTextEdit rather than QPlainTextEdit to leave the capability open to
    support colors.)
    """

    # Used to block the user from backspacing more characters than they
    # typed since last pressing Enter
    backspace_budget = 0

    

    # Persistent handle for the master side of the PTY and its QSocketNotifier
    pty_m = None
    subproc = None
    notifier = None

    def __init__(self, *args, **kwargs):
        super(PrimitiveTerminalWidget, self).__init__(*args, *kwargs)

        # Do due diligence to figure out what character coding child
        # applications will expect to speak
        self.codec = locale.getpreferredencoding()

        # Customize the look and feel
        pal = self.palette()
        pal.setColor(QPalette.Base, DEFAULT_TTY_BG)
        pal.setColor(QPalette.Text, DEFAULT_TTY_FG)
        self.setPalette(pal)
        self.setFont(DEFAULT_TTY_FONT)

        # Disable the widget's built-in editing support rather than looking
        # into how to constrain it. (Quick hack which means we have to provide
        # our own visible cursor if we want one)
        # self.setReadOnly(True)
        # self.setTextInteractionFlags(
        #     self.textInteractionFlags()
        #     | Qt.TextInteractionFlag.TextSelectableByKeyboard
        # )

    def cb_echo(self, pty_m):
        """Display output that arrives from the PTY"""
        # Read pending data or assume the child exited if we can't
        # (Not technically the proper way to detect child exit, but it works)
        try:
            # Use 'replace' as a not-ideal-but-better-than-nothing way to deal
            # with bytes that aren't valid in the chosen encoding.
            child_output = os.read(self.pty_m, 1024).decode(self.codec, "replace")
        except OSError:
            # Ask the event loop to exit and then return to it
            QApplication.instance().quit()
            return

        # Insert the output at the end and scroll to the bottom
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(child_output)
        scroller = self.verticalScrollBar()
        scroller.setValue(scroller.maximum())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.moveCursor(QTextCursor.End)
        cursor = self.textCursor()
        kc = event.keyCombination()
        print(kc.keyboardModifiers(), hex(kc.key().value))
        match kc.keyboardModifiers():
            case Qt.KeyboardModifier.NoModifier:
                match kc.key():
                    case Qt.Key.Key_Backspace:
                        if self.backspace_budget > 0:  # Backspace
                            cursor.deletePreviousChar()
                            self.backspace_budget -= 1
                    # case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                    #     self.backspace_budget = 0
                    case _:
                        char = event.text()
                        print(ord(char), char, char.encode(self.codec), char.isprintable())
                        if char and (char.isprintable() or char == "\r"):
                            cursor.insertText(char)
                        # Regardless of what we do, send the character to the PTY
                        # (Let the kernel's PTY implementation do most of the heavy lifting)
                        os.write(self.pty_m, char.encode(self.codec))
                        # os.write(self.pty_m, bytes(kc.key().value))


        # Scroll to the bottom on keypress, but only after modifying the
        # contents to make sure we don't scroll to where the bottom was before
        # word-wrap potentially added more lines
        scroller = self.verticalScrollBar()
        scroller.setValue(scroller.maximum())

    def resizeEvent(self, event):
        """Handler to announce terminal size changes to child processes"""
        # Call Qt's built-in resize event handler
        super(PrimitiveTerminalWidget, self).resizeEvent(event)

        fontMetrics = self.fontMetrics()
        win_size_px = self.size()
        char_width = fontMetrics.boundingRect(REFERENCE_CHAR).width()

        # Subtract the space a scrollbar will take from the usable width
        usable_width = (
            win_size_px.width()
            - QApplication.instance().style().pixelMetric(QStyle.PM_ScrollBarExtent)
        )

        # Use integer division (rounding down in this case) to find dimensions
        cols = usable_width // char_width
        rows = win_size_px.height() // fontMetrics.height()

        # Announce the change to the PTY
        fcntl.ioctl(
            self.pty_m, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0)
        )

        # As a quick hack, scroll to the bottom on resize
        # (The proper solution would be to preserve scroll position no matter
        # what it is)
        scroller = self.verticalScrollBar()
        scroller.setValue(scroller.maximum())

    def spawn(self, argv):
        """Launch a child process in the terminal"""
        # Clean up after any previous spawn() runs
        # TODO: Need to reap zombie children
        # XXX: Kill existing children if spawn is called a second time?
        if self.pty_m:
            self.pty_m.close()
        if self.notifier:
            self.notifier.disconnect()

        # Create a new PTY with both ends open
        self.pty_m, pty_s = pty.openpty()

        # Reset this, since it's PTY-specific
        self.backspace_budget = 0

        # Stop the PTY from echoing back what we type on this end
        term_attrs = termios.tcgetattr(pty_s)
        term_attrs[3] &= ~termios.ECHO
        termios.tcsetattr(pty_s, termios.TCSANOW, term_attrs)

        # Tell child processes that we're a dumb terminal that doesn't
        # understand colour or cursor movement escape sequences
        #
        # (This will prevent well-behaved processes from emitting colour codes
        # and will cause things which *require* cursor control like mutt and
        # ncdu to error out on startup with "Error opening terminal: tty")
        child_env = os.environ.copy()
        child_env["TERM"] = "tty"

        # Launch the subprocess
        # FIXME: Keep a reference so we can reap zombie processes
        subprocess.Popen(
            argv,  # nosec
            stdin=pty_s,
            stdout=pty_s,
            stderr=pty_s,
            env=child_env,
            preexec_fn=os.setsid,
        )

        # Close the child side of the PTY so that we can detect when to exit
        os.close(pty_s)


        # Hook up an event handler for data waiting on the PTY
        # (Because I didn't feel like looking into whether QProcess can be
        #  integrated with PTYs as a subprocess.Popen alternative)
        self.notifier = QSocketNotifier(self.pty_m, QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.cb_echo)
