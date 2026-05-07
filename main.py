import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon
from ui.menu import MenuBarBuilder
from ui.sidebar import Sidebar
from ui.contentpanel import ContentPanel
import os


class WindowConfig:
    TITLE = "PyroX"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGO = os.path.join(BASE_DIR, "pyrox_logo.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WindowConfig.TITLE)
        self.setWindowIcon(QIcon(WindowConfig.LOGO))
        self.setStyleSheet("background-color:#141313;")
        self.setMinimumSize(900, 600)
        self.resize(1280, 800)
        self._build_menu()
        self._build_ui()

    def _build_menu(self):
        MenuBarBuilder(self).build()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()

        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background-color: #1e1e1e;")

        self.content = ContentPanel()

        layout.addWidget(self.sidebar)
        layout.addWidget(sep)
        layout.addWidget(self.content)
        layout.setStretch(2, 1)

        self.sidebar.analysis_requested.connect(self._on_analysis)

    def _on_analysis(self, name: str):
        if not self.content.viewer.has_image():
            self.content.show_result(name, "Please upload an image first.")
            return
        self.content.show_result(name, f"Running '{name}'...")


if __name__ == "__main__":
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "pyrox.app.v1"
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("pyrox_logo.png"))

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
