# asitop-csv

*Because sometimes you want your Apple Silicon metrics in spreadsheet form, not just pretty terminal colors.*

A CSV-logging fork of the excellent [`asitop`](https://github.com/tlkh/asitop) - a Python-based `nvtop`-inspired command line tool for Apple Silicon Macs. While the original `asitop` gives you beautiful real-time terminal output, this fork saves all that juicy performance data to CSV files for easy analysis with pandas, Excel, or your favorite data visualization tools.

## What's Different?

Instead of just displaying metrics in your terminal (though it still does that), this fork **logs everything to CSV files** so you can:
- Create custom visualizations with matplotlib/seaborn
- Perform deep analysis with pandas
- Build dashboards in Jupyter notebooks  
- Track performance trends over time
- Generate reports for system optimization

Perfect for developers, researchers, and data nerds who want to understand their Apple Silicon performance patterns beyond the moment.

## Features

All the goodness of the original `asitop`, plus CSV logging:

### **Utilization Metrics (Now in CSV!)**
- CPU utilization (E-cluster and P-cluster)
- GPU utilization and frequency
- ANE (Apple Neural Engine) utilization
- All timestamped for trend analysis

### **Memory Metrics (Spreadsheet Ready)**
- RAM and swap usage over time
- Memory pressure indicators
- Perfect for identifying memory bottlenecks

### **Power Metrics (Chart-Friendly)**
- CPU and GPU power consumption
- Peak power tracking
- Rolling averages for smooth trend lines
- Great for battery life optimization studies

## Installation

Same as the original - you'll need `pip` and Python (which macOS already has):

```bash
pip install asitop-csv
# or if you're installing from source
pip install -e .
```

## Usage

### Basic CSV Logging
```bash
# Start logging to CSV (recommended - enter password upfront)
sudo asitop-csv

# Or let it prompt for password
asitop-csv
```

### Advanced Options
```bash
asitop-csv [-h] [--interval INTERVAL] [--color COLOR] [--avg AVG] [--output OUTPUT] [--no-display]

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL   Display interval and sampling interval (seconds, default: 1)
  --color COLOR         Choose display color (0~8, default: 2)
  --avg AVG            Interval for averaged values (seconds, default: 30)
  --output OUTPUT      CSV output directory (default: ./asitop_logs/)
  --no-display        Disable terminal output, CSV logging only
```

### Pro Tips

**Long-term monitoring:**
```bash
# Run in background, log every 5 seconds, no terminal spam
sudo asitop-csv --interval 5 --no-display --output ~/Desktop/my_mac_stats/
```

**Benchmark session:**
```bash
# High-frequency logging during testing
sudo asitop-csv --interval 0.5 --output ./benchmark_$(date +%Y%m%d_%H%M%S)/
```

## CSV Output Format

Your data gets saved in timestamped CSV files:
```
asitop_logs/
├── asitop_20241216_143022.csv
├── asitop_20241216_150315.csv
└── ...
```

Each CSV contains columns like:
- `timestamp` - When the measurement was taken
- `cpu_util_total` - Overall CPU utilization %
- `cpu_util_ecores` - Efficiency cores utilization %
- `cpu_util_pcores` - Performance cores utilization %
- `gpu_util` - GPU utilization %
- `cpu_power` - CPU power consumption (W)
- `gpu_power` - GPU power consumption (W)
- `memory_used` - RAM usage (GB)
- `memory_pressure` - Memory pressure indicator
- And much more...

## Quick Analysis with Pandas

This fork includes built-in pandas integration for easy visualization and analysis:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("asitop_metrics.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
sns.set(style="whitegrid")
metrics_to_plot = [
    "E-CPU Usage (%)", "P-CPU Usage (%)",
    "GPU Usage (%)", "RAM Used (GB)", "Swap Used (GB)",
    "CPU Power (W)", "GPU Power (W)", "Package Power (W)",
    "E-CPU Freq (MHz)", "P-CPU Freq (MHz)", "GPU Freq (MHz)"
]
for col in metrics_to_plot:
    plt.figure(figsize=(12, 4))
    sns.lineplot(data=df, x="timestamp", y=col)
    plt.title(col + " Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel(col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{col.replace(' ', '_').replace('(', '').replace(')', '')}.png")
    plt.close()
    
print(" graphs saved as ")

```

The tool automatically generates several common visualizations using pandas and matplotlib, including:
- CPU and GPU utilization trends
- Power consumption patterns
- Memory usage over time
- Temperature correlations
- Performance efficiency metrics

## How It Works

Same underlying tech as the original `asitop`:
- `powermetrics` for CPU/GPU/ANE metrics (requires `sudo`)
- `psutil` for memory and swap stats
- `sysctl` for system information
- `system_profiler` for hardware details

**Plus:** Custom CSV writer that timestamps and saves all metrics without impacting performance.

## Why This Fork?

The original `asitop` is fantastic for real-time monitoring, but sometimes you need the data for:
- Performance regression analysis
- Battery optimization studies  
- Workload characterization
- Custom dashboard creation
- Academic research
- Debugging performance issues

This fork gives you the best of both worlds - live monitoring AND historical data analysis.

## Requirements

- Apple Silicon Mac (M1, M1 Pro, M1 Max, M1 Ultra, M2, M2 Pro, M2 Max, etc.)
- macOS Monterey or later
- Python 3.6+
- `sudo` access (because `powermetrics` needs it)

## Contributing

Found a bug? Want to add a feature? PRs welcome! This is a community-driven fork focused on making Apple Silicon performance data more accessible for analysis.

## License

Same as the original `asitop` - because we're standing on the shoulders of giants.

## Credits

Huge thanks to [@tlkh](https://github.com/tlkh) for creating the original `asitop`. This fork simply adds CSV logging capabilities to their excellent work.

## Disclaimers

Just like the original: "I did this randomly don't blame me if it fried your new MacBook or something." 

But seriously, this tool only *reads* performance metrics - it doesn't change any system settings. The biggest risk is filling up your disk with CSV files if you forget to stop it.

---

*Happy monitoring! May your CPU temps be low and your GPU utilization be high.*
