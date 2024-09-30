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

    cursor.execute("SELECT MAX(total_bytes_processed) FROM server_metrics")
    total_bytes_processed = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(bytes_processed_per_second) FROM server_metrics")
    avg_bytes_per_second = cursor.fetchone()[0]

    return {
        "max_clients": max_clients,
        "max_cpu_usage": max_cpu_usage,
        "max_memory_usage": max_memory_usage,
        "total_bytes_processed": total_bytes_processed,
        "avg_bytes_per_second": avg_bytes_per_second,
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
            "SELECT timestamp, cpu_usage, memory_usage, bytes_processed_per_second FROM server_metrics"
        )
        data = cursor.fetchall()

    timestamps = [row[0] for row in data]
    start_time = timestamps[0]
    durations = [(t - start_time) for t in timestamps]
    cpu_usage = [row[1] for row in data]
    memory_usage = [row[2] for row in data]
    bytes_per_second = [row[3] for row in data]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Duration (seconds)")
    ax1.set_ylabel("Usage (%)")
    ax1.plot(durations, cpu_usage, label="CPU Usage", color="red")
    ax1.plot(durations, memory_usage, label="Memory Usage", color="blue")
    ax1.tick_params(axis="y")
    ax1.set_ylim(0, 100)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Bytes Processed per Second")
    ax2.plot(durations, bytes_per_second, label="Bytes/Second", color="green")
    ax2.tick_params(axis="y")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Server Metrics Over Time")
    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_server_metrics.png")
    plt.close()


def plot_client_tasks(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT start_time, end_time, queue_time, network_time, processing_time, operation_completed FROM client_metrics ORDER BY start_time"
        )
        data = cursor.fetchall()

    start_times = [row[0] for row in data]
    overall_start = min(start_times)
    queue_times = [row[2] for row in data]
    network_times = [row[3] for row in data]
    processing_times = [row[4] for row in data]
    completed = [row[5] for row in data]

    fig, ax = plt.subplots(figsize=(15, 10))

    for i, (start, queue, network, processing, complete) in enumerate(
        zip(start_times, queue_times, network_times, processing_times, completed)
    ):
        left = start - overall_start

        # Queue time
        ax.barh(
            i, queue, left=left, height=0.5, align="center", color="yellow", alpha=0.7
        )

        # Network time
        ax.barh(
            i,
            network,
            left=left + queue,
            height=0.5,
            align="center",
            color="green",
            alpha=0.7,
        )

        # Processing time
        ax.barh(
            i,
            processing,
            left=left + queue + network,
            height=0.5,
            align="center",
            color="blue",
            alpha=0.7,
        )

        # Add a red border if the operation failed
        if not complete:
            ax.barh(
                i,
                queue + network + processing,
                left=left,
                height=0.5,
                align="center",
                fill=False,
                edgecolor="red",
                linewidth=2,
            )

    ax.set_xlabel("Seconds")
    ax.set_ylabel("Tasks")
    ax.set_title("Client Task Timeline")
    ax.set_ylim(-1, len(data))

    # Add a legend
    ax.barh(0, 0, color="yellow", alpha=0.7, label="Queue Time")
    ax.barh(0, 0, color="green", alpha=0.7, label="Network Time")
    ax.barh(0, 0, color="blue", alpha=0.7, label="Processing Time")
    ax.barh(0, 0, fill=False, edgecolor="red", linewidth=2, label="Failed Operation")
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(f"{os.path.basename(db_path)}_client_tasks.png")
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
