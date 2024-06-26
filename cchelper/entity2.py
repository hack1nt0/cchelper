import dataclasses
from dataclasses import dataclass, field
import time
import enum
import os
from .db import db
from typing import List, Tuple, Dict, Any
import json
import glob
import pickle
import shutil
from pathlib import Path
import itertools
import math
import io
from concurrent.futures import ThreadPoolExecutor

T, F = True, False
import cchelper.paths as paths
from .logger import logger

__all__ = [
    "Language",
    "TS",
    "Task",
    "Test",
    "Verdict",
    "VS",
    "CT",
    "IT",
    "AT",
    "File",
    "TokenFile",
    "conf",
]


@dataclasses.dataclass
class Language:
    name: str = ""
    suffix: str = ""
    template: str = ""
    debug: str = ""
    release: str = ""
    run: str = ""


class Configuration:
    def __init__(
        self,
    ) -> None:
        self.fn = paths.data("db", "config.json")
        self.reload()

    def reload(self):
        with open(self.fn, "r") as r:
            self.dat = json.load(r)

    def reset(self):  # restore to defaults
        self.dat = {
            "project_dir": "/Users/dy/cc",
            "solver": "Solver.cpp",
            "generator": "Generator.py",
            "jurger": "Jurger.cpp",
            "editor": "/usr/local/bin/code",
            "parallel": 1,
            "refresh_rate": 10,
            "languages": [
                {
                    "name": "C++",
                    "suffix": ".cpp",
                    "template": r"""
#include "debug.h"

void solve(int it) {}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(&cout);
    int n; cin >> n;
    for (int i = 0; i < n; ++i) {
        int x, y;
        cin >> x >> y;
        cout << x + y << '\n';
    }
    return 0;
}
""",
                    "debug": r"/usr/bin/c++ -I/Users/dy/cc/include -std=c++20 -g -Wall -DDEBUG -fsanitize=address -fsanitize=undefined -o {}.exe {}.cpp",
                    "release": r"/usr/bin/c++ -I/Users/dy/cc/include -std=c++20 -O2 -Wall -o {}.exe {}.cpp",
                    "run": r"{}.exe",
                },
                {
                    "name": "Python",
                    "suffix": ".py",
                    "template": r"""
import random
n = int(1e6)
print(n)
for _ in range(n):
    x = random.randint(0, 10)
    y = random.randint(0, 10)
    print(x, y)
""",
                    "debug": "",
                    "release": "",
                    "run": r"/opt/homebrew/bin/python3 {}.py",
                },
            ],
            "tags": [
                "*",
                "Solved",
                "Hard",
                "Stupid",
                "Ad hoc",
                "Dynamic Programming",
                "Data Structure",
                "Math",
            ],
            "bytes_per_page": 100000,
            "bytes_per_cell": 1000,
            "bytes_per_read": 1000000,
            "rows_per_page": 100,
            "build_debug": True,
            "build_release": False,
            "build_asneed": False,
            "run_inshell": True,
            "submit_code": True,
            "submit_data": False,
            "submit_withmain": True,
            "log_level": "DEBUG",
            "exe_dump_delay": 1,
            "exe_warm_delay": 2,
            "font": None,
        }
        self.save()

    def save(self):
        with open(self.fn, "w") as w:
            json.dump(self.dat, w, indent=4)

    @property
    def project_dir(self) -> str:
        return self.dat["project_dir"]

    def working_dir(self, *args) -> str:
        return os.path.join(self.project_dir, "cchelper", *map(str, args))

    @property
    def solver(self) -> str:
        return self.dat["solver"]

    @property
    def generator(self) -> str:
        return self.dat["generator"]

    @property
    def jurger(self) -> str:
        return self.dat["jurger"]

    @property
    def editor(self) -> str:
        return self.dat["editor"]

    @property
    def parallel(self) -> int:
        return self.dat["parallel"]

    @property
    def refresh_rate(self) -> int:
        return self.dat["refresh_rate"]

    @property
    def languages(self) -> List[Language]:
        return [Language(**dat) for dat in self.dat["languages"]]

    @property
    def prefer_lang(self) -> Language:
        return [
            lang
            for lang in conf.languages
            if lang.suffix == os.path.splitext(conf.solver)[-1]
        ][0]

    @property
    def tags(self) -> List[str]:
        return self.dat["tags"]

    @property
    def bytes_per_cell(self) -> int:
        return self.dat["bytes_per_cell"]

    @property
    def bytes_per_page(self) -> int:
        return self.dat["bytes_per_page"]

    @property
    def bytes_per_read(self) -> int:
        return self.dat["bytes_per_read"]

    @property
    def rows_per_page(self) -> int:
        return self.dat["rows_per_page"]

    @property
    def build_debug(self) -> bool:
        return self.dat["build_debug"]

    @property
    def build_asneed(self) -> bool:
        return self.dat["build_asneed"]

    @property
    def run_inshell(self) -> bool:
        return self.dat["run_inshell"]

    @property
    def submit_code(self) -> bool:
        return self.dat["submit_code"]

    @property
    def submit_withmain(self) -> bool:
        return self.dat["submit_withmain"]

    @property
    def log_level(self) -> str:
        return self.dat["log_level"]

    @property
    def crawl_timeout(self) -> int:
        return 10

    @property
    def exe_dump_delay(self) -> int:
        return self.dat["exe_dump_delay"]

    @property
    def exe_warm_delay(self) -> int:
        return self.dat["exe_warm_delay"]

    @property
    def font(self) -> Tuple[str, int]:
        dat = self.dat["font"].split(',')
        return (dat[0], int(dat[1]))

    @property
    def graphviz(self) -> str:
        return self.dat.get("graphviz")

