import asyncio
import aiohttp

from app.services.fetcher import fetch_url


async def timeout_race_strategy(urls, timeout_sec):

    async with aiohttp.ClientSession() as session:

        tasks = [
            asyncio.create_task(
                fetch_url(session, url, timeout_sec)
            )
            for url in urls
        ]

        done, pending = await asyncio.wait(
            tasks,
            timeout=timeout_sec
        )

        results = []

        # Завершённые задачи
        for task in done:
            results.append(task.result())

        # Отменяем зависшие задачи
        for task in pending:
            task.cancel()

            results.append({
                "url": "unknown",
                "timeout": True,
                "elapsed_ms": timeout_sec * 1000
            })

    return results