# Kobra-shaper-calibration-visualizer
Plot your Anicubic Kobra input shaping calibration results from a CSV file.

# What's this for?
When calibrating input shaping on Anycubic Kobra 3d-printer with SHAPER_CALIBRATE AXIS=X or Y, the output CSV file has different structure than what vanilla Klipper outputs, so it can't be used with Klipper scripts (at least to my knowledge). That's because Kobra printers (or at least Kobra S1) run on a modified version of Klipper, known as GoKlipper, which is not opensource as of April 2025.

This repository is a solution to the above problem. Provided you can access CSV files after calibration, this utility visualises them in a way familiar to Klipper users.

This project was inspired by 
https://github.com/theycallmek/Klipper-Input-Shaping-Assistant,

which in turn was based on official Klipper repo:
https://github.com/Klipper3d/klipper

# Where to get the CSV from
In case you don't know how to send commands to your Kobra printer and access its filesystem with SSH, your are probably running on stock firmware. In order to continue with the following steps, consider installing custom firmware (refer to https://github.com/jbatonnet/Rinkhals) or obtaining the CSV file by other means. 

First you need to obtain the CSV file/files with X and/or Y input shaping calibration results. Executing `SHAPER_CALIBRATE AXIS=X` (or Y) generates a file named `calibration_data_x_*.csv` in the /tmp folder of the printer.

Copy the file(s) to the desired location on your local machine (you probably want to use `scp` command).

# How to use
## With GUI
- Download an .exe file from the [Releases](https://github.com/Danielf003/Kobra-shaper-calibration-visualizer/releases/) and run it.
- Or you can build it from source code yourself in cmd with `pyinstaller gui.py --onefile` (requirements below).
- Or you can run the python script itself with `python gui.py` (requirements below).

Once the window appears, browse to a CSV file with its original name starting as `calibration_data_`, tweak visualisation options if needed, and press the **Plot** button.

## With command line
Requires: python>=3.9, numpy, matplotlib

Run with `python main.py /path/to/file.csv 0 -e`,

or read help with `python main.py -h` to learn about the arguments and usage.
