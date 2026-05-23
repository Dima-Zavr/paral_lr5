import asyncio
import random
import time

from fastapi import FastAPI


app = FastAPI()


@app.get("/data")
async def get_data():

    start = time.perf_counter()

    # Медленный API
    delay = random.uniform(3, 5)

    await asyncio.sleep(delay)

    elapsed_ms = int(
        (time.perf_counter() - start) * 1000
    )

    return {
        "api": "slow",
        "status": "ok",
        "delay_ms": elapsed_ms
    }