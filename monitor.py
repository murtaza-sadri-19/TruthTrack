import psutil
import time

def monitor_usage():
    """Monitor CPU and RAM usage every second."""
    print("Monitoring resource usage... (Press Ctrl+C to stop)")

    while True:
        memory_usage = psutil.virtual_memory().used / (1024**3)  # Convert to GB
        cpu_usage = psutil.cpu_percent(interval=1)  # % usage

        print(f"Memory Usage: {memory_usage:.2f} GB | CPU Usage: {cpu_usage:.2f}%")
        time.sleep(1)  # Log every second

if __name__ == "__main__":
    monitor_usage()