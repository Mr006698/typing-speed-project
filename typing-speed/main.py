import tkinter as tk
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from word_slider import WordSlider

from pprint import pprint

WORD_FILE = 'typing-speed/test_file.txt'

class TypingSpeedTest(tk.Tk):
  def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
    super().__init__(screenName, baseName, className, useTk, sync, use)
    self.title('Typing Speed Test')
    self.minsize(640, 480)
    self._load_theme()
    self.bind('<Key>', self._key_press)
    # Hide the root window until centered on screen
    self.withdraw()
    self._center_window()
    self.deiconify()

    # Create the GUI
    self._create_gui()


  def _create_gui(self) -> None:
    # Speed and accuracy metrics
    self._words_per_minute = tk.StringVar(self, '0')
    self._accuracy = tk.StringVar(self, '0%')
    performance_display = ttk.Frame(self)
    wpf_label = ttk.Label(performance_display, text='Words per Minute: ')
    wpf_label.pack(side=tk.LEFT)
    wpf_value = ttk.Label(performance_display, textvariable=self._words_per_minute)
    wpf_value.pack(side=tk.LEFT)
    acc_label = ttk.Label(performance_display, text='Accuracy: ')
    acc_label.pack(side=tk.LEFT)
    acc_value = ttk.Label(performance_display, textvariable=self._accuracy)
    acc_value.pack(side=tk.LEFT)
    performance_display.pack(side=tk.TOP)

    # Current word display
    self._word_slider = WordSlider(
      self,
      word_file=WORD_FILE,
      width=self.winfo_width(),
      height=int(self.winfo_height()*0.25))
    
    self._word_slider.pack(side=tk.TOP)

    # Typing text box
    text_box = tk.Text(self)
    text_box.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

  
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
        self._word_slider.next_word()

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
