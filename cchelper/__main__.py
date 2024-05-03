from PySide6.QtCore import QEvent, QObject
from cchelper import *
from cchelper.taskcomposer import TaskComposerM
from cchelper.settings import Settings


class App(QApplication):
    def notify(self, obj: QObject, e: QEvent) -> bool:
        if (
            e.type() == QEvent.Type.KeyPress
            and e.key() == Qt.Key.Key_Tab
            and obj == windows["terminal"]
        ):
            obj.keyPressEvent(e)
            return T
        try:
            return super().notify(obj, e)
        except:
            pass
        finally:
            return F

if __name__ == "__main__":
    app = App()

    windows['app'] = app

    print('STYLE'.center(100, '-'), '\n', app.styleSheet())

    c = TaskComposerM()
    app.paletteChanged.connect(c.set_color) #TODO
    c.show()
    c.settings()

    # b.setting()
    # os.chdir(conf.project_dir) #TODO
    # b.refresh_tasks()
    # b.start_listener()

    # def run_event_loop(loop: asyncio.AbstractEventLoop):
    #     logger.debug("""Run asyncio event loop in daemon thread""")
    #     loop.run_forever()

    # thread = Thread(target=run_event_loop, args=(global_asyncloop,))
    # thread.daemon = True
    # thread.start()

    returncode = app.exec()
    sys.exit(returncode)
