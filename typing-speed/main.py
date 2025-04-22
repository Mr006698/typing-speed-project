from math import fsum
import tkinter as tk
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from word_slider import WordSlider

WORD_FILE: str = 'typing-speed/test_file.txt'
STAT_UPDATE_FREQ: int = 1000 # in milliseconds
MILLI_SEC_PER_MIN: int = 60000

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
    self._create_timer()


  def _create_gui(self) -> None:
    # Speed and accuracy statistics
    self._words_per_minute = tk.StringVar(self, '0.00')
    self._accuracy = tk.StringVar(self, '100%')
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
    self._text_box = tk.Text(self, padx=25, pady=25)
    self._text_tag_buffer: str | None = None
    self._text_box.tag_configure('Red', background='lightsalmon')
    self._text_box.bind('<Key>', self._key_press)
    self._text_box.focus_set()
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
        self._process_key(ev.char)
        return
      
      case 'Caps_Lock':
        return
      
      case 'Tab':
        return
      
      case 'BackSpace':
        # Move WordSlider.current_word_index() back one if not space
        char_pos = self._text_box.index(tk.INSERT)
        if char_pos == '1.0': # Ignore start of  text
          return
        
        deleted_char = self._text_box.get(self._get_beg_index(char_pos), char_pos)
        if not deleted_char.isspace():
          self._word_slider.delete_char()

      case _:
        self._process_key(ev.char)

  
  def _process_key(self, char: str) -> None:
    char_pos = self._text_box.index(tk.INSERT)
    if self._text_tag_buffer is not None:
      self._text_box.tag_add('Red', self._text_tag_buffer, char_pos)
      self._text_tag_buffer = None

    if char.isspace(): # Record space in the buffer but not check it against the list in word_slider
      return
    
    if not self._word_slider.check_char(char):
      self._text_tag_buffer = char_pos

    
  def _get_end_index(self, char_pos: str) -> str:
    row_idx, col_idx = char_pos.split('.')
    return f'{row_idx}.{(int(col_idx) + 1)}'
  
  def _get_beg_index(self, char_pos: str) -> str:
    row_idx, col_idx = char_pos.split('.')
    if col_idx == '0' and row_idx != '1': # Must be multiline
      # Get the start of the next line
      row_end_idx = self._text_box.index(f'{(int(row_idx) - 1)}.end')

      return row_end_idx

    return f'{row_idx}.{(int(col_idx) - 1)}'
  

  def _create_timer(self) -> None:
    self._update_tick:int = STAT_UPDATE_FREQ
    self._wpm_list:list[float] = []
    self.after(STAT_UPDATE_FREQ, self._update_timer) # Initial timer start

  
  def _update_timer(self) -> None:
    self._update_tick += STAT_UPDATE_FREQ
    self._calculate_wpm()
    self._calculate_acc()
    self.after(STAT_UPDATE_FREQ, self._update_timer)  # Recursive call


  def _calculate_wpm(self) -> None:
    wpm:float = (self._word_slider.word_count / self._update_tick) * MILLI_SEC_PER_MIN
    self._wpm_list.append(wpm)
    avg_wpm = self._calculate_avg_wpm()
    self._words_per_minute.set(avg_wpm)


  def _calculate_avg_wpm(self) -> str:
    wpm_samples = len(self._wpm_list)
    wpm_total = fsum(self._wpm_list)
    return f'{wpm_total / wpm_samples:.2f}'
  

  def _calculate_acc(self) -> None:
    num_errors:float = len(self._text_box.tag_ranges('Red')) * 0.5
    if num_errors > 0.0:
      text_str:str = self._text_box.get('1.0', 'end-1c')
      num_chars = len(text_str) - text_str.count('\n')
      error_percent = (num_errors / num_chars) * 100
      self._accuracy.set(f'{100 - error_percent:.2f}%')


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
