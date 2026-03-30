import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox
from gui import TagWolfGUI
from api_client import TagWolfAPI

class TagWolfApp:
    def __init__(self):
        self.root = tk.Tk()
        self.api = TagWolfAPI()
        self.gui = TagWolfGUI(self.root, self.api)
        self.check_api_status()
        
    def check_api_status(self):
        def check():
            try:
                status = self.api.check_connection()
                self.gui.update_api_status(status)
            except Exception as e:
                self.gui.update_api_status({"status": "offline", "error": str(e)})
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TagWolfApp()
    app.run()
