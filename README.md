# PyroX — Wildfire Intelligence Platform

> **⚠ This project is actively under development. The frontend UI is functional; backend analysis workers are currently in progress.**

---

## Overview

PyroX is a desktop application for satellite-based wildfire analysis and monitoring. It provides a structured interface for running a wide range of fire, spatial, temporal, atmospheric, and terrain analyses on uploaded satellite imagery. The application is built with Python and PyQt5, following a clean modular architecture that separates the UI from the analysis logic.

---

## Features

- Dark-themed, professional desktop UI built with PyQt5
- Sidebar with categorized analysis options across five domains
- Interactive image viewer with pan, zoom, grid overlay, and axis display
- Toolbar with upload, remove, zoom in/out, and reset view controls
- Active state tracking on sidebar buttons with per-group accent colors
- Result bar that displays analysis output below the viewer
- About dialog with application information
- Modular file structure ready for backend integration

---

## Project Structure

```
PyroX/
│
├── main.py                  # Application entry point, main window
│
├── ui/
│   ├── sidebar.py           # Sidebar widget with analysis groups and About dialog
│   ├── contentpanel.py      # Main content area with image viewer and toolbar
│   └── menu.py              # Menu bar builder (File, Edit, Help)
│
└── pyrox_logo.png           # Application icon
```

---

## File Breakdown

### `main.py`

The application entry point. Defines `MainWindow`, which:

- Sets the window title, icon, minimum size (900×600), and default size (1280×800)
- Builds the menu bar via `MenuBarBuilder`
- Constructs the main layout: `Sidebar` + separator + `ContentPanel`
- Connects the `analysis_requested` signal from the sidebar to `_on_analysis`, which validates that an image is loaded before dispatching to a backend worker

```python
self.sidebar.analysis_requested.connect(self._on_analysis)
```

The Windows taskbar App User Model ID is also set here for proper icon display on Windows.

---

### `ui/sidebar.py`

Contains three components:

**`ANALYSIS_GROUPS`** — A dictionary defining five analysis categories and their tasks:

| Group | Color |
|---|---|
| FIRE & THERMAL | `#e05c2a` (orange-red) |
| SPATIAL | `#4a9eff` (blue) |
| TEMPORAL | `#4caf50` (green) |
| ATMOSPHERIC & SMOKE | `#aaaaaa` (grey) |
| TERRAIN & ENVIRONMENT | `#8bc34a` (lime) |

**`AboutDialog`** — A styled `QDialog` showing application name, subtitle, and a short description. Opened by clicking the About button at the bottom of the sidebar.

**`Sidebar`** — The main sidebar widget. Features:
- Fixed width of 220px
- A branded header with the PyroX name and "Wildfire Intelligence" subtitle
- A scrollable area containing all analysis group headers and task buttons
- A colored top rule above each group header for visual separation
- Active button state with a left accent border, toggled on click
- Emits `analysis_requested(str)` signal with the selected task name when a button is clicked
- An About button at the bottom that opens `AboutDialog`

---

### `ui/contentpanel.py`

Contains two components:

**`ImageViewer`** — A subclass of `QGraphicsView` that:
- Renders a subtle dot grid and axis lines over a dark background
- Displays loaded images centered in the scene
- Supports scroll-wheel zoom, click-and-drag panning, programmatic zoom in/out, and fit-to-view reset
- Uses `QGraphicsPixmapItem` with smooth transformation mode

**`ContentPanel`** — The main content area widget. Features:
- A toolbar with Upload Image, Remove, zoom (−/+), and Reset View buttons
- A status pill on the right of the toolbar showing the loaded filename or "No image loaded"
- The `ImageViewer` occupying the remaining vertical space
- A result bar at the bottom (hidden by default) that displays analysis output from `show_result(analysis, text)`

---

### `ui/menu.py`

**`MenuBarBuilder`** — Builds and styles the application menu bar with three menus:

- **File** — New, Open, Save, Save As, Exit (Exit is wired to close the window)
- **Edit** — Copy, Paste
- **Help** — Help, About

The menu bar uses a dark style consistent with the rest of the UI (`#1e1e1e` background, white text).

---

## Analysis Categories

### Fire & Thermal
Covers core fire detection and thermal characterization tasks including segmentation, localization, intensity estimation, radiative power analysis, thermal anomaly detection, and hotspot detection.

### Spatial
Handles geographic and spatial tasks such as fire spread mapping, heatmap generation, region-wise fire density analysis, and infrastructure proximity analysis.

### Temporal
Time-based analyses including fire progression tracking, change detection, burn area growth rate, multi-temporal NDMI analysis, and seasonal trend analysis.

### Atmospheric & Smoke
Smoke detection and plume segmentation, aerosol optical depth analysis, and air quality impact estimation.

### Terrain & Environment
Environmental context analyses including slope and aspect analysis, wind influence, temperature and humidity correlation, and land cover classification.

---

## Requirements

- Python 3.10+
- PyQt5

Install dependencies:

```bash
pip install PyQt5
```

---

## Running the Application

```bash
python main.py
```

On Windows, ensure `pyrox_logo.png` is present in the root directory for the taskbar icon to display correctly.

---

## Backend Status

> **The backend analysis engine is currently under active development.**

The frontend UI is complete and fully functional. The `_on_analysis` method in `main.py` is the integration point where each selected analysis task will dispatch to its corresponding backend worker. When a task button is clicked, the application currently shows a `Running '<task>'...` placeholder in the result bar.

Planned backend work includes:

- Satellite image preprocessing pipeline
- Integration of analysis workers for each of the 27 analysis tasks
- Results rendering back into the image viewer (overlays, heatmaps, segmentation masks)
- Export functionality for analysis results
