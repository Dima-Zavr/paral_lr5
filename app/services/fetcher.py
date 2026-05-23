import asyncio
import time
import aiohttp


async def fetch_url(session: aiohttp.ClientSession, url: str, timeout_sec: int):
    start_time = time.perf_counter()

    try:
        async with session.get(url, timeout=timeout_sec) as response:

            elapsed_ms = int((time.perf_counter() - start_time) * 1000)

            try:
                data = await response.json()
            except:
                data = await response.text()

            return {
                "url": url,
                "status": response.status,
                "data": data,
                "elapsed_ms": elapsed_ms
            }

    except asyncio.TimeoutError:

        elapsed_ms = int((time.perf_counter() - start_time) * 1000)

        return {
            "url": url,
            "timeout": True,
            "elapsed_ms": elapsed_ms
        }

    except Exception as e:

        elapsed_ms = int((time.perf_counter() - start_time) * 1000)

        return {
            "url": url,
            "error": str(e),
            "elapsed_ms": elapsed_ms
        }