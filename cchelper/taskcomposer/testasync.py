from cchelper import *
import collections
import contextlib
from concurrent.futures import Future
import aiofiles
import collections.abc


class CcException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg


@dataclasses.dataclass
class Node:
    io: io.IOBase
    desc: str

    def close(self):
        self.io.close()

    def __hash__(self) -> int:
        return hash(self.io.fileno())

    def __eq__(self, othr: object) -> bool:
        return type(othr) is Node and self.io.fileno() == othr.io.fileno()


lock = threading.Lock()


@dataclasses.dataclass
class Process:
    cmd: str | List[str]
    desc: str
    p: Popen = None

    def __post_init__(self):
        # with lock:  # TODO Make os.pipe thread-safe ???
        self.p = Popen(
            self.cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=type(self.cmd) is str,
        )

    @property
    def stdin(self):
        return Node(self.p.stdin, desc=f"{self.desc}/stdin")

    @property
    def stdout(self):
        return Node(self.p.stdout, desc=f"{self.desc}/stdout")

    @property
    def stderr(self):
        return Node(self.p.stderr, desc=f"{self.desc}/stderr")

    def poll(self):
        return self.p.poll()

    def terminate(self):
        self.p.terminate()

    @property
    def pid(self):
        return self.p.pid

    @property
    def returncode(self):
        return self.p.returncode


async def flow(
    s: Node,
    ts: List[Node],
    verdict: Verdict,
):
    t = None
    try:
        close_ts = s.desc in ("input", "generator/stdout") and "solver/stdin" in map(
            lambda t: t.desc, ts
        )
        async with contextlib.AsyncExitStack() as stack:
            r = await stack.enter_async_context(
                aiofiles.open(s.io.fileno(), "rb", closefd=F, buffering=0)
            )
            ws = [
                (
                    t,
                    await stack.enter_async_context(
                        aiofiles.open(t.io.fileno(), "ab", closefd=F, buffering=0)
                    ),
                )
                for t in ts
            ]
            while T:
                c = await r.read(conf.bytes_per_read)
                if not c:
                    break
                for t, w in ws:
                    await w.write(c)
                if close_ts:
                    verdict.flow_bytes += len(c)
    except ValueError as e:  # ValueError: I/O operation on closed file
        pass
    except BrokenPipeError:
        if verdict.status != VS.SKP:
            verdict.status = VS.RTE
            verdict.status_detail = f"[{s.desc} > {t.desc}] BROKEN PIPE"
    except BaseException as e:
        raise CcException(f"[{s.desc} > {t.desc if t else '*'}] ERROR")
    finally:
        try:
            if close_ts:
                for t in ts:
                    t.close()
        except BaseException as e:
            raise CcException(f"Node[{t.desc} close ERROR")


async def poll(
    proc: Process,
    verdict: Verdict,
):
    need_metric: bool = proc.desc in ("solver", "compile")
    tic = time.perf_counter()
    pp: psutil.Process = None
    try:
        while T:
            if global_stopflag.is_set():
                verdict.status = VS.SKP
                proc.terminate()
                return
            if need_metric:
                verdict.cpu = round((time.perf_counter() - tic) * 1000)
                try:
                    if pp is None:
                        pp = psutil.Process(proc.pid)
                    verdict.mem = round(pp.memory_info().rss / 1024 / 1024)
                except:
                    pass
            ret = proc.poll()
            if ret is not None:
                return
            await asyncio.sleep(0)
    except BaseException as e:
        raise CcException(f"Proc[{proc.desc}] ERROR")


async def main(tasks: List[collections.abc.Coroutine]):
    await asyncio.gather(*tasks)


last_built_debug: bool = None

