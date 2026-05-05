from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QHBoxLayout, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem
)

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.pixmap_item = None
        self.scale_factor = 1.0


        self.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )

        # Enable drag (pan)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # Hide scrollbars (Desmos style)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("border: 2px dashed #444;")

        # Set large scene space (acts like infinite plane)
        self.scene.setSceneRect(-1000, -1000, 2000, 2000)

        self.draw_axes()
        self.draw_grid()

    # --------------------------
    # Set Image
    # --------------------------
    def set_image(self, pixmap):
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)

        self.pixmap_item = QGraphicsPixmapItem(pixmap)

        # Center image at (0,0)
        w = pixmap.width()
        h = pixmap.height()
        self.pixmap_item.setPos(-w / 2, -h / 2)

        self.scene.addItem(self.pixmap_item)

    # --------------------------
    # Clear Image
    # --------------------------
    def clear_image(self):
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)
            self.pixmap_item = None

    # --------------------------
    # Zoom (mouse wheel)
    # --------------------------
    def wheelEvent(self, event):
        zoom_in = 1.2
        zoom_out = 1 / zoom_in

        factor = zoom_in if event.angleDelta().y() > 0 else zoom_out

        self.scale(factor, factor)

    # --------------------------
    # Draw Axes (Desmos style)
    # --------------------------
    def draw_axes(self):
        pen = QPen(Qt.white)
        pen.setWidth(2)

        # X-axis
        self.scene.addLine(-1000, 0, 1000, 0, pen)

        # Y-axis
        self.scene.addLine(0, -1000, 0, 1000, pen)

    # --------------------------
    # Draw Grid (optional)
    # --------------------------
    def draw_grid(self):
        pen = QPen(Qt.gray)
        pen.setWidth(1)

        step = 50

        for x in range(-1000, 1000, step):
            self.scene.addLine(x, -1000, x, 1000, pen)

        for y in range(-1000, 1000, step):
            self.scene.addLine(-1000, y, 1000, y, pen)

class ContentPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color:#141313;")

        main_layout = QVBoxLayout(self)

        # 🔹 Top bar
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.upload_btn = QPushButton("Upload Image (*.png *.jpg *.jpeg *.bmp)")
        self.remove_btn = QPushButton("Remove")
        self.zoom_in_btn = QPushButton("+")
        self.zoom_out_btn = QPushButton("-")

        for btn in [self.upload_btn, self.remove_btn, self.zoom_in_btn, self.zoom_out_btn]:
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: white;
                    border-radius: 6px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)

        top_bar.addWidget(self.upload_btn)
        top_bar.addWidget(self.remove_btn)
        top_bar.addWidget(self.zoom_in_btn)
        top_bar.addWidget(self.zoom_out_btn)

        # 🔹 Image viewer
        self.viewer = ImageViewer()
        self.viewer.setFixedSize(700, 450)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.viewer)
        center_layout.addStretch()

        main_layout.addLayout(top_bar)
        main_layout.addSpacing(15)
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        # 🔥 Connections
        self.upload_btn.clicked.connect(self.upload_image)
        self.remove_btn.clicked.connect(self.viewer.clear_image)
        self.zoom_in_btn.clicked.connect(lambda: self.viewer.scale(1.2, 1.2))
        self.zoom_out_btn.clicked.connect(lambda: self.viewer.scale(0.8, 0.8))

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            pixmap = QPixmap(file_path)
            self.viewer.set_image(pixmap)