conf = Configuration()


class CT(enum.Enum):
    TBT = "Token By Token"
    CBC = "Char By Char"


@dataclasses.dataclass
class File:
    path: str

    def __post_init__(self):
        if not os.path.exists(self.path):
            root = os.path.dirname(os.path.abspath(self.path))
            os.makedirs(root, exist_ok=T)
            with open(self.path, "w") as w:
                pass

    def __iadd__(self, value: bytes | str):
        if value is None:
            return self
        if type(value) != bytes:  # TODO
            value = str(value).encode()
        with open(self.path, "ab", buffering=0) as w:
            w.write(value)
            w.write(b"\n")
        return self

    def clear(self):
        with open(self.path, "wb", buffering=0) as w:
            w.truncate(0)
            w.seek(
                0
            )  # Important, else you will have weird \x00 appended at the start of the file.

    # tail
    def summary(self, MAX_CS=100):
        with open(self.path, "rb", buffering=0) as r:
            L = r.seek(0, 2)
            L1 = (MAX_CS + 1) // 2
            L2 = MAX_CS // 2
            R1 = (0, min(L, L1))
            R2 = (max(R1[1], L - L2), L)
            L1 = R1[1] - R1[0]
            L2 = R2[1] - R2[0]
            r.seek(0, 0)
            S1 = r.read(L1)
            r.seek(-L2, 2)
            S2 = r.read(L2)
            M = "... ..." if R1[1] < R2[0] else ""
            return M.join((S1.decode(), S2.decode()))

    def tail(self, MAX_CS=1000) -> str:
        with open(self.path, "rb", buffering=0) as r:
            L = r.seek(0, 2)
            L2 = min(MAX_CS, L)
            r.seek(-L2, 2)
            S = r.read(L2)
            # H = "..." if L2 < L else ""
            return S.decode(errors="ignore")  # TODO may cause decode error

    def head(self, MAX_CS=1000) -> str:
        with open(self.path, "rb", buffering=0) as r:
            L = r.seek(0, 2)
            r.seek(0)
            s = r.read(MAX_CS)
        s = s.decode(errors="ignore")
        if MAX_CS < L:
            s += '\n... ...'
        return s

    def __eq__(self, othr) -> bool:
        if type(othr) is not File:
            return F
        if len(self) != len(othr):
            return F
        with (
            open(self.path, "rb", buffering=0) as r1,
            open(othr.path, "rb", buffering=0) as r2,
        ):
            while T:
                c1 = r1.read(conf.bytes_per_read)
                c2 = r2.read(conf.bytes_per_read)
                if c1 != c2:
                    return F
                if len(c1) == 0:
                    return T

    def __ne__(self, othr) -> bool:
        return not (self == othr)

    def __len__(self) -> int:
        return os.path.getsize(self.path)

    @property
    def length(self) -> int:
        return len(self)

    @property
    def mtime(self) -> int:
        return round(os.path.getmtime(self.path))

    @property
    def suffix(self) -> str:
        return os.path.splitext(self.path)[1]


    @property
    def compile_cmd(self) -> str:
        prefix, suffix = os.path.splitext(self.path)
        prefix_exe = conf.working_dir('dist', os.path.splitext(os.path.basename(self.path))[0])
        lang = [lang for lang in conf.languages if lang.suffix == suffix]
        if not lang:
            return
        lang = lang[0]
        if conf.build_debug:
            cmd = lang.debug.format(prefix_exe, prefix) if lang.debug else None
        else:
            cmd = lang.release.format(prefix_exe, prefix) if lang.release else None
        return self.format_cmd(cmd)

    @property
    def execute_cmd(self) -> str:
        prefix = conf.working_dir('dist', os.path.splitext(os.path.basename(self.path))[0])
        if self.compile_cmd is None:
            prefix = conf.working_dir(os.path.splitext(os.path.basename(self.path))[0])
        suffix = os.path.splitext(self.path)[1]
        lang = [lang for lang in conf.languages if lang.suffix == suffix]
        if not lang:
            return
        lang = lang[0]
        cmd = lang.run.format(prefix)
        return self.format_cmd(cmd)

    def format_cmd(self, cmd: str) -> str | List[str] | None:
        if cmd is None:
            return
        return cmd if conf.run_inshell else cmd.split(" ")  # TODO

    @property
    def executable(self) -> str:
        prefix = conf.working_dir('dist', os.path.splitext(os.path.basename(self.path))[0])
        return prefix + ".exe"


