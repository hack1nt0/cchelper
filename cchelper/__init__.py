from typing import List, Any, Sequence, Type, Dict, Tuple

import os
import dataclasses
import sys
import json
import multiprocessing
import time
import io
from threading import Thread, Event
from subprocess import Popen, PIPE, DEVNULL
from typing import IO
import asyncio
import aiofiles
import time
import psutil
import pathlib
import os
import subprocess
from datetime import datetime
import shutil
from collections import defaultdict, deque
import re
import html
import traceback

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, Future
import threading
import enum
import pickle

T, F = True, False

MARK_V = "✔"
MARK_X = "✘"
MARK_O = "●"

W, H = 750, 750

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCharts import *
from PySide6.QtStateMachine import *


WHITE = QColor(255, 255, 255)
BLACK = QColor(0, 0, 0)
BLUE = QColor(0, 0, 128)
RED = QColor(128, 0, 0)
GREEN = QColor(0, 128, 0)
YELLOW = QColor(255, 255, 0)  # TODO
PINK = QColor(255, 0, 255)  # TODO


SZ_UNIT = ["", "K", "M", "G", "T", "P"]


def time_str(timestamp: int) -> str:
    return None if timestamp is None else QDateTime.fromSecsSinceEpoch(timestamp)


def bytes_str(bs: int) -> str:
    p = 0
    while bs >= 1024:
        p += 1
        bs /= 1024
    return f"{round(bs, 2)}{SZ_UNIT[p]}B"



import logging
from .logger import logger
from .db import db
from .entity import *
import cchelper.paths as paths
from .windows import *
from .parallels import *

windows: Dict[str, QWidget] = {}


def popup_window(clazz, parent=None):
    name = f"{clazz.__name__}"
    if name in windows:
        w = windows[name]
        w.show()
        w.raise_()
        w.activateWindow()
    else:
        w = clazz(parent)
        w.setWindowFlags(Qt.WindowType.Window)
        w.show()
        windows[name] = w
    return w
