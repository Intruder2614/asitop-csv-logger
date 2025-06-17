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