def compile_one(
    verdict: Verdict,
    # stop_flag: threading.Event,
    file: File,
    build_asneed: bool,
):
    if global_stopflag.is_set():
        verdict.status = VS.COMPILATION_SKP
        return
    try:
        nodes: List[Node] = []
        procs: List[Process] = []
        tasks: List[collections.abc.Coroutine] = []
        verdict.status = VS.COMPILATION_RUN
        verdict.cmd = file.compile_cmd
        global last_built_debug
        if verdict.cmd:
            exe = file.executable
            if (
                not build_asneed
                or build_asneed
                and (
                    not os.path.exists(exe)
                    or os.path.getmtime(file.path) > os.path.getmtime(exe)
                )
                or last_built_debug != conf.build_debug
            ):
                last_built_debug = conf.build_debug
                cmd = verdict.cmd
                pcompile = Process(cmd, "compile")
                vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                nodes += [vstderr]
                procs += [pcompile]
                tasks.append(flow(pcompile.stderr, [vstderr], verdict))
                tasks.append(poll(pcompile, verdict))
                asyncio.run(main(tasks))
                # asyncio.run_coroutine_threadsafe(main(tasks), global_asyncloop).result()
                if pcompile.returncode:
                    verdict.status = VS.COMPILATION_ERR
                    verdict.status_detail = VS.COMPILATION_ERR.value
                else:
                    verdict.status = VS.COMPILATION_OK
                    verdict.status_detail = VS.COMPILATION_OK.value
                    # logger.info("Waiting exe to be dumped...")
                    # time.sleep(conf.exe_dump_delay)
                    # logger.info("Warming exe up...")
                    # pwarm = Process(file.execute_cmd, "warmup")
                    # time.sleep(conf.exe_warm_delay)
                    # pwarm.terminate()
            else:
                verdict.status = VS.COMPILATION_SKP
                verdict.status_detail = f"Executable is up-to-date"
        else:
            verdict.status = VS.COMPILATION_SKP
            verdict.status_detail = "No compilation cmd given"
    except BaseException as e:
        verdict.status = VS.COMPILATION_ERR
        verdict.status_detail = (
            e.msg if isinstance(e, CcException) else VS.COMPILATION_ERR.value
        )
        verdict.stderr += "".join(traceback.format_exception(e))
        global_stopflag.set()
    finally:
        for node in nodes:
            node.close()