class TokenFile(File):

    def __init__(self, obj: File) -> None:
        super().__init__(obj.path)

    def __eq__(self, othr) -> bool:
        if type(othr) is not TokenFile:
            return F
        def tokens(stream):
            for line in stream:
                for tk in line.split():
                    yield tk
        with (
            open(self.path, "r") as a,
            open(othr.path, "r") as b,
        ):
            for atoken, btoken in itertools.zip_longest(
                tokens(a), tokens(b)
            ):
                ret = F
                if atoken and btoken:
                    try:
                        ret = abs(float(atoken) - float(btoken)) < 1e-6
                    except ValueError:
                        ret = atoken == btoken
                if not ret:
                    return F
        return T


class VS(enum.Enum):
    COMPILATION_QUE = "Compilation queued"
    COMPILATION_RUN = "Compilation running"
    COMPILATION_OK = "Compilation OK"
    COMPILATION_ERR = "Compilation error"
    COMPILATION_SKP = "Compilation Skipped"

    QUE = "Queued"
    SKP = "Skipped"
    NA = "Answer Not Given"
    RUN = "Running"
    AC = "Accepted"
    RTE = "Runtime Error"
    WA = "Wrong Answer"
    OOM = "Memory Limit Exceeded"
    TLE = "Time limit Exceeded"
    QLE = "Query Limit Exceeded"

    @staticmethod
    def kind(v) -> int:
        ret = None
        match v:
            case VS.AC | VS.COMPILATION_OK:
                ret = 1
            case VS.COMPILATION_ERR | VS.RTE | VS.WA | VS.OOM | VS.TLE | VS.QLE:
                ret = 0
            case VS.SKP | VS.NA:
                ret = 2
            case _:
                ret = 3
        return ret


class IT(enum.Enum):
    MANUAL = "Manual"
    GENERATOR = "Generator"


class AT(enum.Enum):
    UNKNOWN = "Unknown"
    MANUAL = "Manual"
    JURGER = "Jurger"
    INTERACTIVE_JURGER = "Interactive-J"


@dataclasses.dataclass
class Test:
    id: int = None
    input: File = None
    answer: File = None
    status: VS = VS.QUE
    input_type: IT = IT.MANUAL
    answer_type: AT = AT.MANUAL
    checked: bool = True


import collections


# @dataclasses.dataclass
# class ComplilationVerdict:
#     id: int
#     status: VS
#     stderr: File = None
#     cmd: str = None
#     cpu: int = 0
#     mem: int = 0

#     def __bool__(self):
#         return VS.kind(self.status) > 0


