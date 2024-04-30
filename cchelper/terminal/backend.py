from cchelper import *
import paramiko
import threading
import time
import uuid
import os
from pyte.screens import Screen, HistoryScreen
from pyte.streams import Stream, ByteStream
import shlex
import pty


class LocalPty:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._screen = HistoryScreen(width, height, history=9999, ratio=0.3)
        self._stream = ByteStream(self._screen)
        self.master_fd, self.slave_fd = pty.openpty()
        # disable echo
        # import termios
        # term_attrs = termios.tcgetattr(self.slave_fd)
        # term_attrs[3] = term_attrs[3] & ~termios.ECHO & ~termios.ICANON
        # termios.tcsetattr(self.slave_fd, termios.TCSANOW, term_attrs)
        # tty.setraw(self.slave_fd)
        # tty.setcbreak(self.slave_fd)
        # start app/shell
        env = os.environ.copy()
        env["TERM"] = "xterm"
        # env["LC_ALL"] = "en_GB.UTF-8"
        env["COLUMNS"] = str(width)
        env["LINES"] = str(height)
        self.process = Popen(
            args=shlex.split("zsh"),
            env=env,
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            # preexec_fn=os.setsid, #TODO
        )
        os.close(self.slave_fd)  # TODO

    #     global_threadpool.submit(self.loop)

    # def loop(self):
    #     while True:
    #         data = self.read()
    #         if not data:
    #             break

    def read(self) -> bytes:
        data = os.read(self.master_fd, 1024)
        self._stream.feed(data)
        return data

    def write(self, data: bytes):
        os.write(self.master_fd, data)

    def close(self):
        self.process.kill()

    def resize(self, width, height):
        self._screen.resize(width, height)

    def __str__(self):
        return "\n".join(self._screen.display)

    def cursorP(self):
        return (
            self._screen.cursor.y * (self._screen.columns + 1) + self._screen.cursor.x
        )


class SshTty:

    def __init__(self, width, height, ip, username=None, password=None):
        self.width = width
        self.height = height
        self.ip = ip
        self.username = username
        self.password = password
        self._screen = HistoryScreen(width, height, history=9999, ratio=0.3)
        self._stream = ByteStream(self._screen)

        self.ssh_client = None
        self.channel = None
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.ip, username=self.username, password=self.password)
        self.channel = self.ssh_client.get_transport().open_session()
        self.channel.get_pty(width=self.width, height=self.height)
        self.channel.invoke_shell()

        timeout = 60
        while not self.channel.recv_ready() and timeout > 0:
            time.sleep(1)
            timeout -= 1

        self.channel.resize_pty(width=self.width, height=self.height)

        global_threadpool.submit(self.loop)

    def loop(self):
        while True:
            data = self.read()
            if not data:
                break

    def read(self) -> bytes:
        data = self.channel.recv(1024)
        self._stream.feed(data)
        return data

    def write(self, data):
        self.channel.send(data)

    def resize(self, width, height):
        if self.channel:
            self.channel.resize_pty(width=width, height=height)
        self._screen.resize(width, height)

    def close(self):
        self.ssh_client.close()

    def __str__(self):
        return "\n".join(self._screen.display)

    def cursorP(self):
        return (
            self._screen.cursor.y * (self._screen.columns + 1) + self._screen.cursor.x
        )