def test_one(
    verdict: Verdict,
    solver: File,
    test: Test,
    cpu_upbound: int,
    mem_upbound: int,
    interactive: bool,
    qry_upbound: int,
    comp_type: CT,
) -> int:
    if global_stopflag.is_set():
        verdict.status = VS.SKP
        return
    try:
        verdict.status = VS.RUN
        verdict.status_detail = VS.RUN.value
        nodes: List[Node] = []
        edges: List[Tuple[Node, Node]] = []
        procs: List[Process] = []
        tasks: List[collections.abc.Coroutine] = []
        psolver = Process(
            solver.execute_cmd,
            desc="solver",
        )
        procs += [psolver]
        match test:
            # 1
            case Test(
                input_type=IT.MANUAL, answer_type=AT.MANUAL, input=input, answer=answer
            ):
                verdict.input = input
                verdict.answer = answer
                vinput = Node(open(verdict.input.path, "rb", buffering=0), "input")
                vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                nodes += [vinput, vactual, vstderr]
                edges += [
                    (vinput, psolver.stdin),
                    (psolver.stdout, vactual),
                    (psolver.stderr, vstderr),
                ]
            # 2
            case Test(
                input_type=IT.MANUAL, answer_type=AT.UNKNOWN, input=input, answer=answer
            ):
                verdict.input = input
                vinput = Node(open(verdict.input.path, "rb", buffering=0), "input")
                vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                nodes += [vinput, vactual, vstderr]
                edges += [
                    (vinput, psolver.stdin),
                    (psolver.stdout, vactual),
                    (psolver.stderr, vstderr),
                ]
            # 3
            case Test(
                input_type=IT.MANUAL, answer_type=AT.JURGER, input=input, answer=answer
            ):
                if not interactive:
                    verdict.input = input
                    vinput = Node(open(verdict.input.path, "rb", buffering=0), "input")
                    vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                    vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                    vanswer = Node(open(verdict.answer.path, "ab", buffering=0), "answer")
                    pjurger = Process(
                        answer.execute_cmd,
                        "jurger",
                    )
                    procs += [pjurger]
                    nodes += [vinput, vactual, vanswer, vstderr]
                    edges += [
                        (vinput, psolver.stdin),
                        (vinput, pjurger.stdin),
                        (psolver.stdout, vactual),
                        (pjurger.stdout, vanswer),
                        (psolver.stderr, vstderr),
                        (pjurger.stderr, vstderr),
                    ]
                else:
                    verdict.input = input
                    vinput = Node(open(verdict.input.path, "rb", buffering=0), "input")
                    vchat = Node(open(verdict.chat.path, "ab", buffering=0), "chat")
                    vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                    pjurger = Process(
                        answer.execute_cmd,
                        "jurger",
                    )
                    procs += [pjurger]
                    nodes += [vinput, vchat, vstderr]
                    edges += [
                        (vinput, pjurger.stdin),
                        (pjurger.stdout, psolver.stdin),
                        (pjurger.stdout, vchat),
                        (psolver.stdout, pjurger.stdin),
                        (psolver.stdout, vchat),
                        (psolver.stderr, vstderr),
                        (pjurger.stderr, vstderr),
                    ]
            # 5
            case Test(
                input_type=IT.GENERATOR,
                answer_type=AT.UNKNOWN,
                input=input,
                answer=answer,
            ):
                vinput = Node(open(verdict.input.path, "ab", buffering=0), "input")
                vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                pgenerator = Process(
                    input.execute_cmd,
                    desc="generator",
                )
                nodes += [vinput, vactual, vstderr]
                procs += [pgenerator]
                edges += [
                    (pgenerator.stdout, psolver.stdin),
                    (pgenerator.stdout, vinput),
                    (psolver.stdout, vactual),
                    (psolver.stderr, vstderr),
                    (pgenerator.stderr, vstderr),
                ]
            # 6
            case Test(
                input_type=IT.GENERATOR,
                answer_type=AT.MANUAL,
                input=input,
                answer=answer,
            ):
                verdict.answer = answer
                vinput = Node(open(verdict.input.path, "ab", buffering=0), "input")
                vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                pgenerator = Process(
                    input.execute_cmd,
                    desc="generator",
                )
                nodes += [vinput, vactual, vstderr]
                procs += [pgenerator]
                edges += [
                    (
                        pgenerator.stdout,
                        psolver.stdin,
                    ),
                    (pgenerator.stdout, vinput),
                    (psolver.stdout, vactual),
                    (psolver.stderr, vstderr),
                    (pgenerator.stderr, vstderr),
                ]
            # 7
            case Test(
                input_type=IT.GENERATOR,
                answer_type=AT.JURGER,
                input=input,
                answer=answer,
            ):
                if not interactive:
                    vinput = Node(open(verdict.input.path, "ab", buffering=0), "input")
                    vactual = Node(open(verdict.actual.path, "ab", buffering=0), "actual")
                    vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                    vanswer = Node(open(verdict.answer.path, "ab", buffering=0), "answer")
                    pgenerator = Process(
                        input.execute_cmd,
                        desc="generator",
                    )
                    pjurger = Process(
                        answer.execute_cmd,
                        desc="jurger",
                    )
                    nodes += [vinput, vactual, vanswer, vstderr]
                    procs += [pjurger, pgenerator]
                    edges += [
                        (pgenerator.stdout, psolver.stdin),
                        (pgenerator.stdout, pjurger.stdin),
                        (pgenerator.stdout, vinput),
                        (psolver.stdout, vactual),
                        (pjurger.stdout, vanswer),
                        (psolver.stderr, vstderr),
                        (pgenerator.stderr, vstderr),
                        (pjurger.stderr, vstderr),
                    ]
                else:
                # 8
                    vinput = Node(open(verdict.input.path, "ab", buffering=0), "input")
                    vstderr = Node(open(verdict.stderr.path, "ab", buffering=0), "stderr")
                    vchat = Node(open(verdict.chat.path, "ab", buffering=0), "chat")
                    pgenerator = Process(
                        input.execute_cmd,
                        desc="generator",
                    )
                    pjurger = Process(
                        answer.execute_cmd,
                        desc="jurger",
                    )
                    nodes += [vinput, vchat, vstderr]
                    procs += [pjurger, pgenerator]
                    edges += [
                        (pgenerator.stdout, pjurger.stdin),
                        (pgenerator.stdout, vinput),
                        (pjurger.stdout, psolver.stdin),
                        (pjurger.stdout, vchat),
                        (psolver.stdout, pjurger.stdin),
                        (psolver.stdout, vchat),
                        (psolver.stderr, vstderr),
                        (pjurger.stderr, vstderr),
                        (pgenerator.stderr, vstderr),
                    ]

        adjs = collections.defaultdict(lambda: set())
        for s, t in edges:
            adjs[s].add(t)
        for s, ts in adjs.items():
            tasks.append(flow(s, list(ts), verdict))
        for proc in procs:
            tasks.append(poll(proc, verdict))
        asyncio.run(main(tasks))
        # asyncio.run_coroutine_threadsafe(main(tasks), global_asyncloop).result() #TODO
        if verdict.status != VS.RUN:  # SKP or RTE
            return
        # TODO check generator/jurger returncode to assign status to RTE !!!!!!!

        match test.answer_type:
            case AT.UNKNOWN:
                for proc in procs:
                    if proc.returncode:
                        verdict.status = VS.RTE
                        verdict.status_detail = (
                            f"Proc[{proc.desc}] exited with code {proc.returncode}"
                        )
                        return
                if verdict.mem > mem_upbound:
                    verdict.status = VS.OOM
                    verdict.status_detail = (
                        f"{VS.OOM.value}: {verdict.mem} > {mem_upbound}"
                    )
                elif verdict.cpu > cpu_upbound:
                    verdict.status = VS.TLE
                    verdict.status_detail = (
                        f"{VS.TLE.value}: {verdict.cpu} > {cpu_upbound}"
                    )
                else:
                    verdict.status = VS.NA
                    verdict.status_detail = VS.NA.value
            case AT.MANUAL | AT.JURGER:
                for proc in procs:
                    if proc.returncode:
                        verdict.status = VS.RTE
                        verdict.status_detail = (
                            f"Proc[{proc.desc}] exited with code {proc.returncode}"
                        )
                        return
                if comp_type == CT.TBT:
                    verdict.actual = TokenFile(verdict.actual)
                    verdict.answer = TokenFile(verdict.answer)
                if verdict.actual != verdict.answer:
                    verdict.status = VS.WA
                    verdict.status_detail = VS.WA.value
                elif verdict.mem > mem_upbound:
                    verdict.status = VS.OOM
                    verdict.status_detail = (
                        f"{VS.OOM.value}: {verdict.mem} > {mem_upbound}"
                    )
                elif verdict.cpu > cpu_upbound:
                    verdict.status = VS.TLE
                    verdict.status_detail = (
                        f"{VS.TLE.value}: {verdict.cpu} > {cpu_upbound}"
                    )
                else:
                    verdict.status = VS.AC
                    verdict.status_detail = VS.AC.value
            case AT.INTERACTIVE_JURGER:
                rsolver = psolver.returncode
                rjurger = pjurger.returncode
                if rsolver:
                    verdict.status = VS.RTE
                    verdict.status_detail = """A solution finishing with exit code other than 0 (without exceeding time or memory limits) would be interpreted as a Runtime Error in the system."""
                elif rjurger:
                    verdict.status = VS.WA
                    verdict.status_detail = """A solution finishing with exit code 0 (without exceeding time or memory limits) and a judge finishing with exit code other than 0 would be interpreted as a Wrong Answer in the system."""
                else:
                    for proc in procs:
                        if proc.returncode:
                            verdict.status = VS.RTE
                            verdict.status_detail = (
                                f"Proc[{proc.desc}] exited with code {proc.returncode}"
                            )
                            return
                    qrys = sum((1 for _ in open(verdict.chat.path))) // 2
                    if qrys > qry_upbound:
                        verdict.status = VS.QLE
                        verdict.status_detail = (
                            f"{VS.QLE.value}: {qrys} > {qry_upbound}"
                        )
                    elif verdict.mem > mem_upbound:
                        verdict.status = VS.OOM
                        verdict.status_detail = (
                            f"{VS.OOM.value}: {verdict.mem} > {mem_upbound}"
                        )
                    elif verdict.cpu > cpu_upbound:
                        verdict.status = VS.TLE
                        verdict.status_detail = (
                            f"{VS.TLE.value}: {verdict.cpu} > {cpu_upbound}"
                        )
                    else:
                        verdict.status = VS.AC
                        verdict.status_detail = VS.AC.value
    except BaseException as e:
        verdict.status = VS.RTE
        verdict.status_detail = e.msg if isinstance(e, CcException) else VS.RTE.value
        verdict.stderr += "".join(traceback.format_exception(e))
        global_stopflag.set()
    finally:
        for node in nodes:
            node.close()
    return
