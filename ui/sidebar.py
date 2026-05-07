from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QScrollArea,
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

ANALYSIS_GROUPS = {
    "FIRE & THERMAL": [
        "Fire Analysis",
        "Fire Segmentation",
        "Fire Localization",
        "Fire Intensity Estimation",
        "Fire Radiative Power Analysis",
        "Thermal Anomaly Detection",
        "Hotspot Detection",
    ],
    "SPATIAL": [
        "Fire Spread Mapping",
        "Fire Spread Extraction",
        "Spatial Extraction",
        "Heatmap Generation",
        "Region-wise Fire Density Analysis",
        "Distance from Infrastructure Analysis",
    ],
    "TEMPORAL": [
        "Fire Progression Tracking",
        "Time-Series Change Detection",
        "Burn Area Growth Rate Analysis",
        "Multi-temporal NDMI Analysis",
        "Seasonal Fire Trend Analysis",
    ],
    "ATMOSPHERIC & SMOKE": [
        "Smoke Detection",
        "Smoke Plume Segmentation",
        "Aerosol Optical Depth Analysis",
        "Air Quality Impact Estimation",
    ],
    "TERRAIN & ENVIRONMENT": [
        "Elevated Impact Analysis",
        "Slope & Aspect Analysis",
        "Wind Influence Analysis",
        "Temperature & Humidity Correlation",
        "Land Cover Classification",
    ],
}

GROUP_COLORS = {
    "FIRE & THERMAL": "#e05c2a",
    "SPATIAL": "#4a9eff",
    "TEMPORAL": "#4caf50",
    "ATMOSPHERIC & SMOKE": "#aaaaaa",
    "TERRAIN & ENVIRONMENT": "#8bc34a",
}


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About PyroX")
        self.setFixedSize(360, 200)
        self.setStyleSheet("background-color: #161616; color: #dddddd;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(8)

        title = QLabel("PyroX")
        title.setStyleSheet("color: #e05c2a; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        sub = QLabel("Wildfire Intelligence Platform")
        sub.setStyleSheet("color: #888888; font-size: 11px; letter-spacing: 1px;")
        layout.addWidget(sub)

        layout.addSpacing(10)

        desc = QLabel("Satellite-based wildfire analysis and monitoring suite.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        layout.addWidget(desc)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #2e2e2e;
                border-radius: 4px;
                padding: 4px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                color: #ffffff;
            }
        """)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class Sidebar(QWidget):
    analysis_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self._active_btn: QPushButton | None = None

        self.setStyleSheet("QWidget { background-color: #111111; color: #dddddd; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet(
            "background-color: #111111; border-bottom: 1px solid #222222;"
        )
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(14, 10, 14, 10)
        h_layout.setSpacing(2)

        title = QLabel("PyroX")
        title.setStyleSheet(
            "color: #e05c2a; font-size: 17px; font-weight: bold; background: transparent;"
        )
        sub = QLabel("Wildfire Intelligence")
        sub.setStyleSheet(
            "color: #555555; font-size: 10px; letter-spacing: 1px; background: transparent;"
        )
        h_layout.addWidget(title)
        h_layout.addWidget(sub)
        root.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #111111;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #111111;
            }
            QScrollBar:vertical {
                background-color: #111111;
                width: 6px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #444444;
                border-radius: 3px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: #111111;")

        inner = QVBoxLayout(container)
        inner.setContentsMargins(8, 8, 8, 12)
        inner.setSpacing(1)

        self.buttons: dict[str, QPushButton] = {}

        for group_name, tasks in ANALYSIS_GROUPS.items():
            grp_row = QWidget()
            grp_row.setStyleSheet("background-color: transparent;")
            grp_row_layout = QVBoxLayout(grp_row)
            grp_row_layout.setContentsMargins(6, 14, 6, 4)
            grp_row_layout.setSpacing(0)

            rule = QFrame()
            rule.setFixedHeight(2)
            rule.setStyleSheet(
                f"background-color: {GROUP_COLORS[group_name]}; border-radius: 1px;"
            )
            grp_row_layout.addWidget(rule)

            lbl = QLabel(group_name)
            lbl.setStyleSheet(
                f"color: {GROUP_COLORS[group_name]}; font-size: 9px; "
                f"font-weight: bold; letter-spacing: 1.5px; "
                f"padding-top: 5px; background: transparent;"
            )
            grp_row_layout.addWidget(lbl)
            inner.addWidget(grp_row)

            for task in tasks:
                btn = QPushButton(task)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setProperty("active", False)
                btn.setStyleSheet(self._btn_style(GROUP_COLORS[group_name]))
                btn.clicked.connect(
                    lambda _, n=task, c=GROUP_COLORS[group_name]: self._on_click(n, c)
                )
                inner.addWidget(btn)
                self.buttons[task] = btn

        inner.addStretch()

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #222222;")
        inner.addWidget(sep)

        about_btn = QPushButton("About")
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #555555;
                padding: 9px 12px;
                text-align: left;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover {
                color: #aaaaaa;
                background-color: #1a1a1a;
            }
        """)
        about_btn.clicked.connect(self._show_about)
        inner.addWidget(about_btn)

        scroll.setWidget(container)
        root.addWidget(scroll)

    @staticmethod
    def _btn_style(accent: str) -> str:
        return f"""
            QPushButton {{
                background-color: transparent;
                color: #cccccc;
                padding: 7px 10px 7px 16px;
                text-align: left;
                border-radius: 4px;
                font-size: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #1c1c1c;
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background-color: #242424;
            }}
            QPushButton[active=true] {{
                background-color: #1a2a1a;
                color: #ffffff;
                border-left: 3px solid {accent};
                padding-left: 13px;
            }}
        """

    def _on_click(self, name: str, accent: str):
        if self._active_btn:
            self._active_btn.setProperty("active", False)
            self._active_btn.style().unpolish(self._active_btn)
            self._active_btn.style().polish(self._active_btn)

        btn = self.buttons[name]
        btn.setProperty("active", True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        self._active_btn = btn

        self.analysis_requested.emit(name)

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.exec_()
