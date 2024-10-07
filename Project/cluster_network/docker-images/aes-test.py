import subprocess
import cProfile
import io
import pstats
import time
import psutil
import os


def process_data(data, operation, is_last_chunk):
    key = "00" * 16
    iv = "00" * 16

    if operation == "encrypt":
        cmd = ["openssl", "enc", "-aes-128-cbc", "-K", key, "-iv", iv, "-nosalt"]
        if not is_last_chunk:
            cmd.append("-nopad")
    else:  # decrypt
        cmd = ["openssl", "enc", "-d", "-aes-128-cbc", "-K", key, "-iv", iv, "-nosalt"]
        if not is_last_chunk:
            cmd.append("-nopad")

    p = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(input=data)

    if p.returncode != 0:
        raise Exception(f"OpenSSL error: {stderr.decode()}")

    return stdout


def run_encryption_test():
    # Generate 50MB of random data
    data = os.urandom(50 * 1024 * 1024)

    # Encrypt the data
    start_time = time.time()
    encrypted_data = process_data(data, "encrypt", True)
    end_time = time.time()

    print(f"Encryption time: {end_time - start_time:.2f} seconds")
    return encrypted_data


def main():
    # CPU and memory usage monitoring
    process = psutil.Process(os.getpid())
    start_cpu_times = process.cpu_times()
    start_memory = process.memory_info().rss / 1024 / 1024  # in MB

    # Run and profile the encryption test
    pr = cProfile.Profile()
    pr.enable()
    encrypted_data = run_encryption_test()
    pr.disable()

    # CPU and memory usage after test
    end_cpu_times = process.cpu_times()
    end_memory = process.memory_info().rss / 1024 / 1024  # in MB

    # Print CPU and memory usage
    print(f"CPU time (user): {end_cpu_times.user - start_cpu_times.user:.2f} seconds")
    print(
        f"CPU time (system): {end_cpu_times.system - start_cpu_times.system:.2f} seconds"
    )
    print(f"Memory usage: {end_memory - start_memory:.2f} MB")

    # Print cProfile results
    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())


if __name__ == "__main__":
    main()
