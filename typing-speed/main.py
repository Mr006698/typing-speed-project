import tkinter as tk
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class TypingSpeedTest(tk.Tk):
  def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
    super().__init__(screenName, baseName, className, useTk, sync, use)
    self.title = 'Typing Speed Test'
    self.minsize(640, 480)
    self._load_theme()
    # Hide the root window until centered on screen
    self.withdraw()

    # Create the GUI
    ################
    
    # Show the window
    self._center_window()
    self.deiconify()


  # Window config functions
  # -----------------------
  def _load_theme(self) -> None:
    styles = ttk.Style()
    styles.theme_use('clam')
    styles.configure('Vertical.TScrollbar', background='lightgrey', arrowsize=16)
    styles.configure('Horizontal.TScrollbar', background='lightgrey', arrowsize=16)
  

  def _center_window(self) -> None:
    self.update_idletasks()
    width = self.winfo_width()
    height = self.winfo_height()
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    self.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == '__main__':
  app = TypingSpeedTest()
  app.mainloop()
