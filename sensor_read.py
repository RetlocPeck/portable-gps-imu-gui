import time
from config import IS_WINDOWS

if not IS_WINDOWS:
    import serial
    import adafruit_gps
    import adafruit_bno055
    import board
    import busio

    # Setup UART for GPS
    gps_uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    gps = adafruit_gps.GPS(gps_uart, debug=False)
    gps.send_command(b'PMTK220,1000')  # 1 Hz update rate
    gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

    # Setup UART for BNO055 (on ttyAMA2)
    imu_uart = serial.Serial("/dev/ttyAMA2", baudrate=115200, timeout=1)
    imu = adafruit_bno055.BNO055_UART(imu_uart)

def get_sensor_data():
    if IS_WINDOWS:
        return {
            "timestamp": time.time(),
            "lat": 35.123456,
            "lon": -97.654321,
            "altitude": 300.0,
            "mag": (-12.3, 4.8, 35.6),
            "accel": (0.01, -0.02, 9.81),
            "gyro": (0.001, 0.002, 0.003),
        }
    else:
        gps.update()
        return {
            "timestamp": time.time(),
            "lat": gps.latitude,
            "lon": gps.longitude,
            "altitude": gps.altitude_m,
            "mag": imu.magnetic,
            "accel": imu.acceleration,
            "gyro": imu.gyro,
        }