from tkinter import Tk, ttk
from gui import VideoConverterGUI

if __name__ == "__main__":
    root = Tk()
    root.tk.call('source', 'forest-dark.tcl')
    ttk.Style().theme_use('forest-dark')
    gui = VideoConverterGUI(root)
    root.mainloop()
