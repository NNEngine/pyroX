from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)
        self.setStyleSheet("background-color:#0f0f0f;")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none;")

        # Container inside scroll
        container = QWidget()
        content_layout = QVBoxLayout(container)
        content_layout.setSpacing(6)
        content_layout.setContentsMargins(10, 15, 10, 10)

        # Title
        title = QLabel("Analyze Image")
        title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border-bottom: 2px solid black;
        """)
        content_layout.addWidget(title)

        # Buttons
        self.buttons = {}

        fire_thermal_analysis = [
            "Fire Analysis", "Fire Segmentation", "Fire Localization",
            "Fire Intensity Estimation", "Fire Radiative Power Analysis",
            "Thermal Anomaly Detection", "Hotspot Detection"
        ]

        spatial_analysis = [
            "Fire Spread Mapping", "Fire Spread Extraction", "Spatial Extraction",
            "Heatmap Generation", "Region-wise Fire Density Analysis",
            "Distance from Infrastructure Analysis"
        ]

        temporal_analysis = [
            "Fire Progression Tracking", "Time-Series Change Detection",
            "Burn Area Growth Rate Analysis", "Multi-temporal NDMI Analysis",
            "Seasonal Fire Trend Analysis"
        ]

        atmospheric_smoke_analysis = [
            "Smoke Detection", "Smoke Plume Segmentation",
            "Aerosol Optical Depth Analysis", "Air Quality Impact Estimation"
        ]

        terrain_environmental_analysis = [
            "Elevated Impact Analysis", "Slope & Aspect Analysis",
            "Wind Influence Analysis", "Temperature & Humidity Correlation",
            "Land Cover Classification"
        ]

        analysis_task = (
            fire_thermal_analysis
            + spatial_analysis
            + temporal_analysis
            + atmospheric_smoke_analysis
            + terrain_environmental_analysis
        )

        for name in analysis_task:
            btn = QPushButton(name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ccc;
                    padding: 10px;
                    text-align: left;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #1f1f1f;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
            """)
            content_layout.addWidget(btn)
            self.buttons[name] = btn

        # Push bottom section
        content_layout.addStretch()

        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("""
            background-color: rgba(255,255,255,0.08);
            margin-left: 10px;
            margin-right: 10px;
        """)
        content_layout.addWidget(separator)

        # About button
        about_btn = QPushButton("About")
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaa;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1f1f1f;
                color: white;
            }
        """)
        content_layout.addWidget(about_btn)

        # Set container inside scroll
        scroll.setWidget(container)

        # Add scroll to main layout
        main_layout.addWidget(scroll)
