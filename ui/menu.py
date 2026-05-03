from PyQt5.QtWidgets import QAction

class MenuBarBuilder:
    def __init__(self, window):
        self.window = window

    def build(self):
        menubar = self.window.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1e1e1e;
                color: white;
            }

            QMenuBar::item:selected {
                background: #333;
            }

            QMenu {
                background-color: #1e1e1e;
                color: white;
            }

            QMenu::separator {
                height: 1px;
                background: white;
                margin: 5px 10px;
            }
        """)

        # File Menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self.window)
        open_action = QAction("Open", self.window)
        save_action = QAction("Save", self.window)
        saveas_action = QAction("Save As", self.window)
        exit_action = QAction("Exit", self.window)

        exit_action.triggered.connect(self.window.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(saveas_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")

        copy_action = QAction("Copy", self.window)
        paste_action = QAction("Paste", self.window)

        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")

        help_action = QAction("Help",self.window)
        about_action = QAction("About", self.window)

        help_menu.addAction(help_action)
        help_menu.addAction(about_action)
