from cchelper import *
import cchelper.taskcomposer.testasync as TestService


class BuildState(QState):
    ok_signal: Signal = Signal()
    nk_signal: Signal = Signal()
    skip_signal: Signal = Signal()

    def __init__(self, task: Task, views: List[QWidget], parent: QState = None) -> None:
        super().__init__(parent)
        self.task = task
        self.views = views
        self.entered.connect(self.start)
        self.futures: List[Future] = []

    def start(self):
        for view in self.views:
            view.start("Build")
        self.timer = QTimer(self)
        self.timer.setInterval(1000 // conf.refresh_rate)
        self.timer.timeout.connect(self.refresh)
        self.threadpool = ThreadPoolExecutor(max_workers=conf.parallel)

        self.task.verdicts.clear()
        if os.path.exists(self.task.verdict_dir()):
            shutil.rmtree(self.task.verdict_dir())
        # self.stop_flag = threading.Event()
        global_stopflag.clear()

        def files():
            self.task.solver.taskname = self.task.name
            yield self.task.solver
            for test in self.task.tests:
                if test.input_type == IT.GENERATOR:
                    test.input.taskname = self.task.name
                    yield test.input
                if test.answer_type == AT.JURGER:
                    test.answer.taskname = self.task.name
                    yield test.answer

        for file in files():
            vid = len(self.task.verdicts)
            verdict = Verdict(
                id=vid,
                test_id=None,
                status=VS.COMPILATION_QUE,
                stderr=File(self.task.verdict_dir(vid, "stderr.txt")).create(),
            )
            self.task.verdicts.append(verdict)
            # if len(file) == 0:  # TODO file empty
            #     verdict.status = VS.COMPILATION_SKP
            #     continue
            task = self.threadpool.submit(
                TestService.compile_one,
                verdict=verdict,
                file=file,
                build_asneed=conf.build_asneed,
            )
            self.futures.append(task)
        for view in self.views:
            view.set_task(self.task)
        self.timer.start()

    def refresh(self):
        self.timer.stop()  # TODO
        if all(future.done() for future in self.futures):
            if self.task.verdicts[0].status == VS.COMPILATION_SKP:
                self.stop()
                self.skip_signal.emit()
            elif all(self.task.verdicts):
                self.stop()
                self.ok_signal.emit()
            else:
                self.stop()
                self.nk_signal.emit()
            return
        for view in self.views:
            view.refresh()
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.futures.clear()
        self.threadpool.shutdown(wait=T, cancel_futures=T)
        for view in self.views:
            view.refresh() #TODO
            view.stop()


class DumpState(QState):
    ok_signal: Signal = Signal()

    def __init__(self, task: Task, views: List[QWidget], parent: QState = None) -> None:
        super().__init__(parent)
        self.task = task
        self.views = views
        self.entered.connect(self.start)
        self.timer = QTimer(self)
        self.timer.setInterval(1000 // conf.refresh_rate)
        self.timer.timeout.connect(self.refresh)
        self.timer2 = QTimer(self)
        self.timer2.setInterval(conf.exe_dump_delay * 1000)
        self.timer2.timeout.connect(self.stop)

    def start(self):
        for view in self.views:
            view.start("Dump")
        self.timer.start()
        self.timer2.start()

    def refresh(self):
        for view in self.views:
            view.refresh()

    def stop(self):
        self.timer.stop()
        self.timer2.stop()
        for view in self.views:
            view.refresh()
            view.stop()
        self.ok_signal.emit()


class WarmState(QState):
    ok_signal: Signal = Signal()

    def __init__(self, task: Task, views: List[QWidget], parent: QState = None) -> None:
        super().__init__(parent)
        self.task = task
        self.views = views
        self.entered.connect(self.start)
        self.timer = QTimer(self)
        self.timer.setInterval(1000 // conf.refresh_rate)
        self.timer.timeout.connect(self.refresh)
        self.timer2 = QTimer(self)
        self.timer2.setInterval(conf.exe_warm_delay * 1000)
        self.timer2.timeout.connect(self.stop)

    def start(self):
        for view in self.views:
            view.start("Warm up")
        self.proc = TestService.Process(self.task.solver.execute_cmd, "warmup")
        self.timer.start()
        self.timer2.start()

    def refresh(self):
        for view in self.views:
            view.refresh()

    def stop(self):
        self.timer.stop()
        self.timer2.stop()
        self.proc.terminate()
        for view in self.views:
            view.refresh()
            view.stop()
        self.ok_signal.emit()


class RunState(QState):
    ok_signal: Signal = Signal()

    def __init__(self, task: Task, views: List[QWidget], parent: QState = None) -> None:
        super().__init__(parent)
        self.task = task
        self.views = views
        self.entered.connect(self.start)
        self.futures: List[Future] = []

    def start(self):
        for view in self.views:
            view.start("Run")
        self.timer = QTimer(self)
        self.timer.setInterval(1000 // conf.refresh_rate)
        self.timer.timeout.connect(self.refresh)
        self.threadpool = ThreadPoolExecutor(max_workers=conf.parallel)

        tests: List[Test] = []
        for old in filter(lambda test: test.checked, self.task.tests):
            if old.count > 0:
                tests += [old] * old.count
            else:
                tests.append(old)
        if tests:
            self.task.verdicts.clear()
            if os.path.exists(self.task.verdict_dir()):
                shutil.rmtree(self.task.verdict_dir())
        for test in tests:
            tid = test.id
            vid = len(self.task.verdicts)
            verdict = None  # TODO
            if self.task.interactive:
                verdict = Verdict(
                    id=vid,
                    test_id=tid,
                    status=VS.QUE,
                    input=File(self.task.verdict_dir(vid, "input.txt")).create(),
                    chat=File(self.task.verdict_dir(vid, "chat.txt")).create(),
                    stderr=File(self.task.verdict_dir(vid, "stderr.txt")).create(),
                )
            else:
                verdict = Verdict(
                    id=vid,
                    test_id=tid,
                    status=VS.QUE,
                    input=File(self.task.verdict_dir(vid, "input.txt")).create(),
                    answer=File(self.task.verdict_dir(vid, "answer.txt")).create(),
                    actual=File(self.task.verdict_dir(vid, "actual.txt")).create(),
                    stderr=File(self.task.verdict_dir(vid, "stderr.txt")).create(),
                )
            self.task.verdicts.append(verdict)
            task = self.threadpool.submit(
                TestService.test_one,
                verdict=verdict,
                solver=self.task.solver,
                test=test,
                cpu_upbound=self.task.cpu,
                mem_upbound=self.task.mem,
                interactive=self.task.interactive,
                qry_upbound=self.task.qry,
                comp_type=self.task.comp_type,
            )
            self.futures.append(task)
        for view in self.views:
            view.set_task(self.task)
        self.timer.start()

    def refresh(self):
        self.timer.stop()
        if all(future.done() for future in self.futures):
            self.stop()
            self.ok_signal.emit()
            return
        for view in self.views:
            view.refresh()
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.futures.clear()
        self.threadpool.shutdown(wait=T, cancel_futures=T)
        for view in self.views:
            view.refresh()
            view.stop()


def statemachine_of_build(task: Task, views: List[QWidget]) -> QStateMachine:
    machine = QStateMachine()
    B = BuildState(task, views)
    T = QFinalState()
    B.addTransition(B, SIGNAL("nk_signal()"), T)
    B.addTransition(B, SIGNAL("ok_signal()"), T)
    B.addTransition(B, SIGNAL("skip_signal()"), T)
    machine.addState(B)
    machine.addState(T)
    machine.setInitialState(B)
    return machine


def statemachine_of_run(task: Task, views: List[QWidget]) -> QStateMachine:
    machine = QStateMachine()
    B = BuildState(task, views)
    D = DumpState(task, views)
    W = WarmState(task, views)
    R = RunState(task, views)
    T = QFinalState()
    B.addTransition(B, SIGNAL("nk_signal()"), T)
    B.addTransition(B, SIGNAL("skip_signal()"), R)
    B.addTransition(B, SIGNAL("ok_signal()"), D)
    D.addTransition(D, SIGNAL("ok_signal()"), W)
    W.addTransition(W, SIGNAL("ok_signal()"), R)
    R.addTransition(R, SIGNAL("ok_signal()"), T)
    # B.addTransition(B, SIGNAL("ok_signal()"), R)
    # R.addTransition(R, SIGNAL("ok_signal()"), T)
    for state in [B, D, W, R, T]:
        machine.addState(state)
    machine.setInitialState(B)
    return machine
