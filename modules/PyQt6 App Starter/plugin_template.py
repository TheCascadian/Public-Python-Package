class Plugin:
    def load(self, parent):
        parent.menu_widget.clear()
        parent.menu_widget.addItem("New Game")
        parent.menu_widget.addItem("Load Game")
        parent.menu_widget.addItem("Settings")
        parent.menu_widget.addItem("Exit")
        parent.menu_widget.itemClicked.connect(lambda item: self.plugin_menu_action(item, parent))
    
    def plugin_menu_action(self, item, parent):
        text = item.text()
        if text == "Exit":
            parent.close()
    
    def unload(self):
        pass
