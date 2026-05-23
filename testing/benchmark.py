import asyncio
import aiohttp

from testing.scenarios import SCENARIOS
from testing.metrics import calculate_metrics


STRATEGIES = [
    "fixed",
    "timeout_race",
    "adaptive"
]


async def send_request(payload):

    async with aiohttp.ClientSession() as session:

        async with session.post(
            "http://127.0.0.1:8000/aggregate",
            json=payload
        ) as response:

            return await response.json()


async def run_benchmark(
    scenario_name,
    repeats
):

    scenario_urls = SCENARIOS[scenario_name]

    all_results = []

    for strategy in STRATEGIES:

        print(f"\nStrategy: {strategy}")

        for iteration in range(repeats):

            payload = {
                "urls": scenario_urls,
                "strategy": strategy,
                "max_concurrent": 3,
                "timeout_sec": 2
            }

            response_data = await send_request(payload)

            metrics = calculate_metrics(
                response_data
            )

            benchmark_result = {
                "scenario": scenario_name,
                "strategy": strategy,
                "iteration": iteration + 1,
                "metrics": metrics
            }

            # adaptive stats
            if "adaptive_stats" in response_data:

                benchmark_result["adaptive_stats"] = (
                    response_data["adaptive_stats"]
                )

            all_results.append(
                benchmark_result
            )

            print(
                f"Run {iteration + 1}: "
                f"{metrics['total_time_ms']} ms | "
                f"success={metrics['successful']} | "
                f"timeouts={metrics['timeouts']}"
            )

            await asyncio.sleep(0.5)

    return all_results