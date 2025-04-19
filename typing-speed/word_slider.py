import tkinter as tk
from tkinter import ttk, font

class WordSlider(ttk.Frame):
  def __init__(self, master:tk.Misc, word_file:str, width: int, height:int):
    super().__init__(master, width=width, height=height)

    self._load_words(word_file)
    self._prepare_words()
    self._create_slider()


  def next_word(self) -> None:
    if self._current_word_idx < self._num_words:
      self._current_word_idx += 1
    else:
      self._current_word_idx = 0

    self._current_word.set(self._word_list[self._current_word_idx])


  def prev_word(self) -> None:
    if self._current_word_idx > 0:
      self._current_word_idx -= 1
    else:
      self._current_word_idx = self._num_words
    
    self._current_word.set(self._word_list[self._current_word_idx])


  # Load words from file into a list
  def _load_words(self, word_file:str) -> None:
    try:
      with open(word_file) as file:
        # Flatten the files into a list of words
        self._word_list = [word for words in file.readlines() for word in words.split()]

    except FileNotFoundError as ex:
      print(f'{word_file}: {ex.strerror}')
      self._word_list = ['No', 'Word', 'List', 'Found']


  def _prepare_words(self) -> None:
    self._num_words = len(self._word_list) - 1
    self._current_word_idx = 0
    self._current_word = tk.StringVar(self, value=self._word_list[self._current_word_idx])
    self._current_word_length = len(self._current_word.get())


  def _create_slider(self) -> None:
    display_font = font.Font(family='Helvetica', name='WordFont', size=36, weight='bold')
    current_word = ttk.Label(self, textvariable=self._current_word, font=display_font, padding=(30, 30))
    current_word.pack()
