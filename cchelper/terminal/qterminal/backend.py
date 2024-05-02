import pyte
import paramiko
import threading
import time
import uuid
import traceback
import sys
import subprocess, os
from cchelper import *
import typing

_WIN = sys.platform == "win32"
if _WIN:
    import winpty
else:
    import pty, tty
    import termios
    import struct
    import fcntl

DEFAULT_ROWS, DEFAULT_COLS = 100, 80


class BasePty(object):
    def __init__(self):
        self.screen = pyte.HistoryScreen(DEFAULT_COLS, DEFAULT_ROWS, ratio=0.3)
        self.stream = pyte.ByteStream(self.screen)
        self.cursorX = 0
        self.cursorY = 0

    @property
    def rows(self) -> int:
        return self.screen.lines

    @property
    def cols(self) -> int:
        return self.screen.columns

    def connect(self):
        pass

    def write_to_screen(self, dat: bytes):
        try:
            self.stream.feed(dat)
        except:  # TODO vim
            pass

    def write(self, dat: bytes):
        pass

    def read(self) -> bytes:
        pass

    def resize(self, rows: int, cols: int):
        self.screen.resize(columns=cols, lines=rows)

    @property
    def dirtyRows(self):
        return self.screen.dirty
    
    def clearDirty(self):
        self.screen.dirty.clear()
    
    def row(self, idx: int):
        line = self.screen.buffer[idx]
        for col in range(self.cols):
            yield line[col]
    
    @property
    def cursor(self) -> pyte.screens.Cursor:
        return self.screen.cursor


class LocalPty(BasePty):

    def connect(self):
        if _WIN:
            pass
        else:
            self.masterfd, self.slavefd = pty.openpty()
            sh = 'wsl' if _WIN else os.environ.get("SHELL", "sh")
            self.process = subprocess.Popen(
                sh,
                shell=True,
                stdin=self.slavefd,
                stdout=self.slavefd,
                stderr=self.slavefd,
                close_fds=F,
            )

        self.screen.reset()

    def write(self, dat: bytes):
        while len(dat):
            nb = os.write(self.masterfd, dat)
            dat = dat[nb:]

    def read(self) -> bytes:
        return os.read(self.masterfd, 1024)

    def resize(self, rows: int, cols: int):
        if _WIN:
            pass
        else:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.masterfd, termios.TIOCSWINSZ, winsize)
            #TODO not apply to running process
            pass
        return super().resize(rows, cols)

    def close(self):
        os.close(self.masterfd)
        os.close(self.slavefd)
        self.process.terminate()


class SshPty(BasePty):

    def connect(self, ip: str, port: int, username, password):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(ip, port=port, username=username, password=password)
        self.channel = self.ssh_client.invoke_shell(
            term="xterm",
        )

        timeout = 60
        while not self.channel.recv_ready() and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        assert self.channel.recv_ready()
        self.channel.set_combine_stderr(T)
        self.channel.settimeout(None)
        self.screen.reset()

    def write(self, dat: bytes):
        while len(dat):
            send = self.channel.send(dat)
            if send == 0 and len(dat):
                logger.error(f"Pty closed before write: {dat.decode(errors='replace')}")
                return
            dat = dat[send:]

    def read(self) -> bytes:
        return self.channel.recv(1024)
    
    def resize(self, rows: int, cols: int):
        if not (rows == self.rows and cols == self.cols):
            self.channel.resize_pty(width=cols, height=rows)
            super().resize(rows, cols)

    def close(self):
        self.channel.close()
        self.ssh_client.close()
