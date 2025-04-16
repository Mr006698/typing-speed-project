import tkinter as tk
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from pprint import pprint

WORD_FILE = 'typing-speed/test_file.txt'

class TypingSpeedTest(tk.Tk):
  def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
    super().__init__(screenName, baseName, className, useTk, sync, use)
    self.title = 'Typing Speed Test'
    self.minsize(640, 480)
    self._load_theme()
    # Hide the root window until centered on screen
    self.withdraw()

    self._load_words()
    self._prepare_words()
    self.bind('<Key>', self._key_press)

    # Create the GUI
    # word_display = ttk.Label(self, text=self._word_list[0])
    # word_display.pack()

    word_len = len(self._word_list[2])
    char_spacing = 0.02
    for idx in range(word_len):
      label = ttk.Label(self, text=self._word_list[2][idx])
      label.place(relx=0.5+(idx*char_spacing), rely=0.2, anchor=tk.CENTER)
    
    # Show the window
    self._center_window()
    self.deiconify()


  # Load words from file into a list
  def _load_words(self) -> None:
    try:
      with open(WORD_FILE) as file:
        # Flatten the files into a list of words
        self._word_list = [word for words in file.readlines() for word in words.split()]

    except FileNotFoundError as ex:
      print(f'{WORD_FILE}: {ex.strerror}')


  def _prepare_words(self) -> None:
    self._num_words = len(self._word_list)
    self._current_word = self._word_list[0]
    print(f'Word file has: {self._num_words} words. Current word is {self._current_word}.')

  
  # Callback from tk logging key presses
  def _key_press(self, ev: tk.Event) -> None:
    match ev.keysym:
      case 'Shift_L':
        return
      
      case 'Shift_R':
        return
      
      case 'Return':
        # Maybe special use case?
        return
      
      case 'Control_L':
        return
      
      case 'Control_R':
        return
      
      case 'space':
        # Maybe special use case?
        return

      case _:
        print(ev.keysym)


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
