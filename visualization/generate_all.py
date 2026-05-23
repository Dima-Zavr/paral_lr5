import os

from avg_time_chart import (
    build_avg_time_chart
)

from adaptive_chart import (
    build_adaptive_chart
)

from success_chart import (
    build_success_chart
)


CSV_PATH = "reports/report.csv"

OUTPUT_DIR = "reports/graphs"


def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    build_avg_time_chart(
        CSV_PATH,
        OUTPUT_DIR
    )

    build_adaptive_chart(
        CSV_PATH,
        OUTPUT_DIR
    )

    build_success_chart(
        CSV_PATH,
        OUTPUT_DIR
    )

    print("\nAll graphs generated.")


if __name__ == "__main__":
    main()