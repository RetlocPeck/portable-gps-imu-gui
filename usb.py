import time
import sys
import serial
from config import IS_WINDOWS

# This function streams data through USB serial (e.g., to another device or PC).
# On Windows, it mocks the stream.
def usb_stream(data):
    if IS_WINDOWS:
        print("[USB] Skipped — Windows mock mode.")
        return

    try:
        # Adjust the port as needed for your system (e.g., /dev/ttyUSB0)
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        print("[USB] USB Serial connected.")
        while True:
            ser.write(f"{data}\n".encode('utf-8'))
            time.sleep(1)
    except Exception as e:
        print(f"[USB] Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("[USB] USB Serial connection closed.")