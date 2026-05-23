import asyncio
import time
import uuid

import aiohttp
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()


# =========================
# МОДЕЛИ ЗАПРОСА/ОТВЕТА
# =========================

class AggregateRequest(BaseModel):
    urls: List[str]
    strategy: Optional[str] = "fixed"
    max_concurrent: Optional[int] = 3
    timeout_sec: Optional[int] = 5


# =========================
# ФУНКЦИЯ ОТПРАВКИ ЗАПРОСА
# =========================

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


# =========================
# ENDPOINT АГРЕГАЦИИ
# =========================

@app.post("/aggregate")
async def aggregate(request: AggregateRequest):

    request_id = str(uuid.uuid4())

    total_start = time.perf_counter()

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch_url(session, url, request.timeout_sec)
            for url in request.urls
        ]

        results = await asyncio.gather(*tasks)

    total_time_ms = int((time.perf_counter() - total_start) * 1000)

    successful = sum(1 for r in results if r.get("status") == 200)
    failed = len(results) - successful

    return {
        "request_id": request_id,
        "results": results,
        "summary": {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "total_time_ms": total_time_ms,
            "strategy_used": request.strategy,
            "concurrent_used": len(request.urls)
        }
    }