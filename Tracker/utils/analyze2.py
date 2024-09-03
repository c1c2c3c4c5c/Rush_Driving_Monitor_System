from Tracker.utils.generate_data import generate_sample_data


def classify_driving_behavior(data, window_size=30):
    classifications = []

    for i in range(0, len(data), window_size):
        window = data[i:i+window_size]

        # Calculate the change in latitude and longitude over the window
        start_lat, start_long, _ = window[0]
        end_lat, end_long, _ = window[-1]
        delta_lat = end_lat - start_lat
        delta_long = end_long - start_long

        # Classify behavior based on the calculated changes
        if abs(delta_lat) < 0.0001 and abs(delta_long) < 0.0001:
            behavior = "HALTED"
        elif abs(delta_lat) < 0.0005 and abs(delta_long) < 0.0005:
            behavior = "NORMAL"
        elif abs(delta_lat) < 0.001 and abs(delta_long) < 0.001:
            behavior = "AGGRESSIVE"
        else:
            behavior = "DANGEROUS"

        classifications.append(behavior)

    return classifications

start_latitude = 37.7749
start_longitude = -122.4194
start_timestamp = 1633302000000  # Initial timestamp in milliseconds
num_data_points = 30000  # Number of data points per second

data = generate_sample_data(num_data_points, start_latitude, start_longitude, start_timestamp)
# divide sample data in parts of 30 elements
behavior_classifications = classify_driving_behavior(data)

# Print the behavior classifications for each second
for i, behavior in enumerate(behavior_classifications):
    print(f"Second {i + 1}: {behavior}")