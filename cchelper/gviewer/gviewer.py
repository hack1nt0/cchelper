from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget
from cchelper import *
from .gwidget_ui import Ui_GWidget
from PySide6.QtSvgWidgets import QSvgWidget, QGraphicsSvgItem
from .model import GModel
import tempfile
from cchelper.fileeditor import CodeEditorD


@dataclasses.dataclass
class GItem:
    props: Dict[str, Any]
    items: List[QGraphicsItem]


PAD = 4  # https://stackoverflow.com/questions/76349251/converting-between-pixels-and-graphviz-sizes-coordinates
LABEL_ITEM_BRUSH = QBrush(QColor(255, 255, 0))
LABEL_ITEM_PEN = QPen(BLACK)
# ITEM_BRUSH = QBrush(BLUE, Qt.BrushStyle.DiagCrossPattern)
ITEM_BRUSH = QBrush(QColor(0, 0, 255))
ITEM_PEN = Qt.PenStyle.NoPen


def parse_node(dats: List[Dict], H: int) -> QAbstractGraphicsShapeItem:
    ret = None
    for dat in dats:
        match dat["op"]:
            case "e":
                x, y, w, h = dat["rect"]
                x = x - w + PAD
                y = H - (y + h) + PAD
                w *= 2
                h *= 2
                ret = QGraphicsEllipseItem(x, y, w, h)
            case "b":
                pass
    if ret:
        ret.setBrush(ITEM_BRUSH)
        ret.setPen(ITEM_PEN)
    return ret


def parse_edge(dats: List[Dict], H: int) -> QAbstractGraphicsShapeItem:
    pass


import math


def parse_text(dats: List[Dict[str, Any]], H: int) -> List[QAbstractGraphicsShapeItem]:
    rets = []
    texts = []
    fontH = math.inf
    minX = math.inf
    maxW = 0
    minY, maxY = math.inf, 0
    lines = 0
    for dat in dats:
        match dat["op"]:
            case "F":
                fontH = dat["size"]
            case "T":
                texts.append(dat["text"])
                x, y = dat["pt"]
                width = dat["width"]
                # match dat['align']:
                #     case 'l':
                #         pass
                #     case 'c':
                #         x -= width / 2
                #     case 'r':
                #         x -= width
                minX = min(minX, x)
                minY = min(minY, y)
                maxY = max(maxY, y + fontH)
                lines += 1
                maxW = max(maxW, width)
    # size = size * 4 / 3
    x = minX + PAD
    # y = H - (y + size / 2) + PAD #TODO
    y = H - maxY + PAD
    w = maxW + PAD
    h = maxY - minY + PAD

    ret_text = QGraphicsTextItem("\n".join(texts))
    ret_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    ret_text.moveBy(x, y)

    w = ret_text.boundingRect().width()
    h = ret_text.boundingRect().height()
    ret_bb = QGraphicsRectItem(x, y, w, h)
    ret_bb.setBrush(LABEL_ITEM_BRUSH)
    ret_bb.setPen(LABEL_ITEM_PEN)

    rets.append(ret_bb)
    rets.append(ret_text)
    return rets


def parse_props(dat: Dict[str, Any]):
    ret = {}
    PREFIX = "cchelper_"
    for k, v in dat.items():
        if k.startswith(PREFIX):
            k = k[len(PREFIX) :]
            ret[k] = v
    return ret


def parse_gitems(dat: Dict) -> List[GItem]:
    _, _, _, H = map(float, dat["bb"].split(","))
    # H += PAD * 2
    rets = []
    nodes, edges = 0, 0
    for o in dat.get("objects", []):
        if "_draw_" not in o:
            continue
        ret = GItem({}, [])
        ret.props["name"] = o["name"]
        ret.props.update(parse_props(o))
        ret.items.append(parse_node(o["_draw_"], H))
        if "_ldraw_" in o:
            ret.items.extend(parse_text(o["_ldraw_"], H))
        rets.append(ret)
        nodes += 1
    for o in dat.get("edges", []):
        if "_draw_" not in o:
            continue
        ret = GItem({}, [])
        ret.props.update(parse_props(o))
        # ret.items.append(parse_node(o["_draw_"], H))
        if "_ldraw_" in o:
            ret.items.extend(parse_text(o["_ldraw_"], H))
        rets.append(ret)
        edges += 1
    return nodes, edges, rets


