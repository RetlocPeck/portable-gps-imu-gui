import csv
from config import IS_WINDOWS

# Function to write sensor data to a CSV file
def write_to_csv(filename, data):
    try:
        with open(filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data["timestamp"], data["lat"], data["lon"],
                data["altitude"], *data["accel"], *data["gyro"]
            ])
    except Exception as e:
        if IS_WINDOWS:
            print(f"[Logger] Failed to write to CSV: {e}")