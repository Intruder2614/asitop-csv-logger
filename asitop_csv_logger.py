


import time
import csv
import threading
from collections import deque
from utils import run_powermetrics_process, parse_powermetrics, get_soc_info, get_ram_metrics_dict


SAMPLE_INTERVAL_SECONDS = 1
OUTPUT_CSV = "asitop_metrics.csv"


csv_headers = [
    "timestamp",
    "E-CPU Usage (%)",
    "P-CPU Usage (%)",
    "E-CPU Freq (MHz)",
    "P-CPU Freq (MHz)",
    "GPU Usage (%)",
    "GPU Freq (MHz)",
    "ANE Usage (%)",
    "RAM Used (GB)",
    "RAM Total (GB)",
    "Swap Used (GB)",
    "CPU Power (W)",
    "GPU Power (W)",
    "ANE Power (W)",
    "Package Power (W)",
    "Thermal Pressure"
]


running = False

def wait_for_enter_start():
    input("\nPress ENTER to START logging...")
    global running
    running = True

def wait_for_enter_stop():
    input("\nPress ENTER to STOP logging...")
    global running
    running = False


def main():
    print("Starting ASITOP CSV Logger with manual start/stop...")
    soc_info = get_soc_info()
    cpu_max_power = soc_info["cpu_max_power"]
    gpu_max_power = soc_info["gpu_max_power"]
    ane_max_power = 8.0

    timecode = str(int(time.time()))
    pm_process = run_powermetrics_process(timecode, interval=SAMPLE_INTERVAL_SECONDS * 1000)

    
    threading.Thread(target=wait_for_enter_start).start()
    while not running:
        time.sleep(0.1)

    print("Logging to:", OUTPUT_CSV)

    
    threading.Thread(target=wait_for_enter_stop).start()

    with open(OUTPUT_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        while running:
            result = parse_powermetrics(timecode=timecode)
            if not result:
                time.sleep(SAMPLE_INTERVAL_SECONDS)
                continue

            cpu_data, gpu_data, thermal_state, _, timestamp = result
            ram_data = get_ram_metrics_dict()

            ane_power = cpu_data["ane_W"] / SAMPLE_INTERVAL_SECONDS
            ane_usage_percent = int((ane_power / ane_max_power) * 100)

            row = [
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                cpu_data["E-Cluster_active"],
                cpu_data["P-Cluster_active"],
                cpu_data["E-Cluster_freq_Mhz"],
                cpu_data["P-Cluster_freq_Mhz"],
                gpu_data["active"],
                gpu_data["freq_MHz"],
                ane_usage_percent,
                ram_data["used_GB"],
                ram_data["total_GB"],
                ram_data["swap_used_GB"],
                cpu_data["cpu_W"] / SAMPLE_INTERVAL_SECONDS,
                cpu_data["gpu_W"] / SAMPLE_INTERVAL_SECONDS,
                ane_power,
                cpu_data["package_W"] / SAMPLE_INTERVAL_SECONDS,
                thermal_state
            ]

            writer.writerow(row)
            time.sleep(SAMPLE_INTERVAL_SECONDS)

    pm_process.terminate()
    print("\n CSV logging stopped. Output saved to:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
