import json
import os
from collections import OrderedDict

# Define the order of tests
test_order = [
    "raspberry-pi_basic_1_20241004_140120.db",
    "raspberry-pi_basic_2_20241004_140133.db",
    "raspberry-pi_basic_3_20241004_140137.db",
    "raspberry-pi_large_scale_1000_20241004_140150.db",
]

# Define human-readable field names and their formatting
field_names = {
    "total_bytes_processed": ("Total Bytes Processed (Mb)", "{:.2f}"),
    "avg_bytes_per_second": ("Avg Bytes per Second (Kb/s)", "{:.2f}"),
    "test_duration": ("Test Duration (s)", "{:.2f}"),
    "estimated_processing_time": ("Total Network Time (s)", "{:.2f}"),
    "estimated_networking_time": ("Total Processing Time (s)", "{:.2f}"),
    "avg_queue_time": ("Avg Queue Time (s)", "{:.2f}"),
}

# Read the JSON file
with open(os.path.join("data", "test_results.json"), "r") as file:
    data = json.load(file)

# Extract the relevant configuration
config_data = data["raspberry-pi"]

# Initialize the result list
result = []

# Process each test
for test in test_order:
    test_data = OrderedDict()
    name = ""

    if "basic_1" in test:
        name = "Basic 1"
    elif "basic_2" in test:
        name = "Basic 2"
    elif "basic_3" in test:
        name = "Basic 3"
    elif "large_scale_1000" in test:
        name = "Large Scale 100"

    test_data["Raspberry Pi Tests"] = name

    for original_field, (readable_field, format_str) in field_names.items():
        value = config_data[test][original_field]
        if original_field == "total_bytes_processed":
            # Convert bytes to megabytes
            value /= 1_000_000
        elif original_field == "avg_bytes_per_second":
            # Convert bytes per second to kilobytes per second
            value /= 1_000

        formatted_value = format_str.format(value)
        test_data[readable_field] = formatted_value

    result.append(test_data)

# Write the processed data to a new JSON file
with open(os.path.join("data", "processed_results.json"), "w") as file:
    json.dump(result, file, indent=2)

print("Processed results have been saved to 'data/processed_results.json'")
