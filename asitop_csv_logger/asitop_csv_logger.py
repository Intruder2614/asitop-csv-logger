import argparse
import time
import csv
import threading
import os
import sys
from collections import deque
from .utils import run_powermetrics_process, parse_powermetrics, get_soc_info, get_ram_metrics_dict

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
    parser = argparse.ArgumentParser(description="ASITOP CSV Logger - Log Apple Silicon powermetrics to CSV")
    parser.add_argument("--interval", type=int, default=1, help="Sampling interval in seconds (default: 1)")
    parser.add_argument("--output", type=str, help="Path to output directory (default: ~/asitop_logs)")
    args = parser.parse_args()

    interval = args.interval
    output_dir = os.path.abspath(os.path.expanduser(args.output)) if args.output else os.path.expanduser("~/asitop_logs")

    timestamp = int(time.time())
    output_path = os.path.join(output_dir, f"asitop_metrics_{timestamp}.csv")

    try:
        os.makedirs(output_dir, exist_ok=True)
        print("Starting ASITOP CSV Logger with manual start/stop...")
        soc_info = get_soc_info()
        ane_max_power = 8.0

        timecode = str(timestamp)
        pm_process = run_powermetrics_process(timecode, interval=interval * 1000)

        threading.Thread(target=wait_for_enter_start).start()
        while not running:
            time.sleep(0.1)

        print(f"Logging to: {output_path}")
        threading.Thread(target=wait_for_enter_stop).start()

        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)

            while running:
                result = parse_powermetrics(timecode=timecode)
                if not result:
                    time.sleep(interval)
                    continue

                cpu_data, gpu_data, thermal_state, _, timestamp = result
                ram_data = get_ram_metrics_dict()

                ane_power = cpu_data["ane_W"] / interval
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
                    cpu_data["cpu_W"] / interval,
                    cpu_data["gpu_W"] / interval,
                    ane_power,
                    cpu_data["package_W"] / interval,
                    thermal_state
                ]

                writer.writerow(row)
                time.sleep(interval)

        print(f"\n CSV logging stopped. Output saved to: {output_path}")

    except KeyboardInterrupt:
        print("\n Interrupted. Stopping logging...")
        sys.exit(0)
    except PermissionError:
        print(f"\n Permission denied for writing to: {output_path}")
        sys.exit(1)
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        sys.exit(1)
    finally:
        if 'pm_process' in locals():
            pm_process.terminate()

if __name__ == "__main__":
    main()