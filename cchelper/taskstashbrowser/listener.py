import json
from cchelper import *
from cchelper.taskcrawler import TaskCrawler


class CcListener(BaseHTTPRequestHandler, QObject):

    def do_POST(self):
        dat = self.rfile.read(int(self.headers["content-length"]))
        dat = json.loads(dat)
        task = Task()

        # TODO shrink
        def group(s):
            ph = s.find(" - ")
            if ph >= 0:
                l, r = s[:ph], s[ph + 3 :]
                if r.startswith(l):
                    ret = r
                else:
                    ret = " ".join((l, r))
            else:
                ret = s
            return "".join(filter(lambda c: c.isalnum(), ret.title()))

        def problem(s):
            return "".join(filter(lambda c: c.isalnum(), s.title()))

        task.name = f"{group(dat['group'])}-{problem(dat['name'])}"
        task.url = dat["url"]
        task.cpu = dat["timeLimit"]
        task.mem = dat["memoryLimit"]
        task.interactive = dat["interactive"]
        if not task.interactive:
            task.tests = []
            for idx, tst_raw in enumerate(dat["tests"]):
                tst = Test(
                    id=idx,
                    status=VS.QUE,
                    input_type=IT.MANUAL,
                    input=tst_raw["input"],
                    answer_type=AT.MANUAL,
                    answer=tst_raw["output"],
                )
                task.tests.append(tst)
        
        windows["TaskWindow"].add_task_signal.emit(task)
