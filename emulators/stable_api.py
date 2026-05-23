import asyncio
import random
import time

from fastapi import FastAPI


app = FastAPI()


@app.get("/data")
async def get_data():

    start = time.perf_counter()

    # Быстрый ответ
    delay = random.uniform(0.05, 0.2)

    await asyncio.sleep(delay)

    elapsed_ms = int(
        (time.perf_counter() - start) * 1000
    )

    return {
        "api": "stable",
        "status": "ok",
        "delay_ms": elapsed_ms
    }