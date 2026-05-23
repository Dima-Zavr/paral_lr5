import json
import os
import pandas as pd


def save_reports(results, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    # =========================
    # JSON
    # =========================

    json_path = os.path.join(
        output_dir,
        "report.json"
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # =========================
    # CSV
    # =========================

    rows = []

    for item in results:

        row = {
            "scenario": item["scenario"],
            "strategy": item["strategy"],
            "iteration": item["iteration"],
            "successful": item["metrics"]["successful"],
            "failed": item["metrics"]["failed"],
            "timeouts": item["metrics"]["timeouts"],
            "total_time_ms": item["metrics"]["total_time_ms"]
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    csv_path = os.path.join(
        output_dir,
        "report.csv"
    )

    df.to_csv(csv_path, index=False)

    print(f"Reports saved to: {output_dir}")