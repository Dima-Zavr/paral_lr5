import asyncio
import random
import time

from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/data")
async def get_data():

    start = time.perf_counter()

    # =========================
    # СЛУЧАЙНАЯ ЗАДЕРЖКА
    # =========================

    delay = random.uniform(0.1, 3)

    await asyncio.sleep(delay)

    # =========================
    # СЛУЧАЙНАЯ ОШИБКА
    # =========================

    error_probability = 0.4

    if random.random() < error_probability:

        error_code = random.choice([500, 503])

        raise HTTPException(
            status_code=error_code,
            detail=f"Simulated server error {error_code}"
        )

    elapsed_ms = int(
        (time.perf_counter() - start) * 1000
    )

    return {
        "api": "unstable",
        "status": "ok",
        "delay_ms": elapsed_ms
    }