import os
import sqlite3
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def calculate_server_stats(cursor):
    cursor.execute("SELECT MAX(active_clients) FROM server_metrics")
    max_clients = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(cpu_usage) FROM server_metrics")
    max_cpu_usage = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(memory_usage) FROM server_metrics")
    max_memory_usage = cursor.fetchone()[0]

    cursor.execute(
        "SELECT MIN(total_bytes_processed), MAX(total_bytes_processed) FROM server_metrics"
    )
    result = cursor.fetchone()
    if result:
        min_bytes, max_bytes = result
        total_bytes_processed = max_bytes - min_bytes
    else:
        total_bytes_processed = 0

    cursor.execute("SELECT AVG(bytes_processed_per_second) FROM server_metrics")
    avg_bytes_per_second = cursor.fetchone()[0]

    cursor.execute(("SELECT timestamp FROM server_metrics"))
    timestamp_col = cursor.fetchall()
    timestamps = [row[0] for row in timestamp_col]

    start_time = timestamps[0]
    durations = [(t - start_time) for t in timestamps]

    return {
        "max_clients": max_clients,
        "max_cpu_usage": max_cpu_usage,
        "max_memory_usage": max_memory_usage,
        "total_bytes_processed": total_bytes_processed,
        "avg_bytes_per_second": avg_bytes_per_second,
        "test_duration": max(durations),
    }


def calculate_client_stats(cursor):
    cursor.execute("SELECT AVG(network_time) FROM client_metrics")
    avg_network_time = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(processing_time) FROM client_metrics")
    avg_processing_time = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(queue_time) FROM client_metrics")
    avg_queue_time = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM client_metrics WHERE operation_completed = 1")
    successful_operations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM client_metrics WHERE operation_completed = 0")
    failed_operations = cursor.fetchone()[0]

    return {
        "avg_network_time": avg_network_time,
        "avg_processing_time": avg_processing_time,
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
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Duration (seconds)")
    ax1.set_ylabel("Usage (%)")
    ax1.plot(durations, cpu_usage, label="CPU Usage", color="red")
    ax1.plot(durations, memory_usage, label="Memory Usage", color="blue")
    ax1.tick_params(axis="y")
    ax1.set_ylim(0, 100)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Bytes Processed")
    ax2.plot(durations, bytes_processed, label="Bytes Processed", color="green")
    ax2.tick_params(axis="y")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Server Metrics Over Time")
    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_server_metrics.png")
    plt.close()

    # Create a new plot for temperature (unchanged)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(durations, temperature, label="Temperature", color="orange")
    ax.set_xlabel("Duration (seconds)")
    ax.set_ylabel("Temperature")
    ax.set_title("Server Temperature Over Time")
    ax.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_server_temperature.png")
    plt.close()


def plot_client_tasks(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT start_time, end_time, queue_time, network_time, processing_time, operation_completed, file_size FROM client_metrics ORDER BY start_time"
        )
        data = cursor.fetchall()

    start_times = [row[0] for row in data]
    overall_start = min(start_times)
    queue_times = [row[2] for row in data]
    network_times = [row[3] for row in data]
    processing_times = [row[4] for row in data]
    completed = [row[5] for row in data]
    file_sizes = [row[6] for row in data]

    # Adjust figure size based on number of clients
    fig_height = max(8, len(data) * 0.25)  # Minimum height of 8 inches
    fig, ax = plt.subplots(figsize=(15, fig_height))

    bar_height = 0.8  # Increase bar height to reduce padding

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
        left = start - overall_start
        total_time = queue + network + processing

        # Queue time
        ax.barh(
            i,
            queue,
            left=left,
            height=bar_height,
            align="center",
            color="yellow",
            alpha=0.7,
        )

        # Network time
        ax.barh(
            i,
            network,
            left=left + queue,
            height=bar_height,
            align="center",
            color="green",
            alpha=0.7,
        )

        # Processing time
        ax.barh(
            i,
            processing,
            left=left + queue + network,
            height=bar_height,
            align="center",
            color="blue",
            alpha=0.7,
        )

        # Add a red border if the operation failed
        if not complete:
            ax.barh(
                i,
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
            left + total_time + 0.5,
            i,
            f"{file_size/1024/1024:.1f} MB",
            va="center",
            fontsize=8,
        )

    ax.set_xlabel("Seconds")
    ax.set_ylabel("Tasks")
    ax.set_title("Client Task Timeline")
    ax.set_ylim(-1, len(data))

    # Adjust y-axis tick labels
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(range(1, len(data) + 1))

    # Add a legend
    ax.barh(0, 0, color="yellow", alpha=0.7, label="Queue Time")
    ax.barh(0, 0, color="green", alpha=0.7, label="Network Time")
    ax.barh(0, 0, color="blue", alpha=0.7, label="Processing Time")
    ax.barh(0, 0, fill=False, edgecolor="red", linewidth=2, label="Failed Operation")
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_client_tasks.png", dpi=300)
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
