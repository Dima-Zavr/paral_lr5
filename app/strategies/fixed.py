import asyncio
import aiohttp

from app.services.fetcher import fetch_url


async def fixed_strategy(urls, max_concurrent, timeout_sec):

    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(session, url):

        async with semaphore:
            return await fetch_url(session, url, timeout_sec)

    async with aiohttp.ClientSession() as session:

        tasks = [
            limited_fetch(session, url)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

    return results