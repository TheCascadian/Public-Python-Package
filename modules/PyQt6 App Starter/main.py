import sys
import os
import importlib.util
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction

from plugin_template import Plugin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plugins = {}
        
        self.menu_widget = QListWidget()
        self.setCentralWidget(self.menu_widget)
        self.populate_default_menu()
    
    def populate_default_menu(self):
        self.menu_widget.clear()
        self.menu_widget.addItem("Start")
        self.menu_widget.addItem("Options")
        self.menu_widget.addItem("Exit")
        self.menu_widget.addItem("Load Plugin")
        self.menu_widget.addItem("Unload Plugin")
        self.menu_widget.itemClicked.connect(self.menu_action)
    
    def menu_action(self, item):
        text = item.text()
        if text == "Exit":
            self.close()
        elif text == "Load Plugin":
            self.load_plugin()
        elif text == "Unload Plugin":
            self.unload_plugin()
    
    def load_plugin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Plugin", "", "Python Files (*.py)")
        if path:
            name = os.path.splitext(os.path.basename(path))[0]
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.plugins[name] = mod
            if hasattr(mod, "Plugin"):
                plugin_instance = mod.Plugin()
                plugin_instance.load(self)
    
    def unload_plugin(self):
        if self.plugins:
            name = next(iter(self.plugins))
            if hasattr(self.plugins[name], "Plugin"):
                self.plugins[name].Plugin().unload()
            del self.plugins[name]

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
