import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon
from ui.menu import MenuBarBuilder
from ui.sidebar import Sidebar
from ui.contentpanel import ContentPanel


class WindowConfig:
    TITLE = "PyroX"
    LOGO = "pyrox_logo.png"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WindowConfig.TITLE)
        self.setWindowIcon(QIcon(WindowConfig.LOGO))
        self.setStyleSheet("background-color:#141313;")
        self.showMaximized()

        self.initMenu()
        self.initUI()

    def initMenu(self):
        MenuBarBuilder(self).build()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 🔹 Sidebar
        self.sidebar = Sidebar()

        # 🔹 Vertical separator
        separator = QFrame()
        separator.setFixedWidth(2)
        separator.setStyleSheet("background-color: #3a3a3a;")

        # 🔹 Content panel
        self.content = ContentPanel()

        # 🔹 Add widgets
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.content)

        # 🔹 Stretch behavior
        main_layout.setStretch(0, 0)  # sidebar
        main_layout.setStretch(1, 0)  # separator
        main_layout.setStretch(2, 1)  # content


if __name__ == "__main__":
    import ctypes

    myappid = "pyrox.app.v1"  # any unique string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("pyrox_logo.png"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
