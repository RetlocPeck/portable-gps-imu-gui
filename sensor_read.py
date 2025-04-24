import time
from config import IS_WINDOWS

if not IS_WINDOWS:
    import serial
    import adafruit_gps
    import board
    import busio
    import digitalio
    import adafruit_lsm9ds1

    # Setup UART for GPS
    gps_uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
    gps = adafruit_gps.GPS(gps_uart, debug=False)
    gps.send_command(b'PMTK220,1000')  # 1 Hz update rate
    gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

    # Setup SPI for LSM9DS1
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

    cs_ag = digitalio.DigitalInOut(board.D5)  # Chip select for accelerometer/gyro
    cs_m = digitalio.DigitalInOut(board.D6)   # Chip select for magnetometer

    cs_ag.direction = digitalio.Direction.OUTPUT
    cs_m.direction = digitalio.Direction.OUTPUT

    imu = adafruit_lsm9ds1.LSM9DS1_SPI(spi, cs_ag, cs_m)

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

        # Fallback while GPS is still acquiring fix
        if gps.latitude is None or gps.longitude is None:
            print("[Sensor] Waiting for GPS fix...")
            gps_lat = 0.0
            gps_lon = 0.0
            gps_alt = 0.0
        else:
            gps_lat = gps.latitude
            gps_lon = gps.longitude
            gps_alt = gps.altitude_m

        return {
            "timestamp": time.time(),
            "lat": gps_lat,
            "lon": gps_lon,
            "altitude": gps_alt,
            "mag": imu.magnetic,
            "accel": imu.acceleration,
            "gyro": imu.gyro,
        }