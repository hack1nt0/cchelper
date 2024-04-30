import json
from cchelper import *
from cchelper.taskcrawler import TaskCrawler


class CcListener(BaseHTTPRequestHandler, QObject):

    def do_POST(self):
        dat = self.rfile.read(int(self.headers["content-length"]))
        dat = json.loads(dat)
        task = Task()

        def name(group: str, name: str) -> str:
            def alnum(s):
                return "".join(filter(lambda c: c.isalnum(), s.title()))
            judge = group
            contest = ''
            if group.find('-') >= 0:
                p = group.find('-')
                judge = group[:p]
                contest = group[p+1:]
            return os.path.join(*map(alnum, (judge, contest, name)))

        task.name = name(dat['group'], dat['name'])
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

        windows["taskbrowser"].new_task_signal.emit(task)
