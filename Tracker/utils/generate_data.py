import random
import time


def generate_sample_data(num_points, start_lat, start_long, start_time):
    # Initialize lists to store generated data
    data = []

    # Set initial values
    lat = start_lat
    long = start_long
    timestamp = start_time
    acc_range = (0.0, 1.0)  # Range for accelerometer values
    gyro_range = (-0.1, 0.1)  # Range for gyroscope values

    for i in range(num_points):
        # Generate random accelerometer and gyroscope values
        if random.random() < 0.40:  # 5% chance of a sudden acceleration spike
            accX = random.uniform(2.0, 5.0)
            accY = random.uniform(2.0, 5.0)
            accZ = random.uniform(2.0, 5.0)
        else:
            accX = random.uniform(*acc_range)
            accY = random.uniform(*acc_range)
            accZ = random.uniform(*acc_range)

        gyroX = random.uniform(*gyro_range)
        gyroY = random.uniform(*gyro_range)
        gyroZ = random.uniform(*gyro_range)

        # Append the data point to the list
        data_point = [lat, long, timestamp]#, accX, accY, accZ, gyroX, gyroY, gyroZ]
        data.append(data_point)

        # Update latitude, longitude, and timestamp for the next data point
        if random.random() < 0.05:
            lat += random.randint(1, 15)/100000  # Small change in latitude (for demonstration purposes)
            long += random.randint(1, 15)/100000  # Small change in longitude (for demonstration purposes)
        else:
            lat += 0.00001
            long += 0.00001
        timestamp += 30  # Increment timestamp by 30 milliseconds (for demonstration purposes)

    return data


# Example usage
start_latitude = 37.7749
start_longitude = -122.4194
start_timestamp = 1633302000000  # Initial timestamp in milliseconds
num_data_points = 300  # Number of data points per second

sample_data = generate_sample_data(num_data_points, start_latitude, start_longitude, start_timestamp)

# Print the generated sample data
# for data_point in sample_data:
#     print(data_point)
