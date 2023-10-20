
import tkinter as tk
from tkinter import filedialog
from tess import process

# Create the root window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Open the file dialog and get the filename
filename = filedialog.askopenfilename()

data = {'file': open(filename, 'rb')}

process(filename)