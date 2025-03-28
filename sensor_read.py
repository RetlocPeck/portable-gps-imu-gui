import time
from config import IS_WINDOWS

if not IS_WINDOWS:
    import serial
    import board
    import busio
    import adafruit_icm20x
    import adafruit_gps

    # Setup UART for GPS
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b'PMTK220,1000')  # 1 Hz
    gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

    # Setup I2C for IMU
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_icm20x.ICM20948(i2c)

def get_sensor_data():
    if IS_WINDOWS:
        # Return mock data for testing
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
        # Update GPS and IMU data
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