class GViewer(QDialog, Ui_GWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Tool)

        self.c_menu = QMenu(self)
        self.c_menu.addAction("Auto Fit", self.fit_scene_to_view)
        self.c_menu.addAction("Reset Scale", self.reset_scale)
        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(
            lambda p: self.c_menu.popup(QCursor().pos())
        )
        self.l_menu = QMenu(self)
        # self.LMenu = QMenu(self)
        self.l_group = QActionGroup(self)
        for L in [
            "dot",
            "neato",
            "fdp",
            "sfdp",
            "circo",
            "twopi",
        ]:
            act: QAction = self.l_group.addAction(
                self.l_menu.addAction(L, self.refresh)
            )
            act.setCheckable(T)
            if L == "dot":
                act.setChecked(T)
        self.LButton.setMenu(self.l_menu)
        self.LButton.setShortcut("Ctrl+L")

        self.findWidget.setVisible(F)
        self.FButton.clicked.connect(self.enter_filter)
        self.FButton.setShortcut("Ctrl+F")
        self.CFButton.clicked.connect(self.exit_filter)
        self.CFButton.setShortcut("Esc")
        self.lineEdit.returnPressed.connect(self.filter)
        self.saveButton.clicked.connect(self.save_png)
        self.editButton.clicked.connect(self.edit_dot)

        self.spinBox.valueChanged.connect(self.refresh)
        self.spinBox.setRange(1, 1)

        self.gitems: List[GItem] = []

        self.DEFAULT_COLOR = f"""
    bgcolor="#000080";
	node [color=white fontcolor=white];
	edge [color=white];
"""

        self.source = File(paths.graph("1.dot")).create()
        if not os.path.exists(self.source.path):
            with open(self.source.path, 'w') as w:
                w.write("digraph {}")
        self.refresh()

    @property
    def L(self):
        return [
            action.text() for action in self.l_menu.actions() if action.isChecked()
        ][0]

    def set_file(self, source: str):
        self.show()  # TODO
        self.source = source if isinstance(source, File) else File(source)
        dots = []
        buf = []
        with open(self.source.path) as r:
            state = 0
            for line in r:
                match state:
                    case 0:
                        if line.startswith("digraph {") or line.startswith("graph {"):
                            state = 1
                            buf.append(line)
                            buf.append(self.DEFAULT_COLOR)
                    case 1:
                        buf.append(line)
                        if line.strip() == "}":
                            state = 0
                            dots.append("".join(buf))
                            buf.clear()
        if dots:
            for idx, dot in enumerate(dots, start=1):
                with open(
                    os.path.join(os.path.dirname(self.source.path), f"{idx}.dot"), "w"
                ) as w:
                    w.write(dot)
        else:
            with open(
                os.path.join(os.path.dirname(self.source.path), f"1.dot"), "w"
            ) as w:
                w.write(f"digraph {{{self.DEFAULT_COLOR}}}")
        self.spinBox.blockSignals(T)
        ptot = max(1, len(dots))
        self.spinBox.setRange(1, ptot)
        self.spinBox.setValue(1)
        self.spinBox.setSuffix(f"/{ptot} pages")
        self.spinBox.blockSignals(F)
        self.refresh()

    def refresh(self):
        dot_path = conf.graphviz
        if not dot_path:
            logger.error("Dot not in PATH")
            return
        self.source = File(
            os.path.join(
                os.path.dirname(self.source.path), f"{self.spinBox.value()}.dot"
            )
        )
        target = os.path.splitext(self.source.path)[0] + ".json"
        try:
            # gv.render(
            #     engine=self.L, filepath=self.source, format="json", outfile=target
            # )
            subprocess.run(
                f"{dot_path} -Tjson -K{self.L} -o {target} {self.source.path}",
                shell=T,
                stderr=PIPE,
                check=T,
            )
        except BaseException as e:
            logger.error("Dot syntax ERROR")
            logger.exception(e)
            return

        # self.gitems.clear()
        with open(target) as r:
            dat = json.load(r)
        try:
            self.nodes, self.edges, self.gitems = parse_gitems(dat)
        except BaseException as e:
            logger.error("Dot extract ERROR")
            logger.exception(e)

        target = os.path.splitext(self.source.path)[0] + ".svg"
        subprocess.run(
            f"{dot_path} -Tsvg -K{self.L} -o {target} {self.source.path}",
            shell=T,
            stderr=PIPE,
            check=T,
        )
        # gv.render(engine=self.L, filepath=self.source, format="svg", outfile=target)
        self.svg_item = QGraphicsSvgItem(target)

        self.view.setItem(self.svg_item)
        # self.view.setSceneRect(*map(float, dat["bb"].split(",")))
        self.view.setSceneRect(self.svg_item.boundingRect())

        self.label.setText(f"{self.nodes}/{self.edges}")

    def clear_found(self):
        for e in self.view.items():
            if e != self.svg_item:
                self.view.delItem(e)

    def filter(self):
        self.clear_found()
        Q = self.lineEdit.text()
        M = 0
        for gitem in self.gitems:
            ok = False
            try:
                ok = eval(Q, gitem.props)
            except BaseException as e:
                # logger.exception(e)
                pass
            if ok:
                M += 1
                for item in gitem.items:
                    self.view.addItem(item)
        logger.info(f"Found {M} items")

    def enter_filter(self):
        self.findWidget.setVisible(T)
        self.lineEdit.setFocus()

    def exit_filter(self):
        self.clear_found()
        self.findWidget.setVisible(F)

    def fit_scene_to_view(self):
        sw, wh = self.view.sceneRect().width(), self.view.sceneRect().height()
        vw, vh = self.view.width(), self.view.height()
        scaleFactor = min(vw / sw, vh / wh)
        self.view.resetTransform()
        self.view.scale(scaleFactor, scaleFactor)

    def reset_scale(self):
        self.view.resetTransform()
        # self.view.setTransform(QTransform(1, 0, 0, 1, 0, 0), combine=False)

    def save_png(self):
        image = QImage(
            self.svg_item.boundingRect().size().toSize(), QImage.Format.Format_ARGB32
        )
        painter = QPainter(image)
        self.svg_item.renderer().render(painter)
        painter.end()
        self.png_fn, _ = QFileDialog.getSaveFileName(
            self,
            caption="Saved As png",
            dir=os.getcwd(),
            filter="*.png",
            selectedFilter="*.png",
        )
        image.save(self.png_fn)
        logger.info(f"Saved as {self.png_fn}")

    def edit_dot(self):
        d = CodeEditorD(self)
        d.set_file(self.source)
        d.saved_signal.connect(self.refresh)
        d.exec()
