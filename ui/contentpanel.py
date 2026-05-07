from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QLabel,
    QSizePolicy,
    QFrame,
)
from PyQt5.QtGui import QPen, QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt

DARK_BG = "#121212"
GRID_COL = QColor("#1a1a1a")
AXIS_COL = QColor("#252525")
SCENE_HALF = 5000


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self._pixmap_item = None

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor(DARK_BG))
        self.setStyleSheet("border: 1px solid #242424; border-radius: 6px;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        S = SCENE_HALF
        self._scene.setSceneRect(-S, -S, S * 2, S * 2)
        self._draw_grid()
        self._draw_axes()

    def _draw_grid(self):
        pen = QPen(GRID_COL)
        pen.setWidth(1)
        S, step = SCENE_HALF, 50
        for x in range(-S, S + 1, step):
            self._scene.addLine(x, -S, x, S, pen)
        for y in range(-S, S + 1, step):
            self._scene.addLine(-S, y, S, y, pen)

    def _draw_axes(self):
        pen = QPen(AXIS_COL)
        pen.setWidth(2)
        S = SCENE_HALF
        self._scene.addLine(-S, 0, S, 0, pen)
        self._scene.addLine(0, -S, 0, S, pen)

    def set_image(self, pixmap: QPixmap):
        if self._pixmap_item:
            self._scene.removeItem(self._pixmap_item)
        self._pixmap_item = QGraphicsPixmapItem(pixmap)
        self._pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        w, h = pixmap.width(), pixmap.height()
        self._pixmap_item.setPos(-w / 2, -h / 2)
        self._scene.addItem(self._pixmap_item)
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def clear_image(self):
        if self._pixmap_item:
            self._scene.removeItem(self._pixmap_item)
            self._pixmap_item = None

    def has_image(self) -> bool:
        return self._pixmap_item is not None

    def wheelEvent(self, event):
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)

    def zoom_in(self):
        self.scale(1.2, 1.2)

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)

    def reset_zoom(self):
        self.resetTransform()
        if self._pixmap_item:
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)


def _toolbar_btn(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setFixedHeight(30)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #1e1e1e;
            color: #cccccc;
            border: 1px solid #2e2e2e;
            border-radius: 4px;
            padding: 0 12px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #2a2a2a;
            color: #ffffff;
            border-color: #3a3a3a;
        }
        QPushButton:pressed {
            background-color: #333333;
        }
    """)
    return btn


class ContentPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {DARK_BG};")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 16)
        root.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self._upload_btn = _toolbar_btn("Upload Image")
        self._remove_btn = _toolbar_btn("Remove")
        self._reset_btn = _toolbar_btn("Reset View")
        self._zoom_in = _toolbar_btn("+")
        self._zoom_out = _toolbar_btn("-")

        self._zoom_in.setFixedWidth(32)
        self._zoom_out.setFixedWidth(32)

        def _vline():
            f = QFrame()
            f.setFrameShape(QFrame.VLine)
            f.setFixedWidth(1)
            f.setStyleSheet("background-color: #2a2a2a; border: none;")
            return f

        toolbar.addWidget(self._upload_btn)
        toolbar.addWidget(self._remove_btn)
        toolbar.addWidget(_vline())
        toolbar.addWidget(self._zoom_out)
        toolbar.addWidget(self._zoom_in)
        toolbar.addWidget(self._reset_btn)
        toolbar.addStretch()

        self._status = QLabel("No image loaded")
        self._status.setStyleSheet(
            "color: #444444; font-size: 11px; "
            "background: #1a1a1a; border: 1px solid #252525; "
            "border-radius: 3px; padding: 2px 10px;"
        )
        toolbar.addWidget(self._status)

        root.addLayout(toolbar)

        self.viewer = ImageViewer()
        root.addWidget(self.viewer, stretch=1)

        self._result_bar = QLabel("")
        self._result_bar.setWordWrap(True)
        self._result_bar.setStyleSheet(
            "color: #888888; font-size: 11px; "
            "background: #181818; border-top: 1px solid #222222; "
            "padding: 5px 8px; border-radius: 3px;"
        )
        self._result_bar.hide()
        root.addWidget(self._result_bar)

        self._upload_btn.clicked.connect(self._upload)
        self._remove_btn.clicked.connect(self._remove)
        self._reset_btn.clicked.connect(self.viewer.reset_zoom)
        self._zoom_in.clicked.connect(self.viewer.zoom_in)
        self._zoom_out.clicked.connect(self.viewer.zoom_out)

    def _upload(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if path:
            px = QPixmap(path)
            if not px.isNull():
                self.viewer.set_image(px)
                name = path.replace("\\", "/").split("/")[-1]
                self._set_status(name, "#5dba80")
                self._result_bar.hide()

    def _remove(self):
        self.viewer.clear_image()
        self._set_status("No image loaded", "#444444")
        self._result_bar.hide()

    def _set_status(self, text: str, colour: str = "#444444"):
        self._status.setText(text)
        self._status.setStyleSheet(
            f"color: {colour}; font-size: 11px; "
            f"background: #1a1a1a; border: 1px solid #252525; "
            f"border-radius: 3px; padding: 2px 10px;"
        )

    def show_result(self, analysis: str, text: str):
        self._result_bar.setText(f"[{analysis}]   {text}")
        self._result_bar.show()
