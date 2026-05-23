import time
import uuid

from app.strategies.adaptive import adaptive_strategy
from app.services.stats_manager import get_all_stats

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.strategies.fixed import fixed_strategy
from app.strategies.timeout_race import timeout_race_strategy


app = FastAPI()


# =========================
# МОДЕЛЬ ЗАПРОСА
# =========================

class AggregateRequest(BaseModel):
    urls: List[str]
    strategy: Optional[str] = "fixed"
    max_concurrent: Optional[int] = 3
    timeout_sec: Optional[int] = 5


# =========================
# ENDPOINT
# =========================

@app.post("/aggregate")
async def aggregate(request: AggregateRequest):

    request_id = str(uuid.uuid4())

    total_start = time.perf_counter()

    # =========================
    # FIXED
    # =========================

    if request.strategy == "fixed":

        results = await fixed_strategy(
            urls=request.urls,
            max_concurrent=request.max_concurrent,
            timeout_sec=request.timeout_sec
        )

    # =========================
    # TIMEOUT RACE
    # =========================

    elif request.strategy == "timeout_race":

        results = await timeout_race_strategy(
            urls=request.urls,
            timeout_sec=request.timeout_sec
        )

    # =========================
    # ADAPTIVE
    # =========================

    elif request.strategy == "adaptive":

        results = await adaptive_strategy(
            urls=request.urls,
            initial_concurrent=request.max_concurrent,
            timeout_sec=request.timeout_sec
        )

    else:

        raise HTTPException(
            status_code=400,
            detail=f"Unknown strategy: {request.strategy}"
        )

    # =========================
    # SUMMARY
    # =========================

    total_time_ms = int(
        (time.perf_counter() - total_start) * 1000
    )

    successful = sum(
        1 for r in results
        if r.get("status") == 200
    )

    failed = len(results) - successful

    response = {
        "request_id": request_id,
        "results": results,
        "summary": {
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "total_time_ms": total_time_ms,
            "strategy_used": request.strategy,
            "concurrent_used": request.max_concurrent
        }
    }

    # Только для adaptive
    if request.strategy == "adaptive":

        response["adaptive_stats"] = get_all_stats()

    return response