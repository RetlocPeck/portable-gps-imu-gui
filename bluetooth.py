import time
from config import IS_WINDOWS

if not IS_WINDOWS:
    import bluetooth

# Stream sensor data over Bluetooth using RFCOMM and PyBluez
def bluetooth_stream(data_queue):
    if IS_WINDOWS:
        print("[Bluetooth] Skipped — Windows mock mode.")
        return

    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        print(f"[Bluetooth] Waiting for connection on RFCOMM channel {port}...")

        client_sock, client_info = server_sock.accept()
        print(f"[Bluetooth] Accepted connection from {client_info}")

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
        if 'client_sock' in locals():
            client_sock.close()
        if 'server_sock' in locals():
            server_sock.close()
        print("[Bluetooth] Connection closed.")