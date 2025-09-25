import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Formula1_Pitstop_Data_clean.csv")

race_stats = df.groupby(["Season", "Round"]).agg(
    AvgPitStopTime=("AvgPitStopTime", "mean"),
    TotalPitStops=("TotalPitStops", "sum"),
    Drivers=("Driver", "count"),
    Laps=("Laps", "max")
).reset_index()

race_stats["AvgPitStopsPerDriver"] = race_stats["TotalPitStops"] / race_stats["Drivers"]

stats = race_stats.groupby("Laps").agg(
    AvgPitStopTime=("AvgPitStopTime", "mean"),
    AvgPitStopsPerDriver=("AvgPitStopsPerDriver", "mean")
).reset_index()

# === График 1: среднее время пит-стопа ===
plt.figure(figsize=(12, 6))
plt.plot(
    stats["Laps"], stats["AvgPitStopTime"],
    color="crimson", marker="o",
    markerfacecolor="white", markeredgecolor="black",
    markeredgewidth=2, linewidth=2, label="Среднее время пит-стопа (с)"
)
plt.grid(linewidth=2, color="mistyrose")
plt.title("Зависимость времени пит-стопа от длины гонки", fontsize=16)
plt.xlabel("Количество кругов в гонке", fontsize=14)
plt.ylabel("Среднее время пит-стопа (с)", fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("line_plot_time.png", dpi=300)
plt.show()

# === График 2: среднее число пит-стопов на гонщика ===
plt.figure(figsize=(12, 6))
plt.plot(
    stats["Laps"], stats["AvgPitStopsPerDriver"],
    color="crimson", marker="s",
    markerfacecolor="white", markeredgecolor="black",
    markeredgewidth=2, linewidth=2, label="Среднее число пит-стопов на гонщика"
)
plt.grid(linewidth=2, color="mistyrose")
plt.title("Зависимость числа пит-стопов от длины гонки", fontsize=16)
plt.xlabel("Количество кругов в гонке", fontsize=14)
plt.ylabel("Среднее число пит-стопов", fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("line_plot_stops.png", dpi=300)
plt.show()
