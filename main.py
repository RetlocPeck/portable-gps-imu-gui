import threading
import queue
import time
import tkinter as tk
from sensor_read import get_sensor_data
from logger import write_to_csv
from gui import SensorGUI
from config import IS_WINDOWS

data_queue = queue.Queue()

# Reads sensor data and puts it in the queue every second
def sensor_loop():
    while True:
        data = get_sensor_data()
        # Pushes the data to the queue
        data_queue.put(data)
        time.sleep(1)

# Writes data from the queue to a CSV file
def csv_loop():
    # Set the file path based on the OS
    file_path = (
        "sensor_data.csv" if IS_WINDOWS
        else "/home/pi/sensor_data.csv"
    )
    while True:
        if not data_queue.empty():
            # Get the data from the queue (deletes it from queue after)
            data = data_queue.get()
            write_to_csv(file_path, data)

def gui_loop(gui):
    def update_gui():
        if not data_queue.empty():
            data = data_queue.get()
            gui.update(data)
        root.after(1000, update_gui)
    update_gui()

# Threads so we can collect data, write to CSV, and update the GUI simultaneously
sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
csv_thread = threading.Thread(target=csv_loop, daemon=True)

# Sets up the GUI
root = tk.Tk()
gui = SensorGUI(root)
gui_thread = threading.Thread(target=gui_loop, args=(gui,), daemon=True)

# Start the threads
sensor_thread.start()
csv_thread.start()
gui_thread.start()
root.mainloop()