import asyncio
import aiohttp

from app.services.fetcher import fetch_url
from app.services.stats_manager import get_api_stats


async def adaptive_strategy(
    urls,
    initial_concurrent,
    timeout_sec
):

    async with aiohttp.ClientSession() as session:

        results = []

        # =========================
        # ГРУППИРУЕМ URL ПО HOST
        # =========================

        grouped = {}

        for url in urls:

            stats = get_api_stats(url)

            host = url.split("/")[2]

            if host not in grouped:
                grouped[host] = {
                    "urls": [],
                    "stats": stats
                }

            grouped[host]["urls"].append(url)

        # =========================
        # ОБРАБАТЫВАЕМ КАЖДЫЙ HOST
        # =========================

        for host_data in grouped.values():

            stats = host_data["stats"]

            # Берём адаптивное concurrency
            concurrency = stats.current_concurrency

            semaphore = asyncio.Semaphore(concurrency)

            async def limited_fetch(url):

                async with semaphore:

                    result = await fetch_url(
                        session,
                        url,
                        timeout_sec
                    )

                    success = result.get("status") == 200

                    elapsed_ms = result.get(
                        "elapsed_ms",
                        timeout_sec * 1000
                    )

                    # Обновляем статистику
                    stats.add_result(
                        success,
                        elapsed_ms
                    )

                    return result

            tasks = [
                limited_fetch(url)
                for url in host_data["urls"]
            ]

            host_results = await asyncio.gather(*tasks)

            results.extend(host_results)

            # =========================
            # АДАПТАЦИЯ
            # =========================

            stats.adapt(initial_concurrent)

    return results