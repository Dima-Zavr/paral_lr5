import os
import matplotlib.pyplot as plt

from load_data import load_report


def build_adaptive_chart(csv_path, output_dir):

    df = load_report(csv_path)

    # =========================
    # ТОЛЬКО ADAPTIVE + SCENARIO C
    # =========================

    adaptive_df = df[
        (df["strategy"] == "adaptive") &
        (df["scenario"] == "C")
    ]

    # =========================
    # ИЩЕМ CONCURRENCY COLUMNS
    # =========================

    concurrency_columns = [
        col for col in adaptive_df.columns
        if "concurrency" in col
    ]

    if not concurrency_columns:

        print("No adaptive concurrency data found.")
        return

    # =========================
    # СРЕДНИЙ CONCURRENCY
    # =========================

    avg_concurrency = []

    for _, row in adaptive_df.iterrows():

        values = []

        for column in concurrency_columns:

            value = row[column]

            if not str(value) == "nan":
                values.append(value)

        if values:
            avg_concurrency.append(
                sum(values) / len(values)
            )
        else:
            avg_concurrency.append(0)

    # =========================
    # ГРАФИК
    # =========================

    plt.figure(figsize=(10, 5))

    plt.plot(
        adaptive_df["iteration"],
        avg_concurrency,
        marker="o",
        linewidth=2
    )

    plt.title(
        "Adaptive Concurrency Over Time (Scenario C)"
    )

    plt.xlabel("Iteration")
    plt.ylabel("Average Concurrency")

    plt.grid(True)

    # =========================
    # СОХРАНЕНИЕ
    # =========================

    output_path = os.path.join(
        output_dir,
        "adaptive_concurrency_C.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"Saved: {output_path}")