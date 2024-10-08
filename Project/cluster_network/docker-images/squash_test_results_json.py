import json
import os
from collections import OrderedDict

# Define the order of tests
test_order = [
    "arty-a7-2c-improved_basic_1_20241007_121858.db",
    "arty-a7-2c-improved_basic_2_20241007_122337.db",
    "arty-a7-2c-improved_basic_3_20241007_122706.db",
    "arty-a7-2c-improved_large_scale_1000_20241007_123418.db",
]

# Define human-readable field names and their formatting
field_names = {
    "total_bytes_processed": ("Total Bytes Processed (Mb)", "{:.2f}"),
    "avg_bytes_per_second": ("Avg Bytes per Second (Kb/s)", "{:.2f}"),
    "test_duration": ("Test Duration (s)", "{:.2f}"),
    "avg_network_time": ("Avg Network Time (ms)", "{:.2f}"),
    "avg_processing_time": ("Avg Processing Time (ms)", "{:.2f}"),
    "avg_queue_time": ("Avg Queue Time (ms)", "{:.2f}"),
}

# Read the JSON file
with open(os.path.join("data", "test_results.json"), "r") as file:
    data = json.load(file)

# Extract the relevant configuration
config_data = data["arty-a7-2c-improved"]

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

    test_data["Improved Dual Core Tests"] = name

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
