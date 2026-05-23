import os
import matplotlib.pyplot as plt

from load_data import load_report


def build_avg_time_chart(csv_path, output_dir):

    df = load_report(csv_path)

    # =========================
    # СРЕДНЕЕ ВРЕМЯ
    # =========================

    grouped = (
        df.groupby(["scenario", "strategy"])
        ["total_time_ms"]
        .mean()
        .reset_index()
    )

    scenarios = ["A", "B", "C"]

    strategies = [
        "fixed",
        "timeout_race",
        "adaptive"
    ]

    plt.figure(figsize=(10, 6))

    # =========================
    # ЛИНИЯ ДЛЯ КАЖДОЙ СТРАТЕГИИ
    # =========================

    for strategy in strategies:

        strategy_data = grouped[
            grouped["strategy"] == strategy
        ]

        y_values = []

        for scenario in scenarios:

            row = strategy_data[
                strategy_data["scenario"] == scenario
            ]

            if not row.empty:
                y_values.append(
                    row["total_time_ms"].values[0]
                )
            else:
                y_values.append(0)

        plt.plot(
            scenarios,
            y_values,
            marker="o",
            linewidth=2,
            label=strategy
        )

    # =========================
    # ОФОРМЛЕНИЕ
    # =========================

    plt.title(
        "Average Execution Time by Strategy"
    )

    plt.xlabel("Scenario")
    plt.ylabel("Average Time (ms)")

    plt.legend()

    plt.grid(True)

    # =========================
    # СОХРАНЕНИЕ
    # =========================

    output_path = os.path.join(
        output_dir,
        "avg_time_comparison.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"Saved: {output_path}")