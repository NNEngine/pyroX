import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from menu import MenuBarBuilder
from sidebar import Sidebar


class WindowConfig:
    TITLE = "Fourth Window"
    LOGO = "logo.png"


class MainWindow(QMainWindow):
        def __init__(self):
                super().__init__()

                self.setWindowTitle(WindowConfig.TITLE)
                self.setWindowIcon(QIcon(WindowConfig.LOGO))
                self.setStyleSheet("background-color:#141313;")
                self.showMaximized()

                self.initMenu()
                self.initSidebar()

        def initMenu(self):
                MenuBarBuilder(self).build()

        def initSidebar(self):
                central = QWidget()
                self.setCentralWidget(central)

                main_layout = QHBoxLayout()

                # Plug in sidebar
                self.sidebar = Sidebar()

                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.setStyleSheet("background-color: #3a3a3a;")
                separator.setFixedWidth(2)

                # Content area
                self.content = QLabel("Main Content")
                self.content.setAlignment(Qt.AlignCenter)

                main_layout.addWidget(self.sidebar)
                main_layout.addWidget(separator)
                main_layout.addWidget(self.content)

                main_layout.setStretch(0, 1)
                main_layout.setStretch(1, 4)

                central.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
