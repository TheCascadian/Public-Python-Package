import inspect
import sys

try:
    from PyQt6 import QtWidgets, QtGui, QtCore
except ImportError:
    print("PyQt6 is not installed.", file=sys.stderr)
    sys.exit(1)

SIGNAL_MAP = {
    'on_click': ['clicked'],
    'on_change': ['textChanged', 'valueChanged', 'stateChanged', 'currentIndexChanged']
}

def discover_all_widgets():
    """Return a comprehensive list of commonly used QWidget subclasses for wrapping."""
    from PyQt6.QtWidgets import (
        # Controls
        QPushButton, QToolButton, QCommandLinkButton, QCheckBox, QRadioButton,
        QLineEdit, QTextEdit, QPlainTextEdit, QLabel, QSlider,
        QSpinBox, QDoubleSpinBox, QComboBox, QFontComboBox, QDateEdit,
        QTimeEdit, QDateTimeEdit, QProgressBar, QLCDNumber,
        
        # Containers & Layouts
        QGroupBox, QFrame, QStackedWidget, QTabWidget, QSplitter,
        QScrollArea, QMainWindow, QDockWidget, QToolBox,

        # Item Views
        QListWidget, QListView, QTreeWidget, QTreeView,
        QTableWidget, QTableView, QGraphicsView,

        # Dialogs & System UI
        QFileDialog, QColorDialog, QFontDialog, QInputDialog,
        QMessageBox, QDialog, QWizard, QWizardPage,

        # Application Components
        QStatusBar, QMenuBar, QMenu, QSystemTrayIcon, QWidget
    )

    return [
        ("QPushButton", QPushButton),
        ("QToolButton", QToolButton),
        ("QCommandLinkButton", QCommandLinkButton),
        ("QCheckBox", QCheckBox),
        ("QRadioButton", QRadioButton),
        ("QLineEdit", QLineEdit),
        ("QTextEdit", QTextEdit),
        ("QPlainTextEdit", QPlainTextEdit),
        ("QLabel", QLabel),
        ("QSlider", QSlider),
        ("QSpinBox", QSpinBox),
        ("QDoubleSpinBox", QDoubleSpinBox),
        ("QComboBox", QComboBox),
        ("QFontComboBox", QFontComboBox),
        ("QDateEdit", QDateEdit),
        ("QTimeEdit", QTimeEdit),
        ("QDateTimeEdit", QDateTimeEdit),
        ("QProgressBar", QProgressBar),
        ("QLCDNumber", QLCDNumber),

        ("QGroupBox", QGroupBox),
        ("QFrame", QFrame),
        ("QStackedWidget", QStackedWidget),
        ("QTabWidget", QTabWidget),
        ("QSplitter", QSplitter),
        ("QScrollArea", QScrollArea),
        ("QMainWindow", QMainWindow),
        ("QDockWidget", QDockWidget),
        ("QToolBox", QToolBox),

        ("QListWidget", QListWidget),
        ("QListView", QListView),
        ("QTreeWidget", QTreeWidget),
        ("QTreeView", QTreeView),
        ("QTableWidget", QTableWidget),
        ("QTableView", QTableView),
        ("QGraphicsView", QGraphicsView),

        ("QFileDialog", QFileDialog),
        ("QColorDialog", QColorDialog),
        ("QFontDialog", QFontDialog),
        ("QInputDialog", QInputDialog),
        ("QMessageBox", QMessageBox),
        ("QDialog", QDialog),
        ("QWizard", QWizard),
        ("QWizardPage", QWizardPage),

        ("QStatusBar", QStatusBar),
        ("QMenuBar", QMenuBar),
        ("QMenu", QMenu),
        ("QSystemTrayIcon", QSystemTrayIcon),
        ("QWidget", QWidget)
    ]

def generate_wrapper(name):
    base = name[1:] if name.startswith("Q") else name
    return f"""
{base}Base = {name}
class {base}({base}Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for kwarg, signals in {{
            'on_click': {SIGNAL_MAP['on_click']},
            'on_change': {SIGNAL_MAP['on_change']}
        }}.items():
            if kwarg in kwargs:
                cb = kwargs[kwarg]
                for sig in signals:
                    if hasattr(self, sig):
                        try:
                            getattr(self, sig).connect(cb)
                            break
                        except TypeError:
                            continue
""".strip()

def write_all_wrappers(filename="wrapped_all_widgets.py"):
    widgets = discover_all_widgets()
    lines = [
        "from PyQt6.QtWidgets import *",
        "from PyQt6.QtGui import *",
        "from PyQt6.QtCore import Qt",
        ""
    ]
    for name, _ in widgets:
        lines.append(generate_wrapper(name))
        lines.append("")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Wrapped {len(widgets)} widgets to '{filename}'.")

if __name__ == "__main__":
    write_all_wrappers()