@dataclasses.dataclass
class Verdict:
    id: int
    test_id: int

    status: VS
    input: File = None
    answer: File = None
    actual: File = None

    stderr: File = None
    chat: File = None

    flow_bytes: int = 0
    cpu: int = 0
    mem: int = 0
    graph: List[str] = dataclasses.field(default_factory=lambda: [])
    cmd: str = None
    status_detail: str = "..."

    added_as_test: bool = F

    @property
    def progress(self) -> int:
        try:
            return self.flow_bytes * 100 // len(self.input)
        except:
            return math.inf

    def __bool__(self):
        return VS.kind(self.status) > 0

class TS(enum.Enum):
    SOLVED = 'Solved'
    UNSURE = 'Unsure'
    UNSOLVED = 'unSolved'

@dataclass
class Task:
    name: str = ""
    id: int = None
    tags: int = 1  # Solved
    status: TS = TS.UNSURE
    url: str = ""
    doc: str = ""

    cpu: int = 1000
    mem: int = 128
    interactive: bool = False
    qry: int = 16

    ctime: int = field(default_factory=lambda: int(time.time()))
    solver: File = None
    generator: File = None
    jurger: File = None
    gcount: int = 100

    comp_type: CT = CT.TBT

    tests: List[Test] = dataclasses.field(default_factory=lambda: [])
    # files: List[File] = dataclasses.field(default_factory=lambda: [])
    verdicts: List[Verdict] = dataclasses.field(default_factory=lambda: [])

    def __str__(self):
        return self.name

    @staticmethod
    def load() -> List:
        tasks = []
        for task_dir in glob.glob(paths.data("stash", "*")):
            with open(os.path.join(task_dir, "meta.pickle"), "rb") as r:
                task = pickle.load(r)
            tasks.append(task)
        return tasks

    def dump(self):
        with open(paths.data("stash", self.name, "meta.pickle"), "wb") as w:
            pickle.dump(self, w)

    # memory -> db
    def arxiv(self):
        task_dict = dataclasses.asdict(self)
        del task_dict["verdicts"]
        task_dict["tests"] = len(self.tests)
        task_dict["comp_type"] = self.comp_type.value
        task_dict["solver"] = os.path.relpath(self.solver.path, self.stash_dir())
        task_dict["generator"] = os.path.relpath(self.generator.path, self.stash_dir())
        task_dict["jurger"] = os.path.relpath(self.jurger.path, self.stash_dir())

        db.execute(
            (
                f"insert or replace into task ({','.join(task_dict.keys())}) values ({','.join(['?'] * len(task_dict))})",
                tuple(task_dict.values()),
            )
        )
        tid = db.query((f"select id from task where name=?", (self.name,)))[0]["id"]
        for test in self.tests:
            db.execute(
                (
                    f"insert or replace into test (id, task_id, test_id, checked, status, input_type, answer_type) values (?,?,?,?,?,?,?)",
                    (
                        None,
                        tid,
                        test.id,
                        test.checked,
                        test.status.value,
                        test.input_type.value,
                        test.answer_type.value,
                    ),
                )
            )
        for file in [self.solver, self.generator, self.jurger] + [
            file for test in self.tests for file in (test.input, test.answer)
        ]:
            db.execute(
                (
                    f"insert or replace into file (id, task_id, path, content) values (?,?,?,?)",
                    (
                        None,
                        tid,
                        os.path.relpath(file.path, self.stash_dir()),
                        open(file.path).read(),
                    ),
                )
            )
    
    def create_symlinks(self):
        os.makedirs(conf.working_dir(), exist_ok=T)
        for file in (self.solver, self.generator, self.jurger):
            source = file.path
            target = conf.working_dir(os.path.basename(file.path))
            paths.remove_symlink(target)
            os.symlink(source, target)

    def remove_symlinks(self):
        for file in (self.solver, self.generator, self.jurger):
            target = conf.working_dir(os.path.basename(file.path))
            try:
                os.remove(target)
            except:
                pass

    def stash_dir(self, *args):
        return paths.data("stash", self.name, *map(str, args))

    def verdict_dir(self, *args):
        return paths.data("stash", self.name, "V", *map(str, args))

    def test_dir(self, *args):
        return paths.data("stash", self.name, "T", *map(str, args))

    def file_dir(self, *args):
        return paths.data("stash", self.name, "F", *map(str, args))
