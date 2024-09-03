from Tracker.utils.generate_data import generate_sample_data


def parse_input(input_data):
    latitudes = []
    longitudes = []
    timestamps = []
    accelerations = []
    gyroscopes = []

    for entry in input_data:
        latitudes.append(entry[0])
        longitudes.append(entry[1])
        timestamps.append(entry[2])
        accelerations.append(entry[3:6])
        gyroscopes.append(entry[6:9])

    return latitudes, longitudes, timestamps, accelerations, gyroscopes


def calculate_change_in_velocity(accelerations, timestamps):
    velocities = [0]  # Initial velocity is assumed to be zero

    for i in range(1, len(accelerations)):
        dt = (timestamps[i] - timestamps[i - 1]) / 1000.0  # Convert timestamp to seconds
        delta_v = sum([a * dt for a in accelerations[i]])  # Calculate change in velocity
        velocities.append(velocities[-1] + delta_v)

    return velocities

def classify_driving_behavior(velocities):
    behavior = []
    for velocity in velocities:
        print(velocity)
        if velocity < 0.1:
            behavior.append("HALTED")
        elif velocity < 5.0:
            behavior.append("NORMAL")
        elif velocity < 10.0:
            behavior.append("AGGRESSIVE")
        else:
            behavior.append("DANGEROUS")

    return behavior


# Sample Input
start_latitude = 37.7749
start_longitude = -122.4194
start_timestamp = 1633302000000  # Initial timestamp in milliseconds
num_data_points = 50000  # Number of data points per second

sample_data = generate_sample_data(num_data_points, start_latitude, start_longitude, start_timestamp)

# divide sample data in parts of 30 elements
sample_data = [sample_data[x:x + 500] for x in range(0, len(sample_data), 500)]

for data in sample_data:
    latitudes, longitudes, timestamps, accelerations, gyroscopes = parse_input(data)
    velocities = calculate_change_in_velocity(accelerations, timestamps)
    driving_behavior = classify_driving_behavior(velocities)
    if 'DANGEROUS' in driving_behavior:
        print('DANGEROUS')
    elif 'AGGRESSIVE' in driving_behavior:
        print('AGGRESSIVE')
    elif 'NORMAL' in driving_behavior:
        print('NORMAL')
    else:
        print('HALTED')
# Step 1: Parse the input data

# Step 2: Calculate change in velocity
# velocities = calculate_change_in_velocity(accelerations, timestamps)
#
# # Step 3: Classify driving behavior
# driving_behavior = classify_driving_behavior(velocities)
#
# # Print the driving behavior for each time step
# for i, behavior in enumerate(driving_behavior):
#     print(f"Time: {timestamps[i]}, Latitude: {latitudes[i]}, Acceleration: {velocities[i]}, Behavior: {behavior}")
