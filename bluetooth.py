import time
from config import IS_WINDOWS

if not IS_WINDOWS:
    import bluetooth

# This function streams data over Bluetooth using RFCOMM.
# It creates a Bluetooth socket, binds it to any available port,
# and listens for incoming connections. Once a client connects,
# it sends data to the client every second until an error occurs.
# The connection is then closed gracefully.
def bluetooth_stream(data):
    if IS_WINDOWS:
        print("[Bluetooth] Skipped — Windows mock mode.")
        return

    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    print("[Bluetooth] Waiting for connection...")

    client_sock, _ = server_sock.accept()
    print("[Bluetooth] Client connected.")

    try:
        while True:
            client_sock.send(f"{data}\n")
            time.sleep(1)
    except Exception as e:
        print(f"[Bluetooth] Error: {e}")
    finally:
        client_sock.close()
        server_sock.close()
        print("[Bluetooth] Connection closed.")