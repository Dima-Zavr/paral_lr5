import argparse
import asyncio

from testing.benchmark import run_benchmark
from testing.report_saver import save_reports


async def run_tests(args):

    scenarios = ["A", "B", "C"]

    if args.scenario != "all":
        scenarios = [args.scenario]

    all_results = []

    for scenario in scenarios:

        print(f"\n====================")
        print(f"SCENARIO {scenario}")
        print(f"====================")

        results = await run_benchmark(
            scenario_name=scenario,
            repeats=args.repeats
        )

        all_results.extend(results)

    save_reports(
        all_results,
        args.output
    )


def main():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    # =========================
    # TEST COMMAND
    # =========================

    test_parser = subparsers.add_parser("test")

    test_parser.add_argument(
        "--scenario",
        default="all"
    )

    test_parser.add_argument(
        "--repeats",
        type=int,
        default=5
    )

    test_parser.add_argument(
        "--output",
        default="reports"
    )

    args = parser.parse_args()

    if args.command == "test":
        asyncio.run(run_tests(args))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()