import os
import sqlite3
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
import random


plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "Times New Roman"

# Global variables
global_processing_time = 0
global_networking_time = 0
global_total_bytes_processed = 0


def calculate_server_stats(cursor):
    global test_duration, global_processing_time, global_networking_time, total_bytes_processed

    cursor.execute("SELECT MAX(active_clients) FROM server_metrics")
    max_clients = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(cpu_usage) FROM server_metrics")
    max_cpu_usage = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(memory_usage) FROM server_metrics")
    max_memory_usage = cursor.fetchone()[0]

    cursor.execute(
        "SELECT timestamp, total_bytes_processed FROM server_metrics ORDER BY timestamp"
    )
    result = cursor.fetchall()
    timestamps = [row[0] for row in result]
    bytes_processed = [row[1] for row in result]

    start_time = timestamps[0]
    durations = [(t - start_time) for t in timestamps]
    test_duration = max(durations)

    total_bytes_processed = max(bytes_processed) - min(bytes_processed)

    # Calculate rate of change
    time_diffs = np.diff(timestamps)
    bytes_diffs = np.diff(bytes_processed)
    rates = bytes_diffs / time_diffs

    # Define a threshold for processing (you may need to adjust this)
    processing_threshold = np.mean(rates) * 0.1  # 10% of mean rate

    processing_time = sum(time_diffs[rates > processing_threshold])
    networking_time = sum(time_diffs[rates <= processing_threshold])

    # Update global variables
    global_processing_time = processing_time
    global_networking_time = networking_time

    avg_bytes_per_second = total_bytes_processed / test_duration

    return {
        "max_clients": max_clients,
        "max_cpu_usage": max_cpu_usage,
        "max_memory_usage": max_memory_usage,
        "total_bytes_processed": total_bytes_processed,
        "avg_bytes_per_second": avg_bytes_per_second,
        "test_duration": test_duration,
        "estimated_processing_time": processing_time,
        "estimated_networking_time": networking_time,
    }


def calculate_client_stats(cursor):
    cursor.execute("SELECT AVG(queue_time) FROM client_metrics")
    avg_queue_time = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM client_metrics WHERE operation_completed = 1")
    successful_operations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM client_metrics WHERE operation_completed = 0")
    failed_operations = cursor.fetchone()[0]

    return {
        "avg_queue_time": avg_queue_time,
        "successful_operations": successful_operations,
        "failed_operations": failed_operations,
    }


def process_database(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        server_stats = calculate_server_stats(cursor)
        client_stats = calculate_client_stats(cursor)

        return {**server_stats, **client_stats}


def plot_server_metrics(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, cpu_usage, memory_usage, total_bytes_processed, temperature FROM server_metrics"
        )
        data = cursor.fetchall()

    timestamps = [row[0] for row in data]
    start_time = timestamps[0]
    durations = [(t - start_time) for t in timestamps]
    cpu_usage = [row[1] for row in data]
    memory_usage = [row[2] for row in data]

    # Calculate bytes_processed by taking the difference
    total_bytes = [row[3] for row in data]
    bytes_processed = [b - total_bytes[0] for b in total_bytes]

    temperature = [row[4] for row in data]

    # Create the plot for CPU, memory, and bytes processed
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("CPU and Memory Usage (%)")
    ax1.plot(durations, cpu_usage, label="CPU Usage (%)", color="red", linewidth=1)
    ax1.plot(
        durations, memory_usage, label="Memory Usage (%)", color="blue", linewidth=1
    )
    ax1.tick_params(axis="y")
    ax1.set_ylim(0, 101)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Total Amount of Bytes Processed (bytes)")
    ax2.plot(
        durations,
        bytes_processed,
        label="Bytes Processed (bytes)",
        color="green",
        linewidth=1,
    )
    ax2.tick_params(axis="y")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.3),
        ncol=4,
    )

    # Add major and minor grid lines
    ax1.grid(True, which="major", linestyle="-", linewidth=0.5, color="#CCCCCC")
    ax1.grid(True, which="minor", linestyle=":", linewidth=0.3, color="#CCCCCC")
    ax1.minorticks_on()

    plt.tight_layout()
    # plt.subplots_adjust(bottom=0.2)
    plt.savefig(
        f"{os.path.basename(db_path)}_server_metrics.png", dpi=600, bbox_inches="tight"
    )
    plt.close()

    # Create a new plot for temperature (unchanged)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(durations, temperature, label="Temperature", color="orange", linewidth=1)
    ax.set_xlabel("Duration (seconds)")
    ax.set_ylabel("Temperature")
    ax.legend(loc="lower center")

    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_server_temperature.png", dpi=600)
    plt.close()


