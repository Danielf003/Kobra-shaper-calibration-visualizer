import tkinter as tk
from tkinter import filedialog
from tkinter import font

import matplotlib

from main import visualize_shaper_calibration

# Use TkAgg backend
matplotlib.use('TkAgg')


def browse_files():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a file",
        filetypes=(
            ("CSV files", "*.csv*"),
            ("all files", "*.*")
        )
    )
    # Change label contents
    label_file_explorer.configure(text="Selected file: " + filename)


def run():
    try:
        filename = label_file_explorer.cget("text").split(": ")[1]
        print('Selected file: ' + filename)
    except IndexError:
        print('Select a CSV file.')
        return

    visualize_shaper_calibration(filename, selected_shaper.get(), is_plotting_extra.get(), is_freq_lim_200hz.get())


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Kobra Shaper Calibration Visualizer by Danielf003")

    font1 = font.Font(family="Arial", size=11, weight="normal", slant="roman")

    selected_shaper = tk.IntVar()
    is_plotting_extra = tk.BooleanVar()
    is_freq_lim_200hz = tk.BooleanVar()

    is_plotting_extra.set(True)
    is_freq_lim_200hz.set(False)

    frame_browse = tk.Frame(root)
    frame_main = tk.Frame(root)

    label_file_explorer = tk.Label(
        frame_browse,
        text="Select a CSV file to visualize:", font=font1,
        anchor=tk.E, padx=10
    )
    label_file_explorer.pack(side=tk.LEFT, anchor=tk.E)

    tk.Button(frame_browse, text="Browse...", font=font1, bg='#D9D9D9',
              command=browse_files).pack(anchor=tk.E)

    frame_shapers = tk.Frame(frame_main)
    frame_options = tk.Frame(frame_main)

    tk.Label(frame_shapers, text="Select the \nrecommended \nshaper:", font=font1,
             justify=tk.LEFT).pack(anchor=tk.W)

    shaper_names = ('zv', 'mzv', 'ei', '2hump_ei', '3hump_ei')
    for i, n in enumerate(shaper_names):
        tk.Radiobutton(frame_shapers, text=n, font=font1,
                       variable=selected_shaper,
                       value=i).pack(anchor=tk.W, padx=10)

    tk.Checkbutton(frame_options, text='Plot extra graph for applied shapers', font=font1,
                   variable=is_plotting_extra).pack(anchor=tk.W, padx=20, pady=15)
    tk.Checkbutton(frame_options, text='Fix max frequency to 200Hz', font=font1,
                   variable=is_freq_lim_200hz).pack(anchor=tk.W, padx=20, pady=15)

    big_button = tk.Button(frame_options, text='Plot', bg='#C9FFC9', height=2,
                           command=run)
    big_button.config(font=("arial", 25, 'bold'))
    big_button.pack(expand=True, fill=tk.BOTH)

    frame_shapers.pack(side=tk.LEFT, padx=10, pady=10)
    frame_options.pack(side=tk.LEFT)

    frame_browse.pack(padx=5, pady=5)
    frame_main.pack(padx=5, pady=5)

    root.mainloop()
