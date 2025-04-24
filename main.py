import threading
import queue
import time
import os
import tkinter as tk
from sensor_read import get_sensor_data
from bluetooth import bluetooth_stream
from logger import write_to_csv
from gui import SensorGUI
from usb import usb_stream
from config import IS_WINDOWS

# Shared queue for streaming sensor data to all destinations
data_queue = queue.Queue()

# Continuously collect sensor data and push into the queue
def sensor_loop():
    while True:
        data = get_sensor_data()
        data_queue.put(data)
        time.sleep(1)

# Write sensor data to CSV
def csv_loop():
    file_path = "sensor_data.csv" if IS_WINDOWS else "/home/pi/sensor_data.csv"
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            write_to_csv(file_path, data)

# Update GUI with latest sensor data
def gui_loop(gui, root):
    def update():
        if not data_queue.empty():
            data = data_queue.get()
            gui.update(data)
        root.after(1000, update)
    update()

# Stream data over USB serial
def usb_loop():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            usb_stream(data)

# Start all threads
def main():
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    csv_thread = threading.Thread(target=csv_loop, daemon=True)

    sensor_thread.start()
    csv_thread.start()

    if not IS_WINDOWS:
        if os.path.exists("/dev/ttyUSB0"):
            print("[Main] USB device found. Starting USB stream...")
            usb_thread = threading.Thread(target=usb_loop, daemon=True)
            usb_thread.start()
        else:
            print("[Main] No USB device connected. Skipping USB stream.")

        try:
            bluetooth_thread = threading.Thread(target=lambda: bluetooth_stream(data_queue), daemon=True)
            bluetooth_thread.start()
        except Exception as e:
            print(f"[Main] Skipping Bluetooth: {e}")

    root = tk.Tk()
    gui = SensorGUI(root)
    gui_loop(gui, root)
    root.mainloop()

if __name__ == "__main__":
    main()