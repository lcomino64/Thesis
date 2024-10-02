import os
import subprocess

# Raspberry Pi IPs
PI_IPS = ["192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14"]

# Files to transfer
FILES = [
    ("client/client.py", "~/client"),
    ("client/generate_testfiles.sh", "~/client"),
    ("client/wait-for-command.py", "~/client"),
    ("server/server.py", "~/server"),  # For when we test the server on a Pi
]

# SSH username
USERNAME = "user"


def transfer_file(file_path, destination, pi_ip):
    scp_command = f"scp {file_path} {USERNAME}@{pi_ip}:{destination}"
    try:
        subprocess.run(scp_command, check=True, shell=True)
        print(f"Successfully transferred {file_path} to {pi_ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to transfer {file_path} to {pi_ip}. Error: {e}")


def main():
    for pi_ip in PI_IPS:
        print(f"\nTransferring files to {pi_ip}...")
        for file_path, destination in FILES:
            transfer_file(file_path, destination, pi_ip)

        # Generate test files on each Pi
        print(f"Generating test files on {pi_ip}...")
        ssh_command = f'ssh {USERNAME}@{pi_ip} "chmod +x ~/generate_testfiles.sh && ~/generate_testfiles.sh"'
        try:
            subprocess.run(ssh_command, check=True, shell=True)
            print(f"Successfully generated test files on {pi_ip}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate test files on {pi_ip}. Error: {e}")


if __name__ == "__main__":
    main()
