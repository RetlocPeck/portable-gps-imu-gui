import time
import socket
import os
from config import IS_WINDOWS

# Bluetooth RFCOMM UUID (standard Serial Port Profile)
BT_UUID = "00001101-0000-1000-8000-00805F9B34FB"

def bluetooth_stream(data_queue):
    if IS_WINDOWS:
        print("[Bluetooth] Skipped — Windows mock mode.")
        return

    # Create native Bluetooth RFCOMM socket
    server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    try:
        server_sock.bind(("", 1))  # Bind to channel 1
        server_sock.listen(1)

        print("[Bluetooth] Waiting for connection on channel 1...")

        client_sock, client_info = server_sock.accept()
        print(f"[Bluetooth] Connected to {client_info}")

        while True:
            if not data_queue.empty():
                data = data_queue.get()
                msg = (
                    f"Lat: {data['lat']}, Lon: {data['lon']}, Alt: {data['altitude']}, "
                    f"Accel: {data['accel']}, Gyro: {data['gyro']}, Mag: {data['mag']}, "
                    f"Timestamp: {data['timestamp']}\n"
                )
                client_sock.send(msg.encode('utf-8'))
                time.sleep(1)

    except Exception as e:
        print(f"[Bluetooth] Error: {e}")
    finally:
        client_sock.close()
        server_sock.close()
        print("[Bluetooth] Connection closed.")