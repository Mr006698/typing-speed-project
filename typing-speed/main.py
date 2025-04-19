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
    wpf_label.pack(side=tk.LEFT, padx=(20, 0), pady=(10, 0))
    wpf_value = ttk.Label(performance_display, textvariable=self._words_per_minute)
    wpf_value.pack(side=tk.LEFT, padx=(0, 0), pady=(10, 0))
    acc_value = ttk.Label(performance_display, textvariable=self._accuracy)
    acc_value.pack(side=tk.RIGHT, padx=(0, 20), pady=(10, 0))
    acc_label = ttk.Label(performance_display, text='Accuracy: ')
    acc_label.pack(side=tk.RIGHT, padx=(0, 0), pady=(10, 0))
    performance_display.pack(side=tk.TOP, fill=tk.X)

    # Current word display
    self._word_slider = WordSlider(
      self,
      word_file=WORD_FILE,
      width=self.winfo_width(),
      height=int(self.winfo_height()*0.25))
    
    self._word_slider.pack(side=tk.TOP, fill=tk.X)

    # Typing text box
    self._text_box = tk.Text(self)
    self._text_tag_buffer: str | None = None
    self._text_box.tag_configure('Red', background='lightsalmon')
    self._text_box.bind('<Key>', self._key_press)
    self._text_box.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

  
  # Callback from tk logging key presses
  def _key_press(self, ev: tk.Event) -> None:
    match ev.keysym:
      case 'Shift_L':
        return
      
      case 'Shift_R':
        return
      
      case 'Return':
        return
      
      case 'Control_L':
        return
      
      case 'Control_R':
        return
      
      case 'space':
        # Maybe special use case?
        return
      
      case 'BackSpace':
        # TODO: Move WordSlider.current_word_index() back one
        return

      case _:
        self._process_key(ev.char)

  
  def _process_key(self, char: str) -> None:
    char_pos = self._text_box.index(tk.INSERT)
    if self._text_tag_buffer is not None:
      self._text_box.tag_add('Red', self._text_tag_buffer, char_pos)
      self._text_tag_buffer = None

    if not self._word_slider.check_char(char):
      self._text_tag_buffer = char_pos

    
  def _get_end_index(self, char_pos: str) -> str:
    row_idx, col_idx = char_pos.split('.')
    return f'{row_idx}.{(int(col_idx) + 1)}'


  # Window config functions
  # -----------------------
  def _load_theme(self) -> None:
    styles = ttk.Style()
    styles.theme_use('clam')
    styles.configure('Vertical.TScrollbar', background='lightgrey', arrowsize=16)
    styles.configure('Horizontal.TScrollbar', background='lightgrey', arrowsize=16)
    styles.configure('TFrame', background='lavender')
    styles.configure('TLabel', background='lavender')
  

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
