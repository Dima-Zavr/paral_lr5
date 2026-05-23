import os
import matplotlib.pyplot as plt

from load_data import load_report


def build_success_chart(csv_path, output_dir):

    df = load_report(csv_path)

    grouped = (
        df.groupby("strategy")
        [["successful", "failed"]]
        .sum()
    )

    grouped.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title(
        "Successful vs Failed Requests"
    )

    plt.xlabel("Strategy")
    plt.ylabel("Requests Count")

    output_path = os.path.join(
        output_dir,
        "success_vs_failed.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"Saved: {output_path}")