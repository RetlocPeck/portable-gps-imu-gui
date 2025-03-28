import tkinter as tk
from config import IS_WINDOWS

# This class creates a simple GUI using Tkinter.
# It displays sensor data in a label and updates it every second.
class SensorGUI:
    # Initializes the GUI with a label to display sensor data.
    # The title of the window changes based on the operating system.
    def __init__(self, root):
        self.label = tk.Label(root, text="Loading...", font=("Helvetica", 16))
        self.label.pack(pady=20)

        if IS_WINDOWS:
            root.title("Sensor GUI [Windows - Mock Mode]")
        else:
            root.title("Sensor GUI [Raspberry Pi - Live Mode]")

    # Updates the label with the latest sensor data.
    # It formats the data into a readable string and sets it as the label's text.
    def update(self, data):
        text = (
            f"Lat: {data['lat']}\n"
            f"Lon: {data['lon']}\n"
            f"Alt: {data['altitude']}\n"
            f"Accel: {data['accel']}\n"
            f"Gyro: {data['gyro']}\n"
            f"Magnetometer: {data['mag']}\n"
            f"Timestamp: {data['timestamp']}"
        )
        self.label.config(text=text)