def plot_client_tasks(db_path):
    global test_duration, global_processing_time, global_networking_time, total_bytes_processed
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT start_time, end_time, queue_time, operation_completed, file_size FROM client_metrics ORDER BY start_time"
        )
        data = cursor.fetchall()

    start_times = [row[0] for row in data]
    end_times = [row[1] for row in data]
    overall_start = min(start_times)
    queue_times = [row[2] for row in data]
    completed = [row[3] for row in data]
    file_sizes = [row[4] for row in data]

    total_times = [end - start for end, start in zip(end_times, start_times)]

    # Calculate average time per byte for processing and networking
    avg_seconds_per_processed_byte = global_processing_time / total_bytes_processed
    avg_seconds_per_networked_byte = global_networking_time / total_bytes_processed

    # Calculate proportional processing and network times
    processing_times = [
        avg_seconds_per_processed_byte
        * (size + random.uniform(-1024 * 1024, 1024 * 1024))
        for size in file_sizes
    ]
    network_times = [avg_seconds_per_networked_byte * size for size in file_sizes]

    # Adjust times to match total_times while maintaining proportions
    for i in range(len(total_times)):
        total_estimated = processing_times[i] + network_times[i] + queue_times[i]
        if total_estimated > 0:
            scale_factor = (total_times[i] - queue_times[i]) / (
                processing_times[i] + network_times[i]
            )
            processing_times[i] *= scale_factor
            network_times[i] *= scale_factor

    # Plotting
    clients_per_row = 30
    num_rows = min(clients_per_row, len(data))
    fig_height = max(5, num_rows * 0.25)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    bar_height = 0.8

    for i, (start, queue, network, processing, complete, file_size) in enumerate(
        zip(
            start_times,
            queue_times,
            network_times,
            processing_times,
            completed,
            file_sizes,
        )
    ):
        row = (i % num_rows) + 1
        left = start - overall_start

        # Queue time
        ax.barh(
            row,
            queue,
            left=left,
            height=bar_height,
            align="center",
            color="yellow",
            alpha=0.7,
        )

        # Network time
        ax.barh(
            row,
            network,
            left=left + queue,
            height=bar_height,
            align="center",
            color="green",
            alpha=0.7,
        )

        # Processing time
        ax.barh(
            row,
            processing,
            left=left + queue + network,
            height=bar_height,
            align="center",
            color="blue",
            alpha=0.7,
        )

        # Add a red border if the operation failed
        if not complete:
            total_time = queue + network + processing
            ax.barh(
                row,
                total_time,
                left=left,
                height=bar_height,
                align="center",
                fill=False,
                edgecolor="red",
                linewidth=2,
            )

        # Add file size label
        ax.text(
            left + queue + network + processing,
            row,
            f"{file_size/1024/1024:.1f}MB",
            va="center",
            fontsize=8,
        )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"Client Number (modulo {clients_per_row})")
    ax.set_ylim(0, num_rows + 1)

    # Set x-axis to display whole numbers
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(5))

    # Adjust y-axis ticks and labels to start from 1
    ax.set_yticks(range(1, num_rows + 1))
    ax.set_yticklabels(range(1, num_rows + 1))

    # Add a legend
    handles = [
        plt.Rectangle((0, 0), 1, 1, color="yellow", alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, color="green", alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, color="blue", alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor="red", linewidth=2),
    ]
    labels = ["Queue Time", "Network Time", "Processing Time", "Failed Operation"]
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=4)

    plt.tight_layout()
    plt.savefig(
        f"{os.path.basename(db_path)}_client_tasks.png", dpi=600, bbox_inches="tight"
    )
    plt.close()


def main():
    data_dir = "data"
    results = defaultdict(dict)

    for filename in os.listdir(data_dir):
        if filename.endswith(".db"):
            db_path = os.path.join(data_dir, filename)
            test_type = filename.split("_")[0]

            stats = process_database(db_path)
            results[test_type][filename] = stats

            # Create plots for each database
            plot_server_metrics(db_path)
            plot_client_tasks(db_path)

    # Print or save the results
    print(json.dumps(results, indent=2))

    # Optionally, save to a file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
