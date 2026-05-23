from collections import deque
from urllib.parse import urlparse


WINDOW_SIZE = 20


class APIStats:

    def __init__(self):

        self.success_history = deque(maxlen=WINDOW_SIZE)
        self.response_times = deque(maxlen=WINDOW_SIZE)

        self.current_concurrency = 3

    # =========================
    # ОБНОВЛЕНИЕ СТАТИСТИКИ
    # =========================

    def add_result(self, success: bool, elapsed_ms: int):

        self.success_history.append(success)
        self.response_times.append(elapsed_ms)

    # =========================
    # SUCCESS RATE
    # =========================

    @property
    def success_rate(self):

        if not self.success_history:
            return 1.0

        return sum(self.success_history) / len(self.success_history)

    # =========================
    # AVG RESPONSE TIME
    # =========================

    @property
    def avg_response_ms(self):

        if not self.response_times:
            return 0

        return sum(self.response_times) / len(self.response_times)

    # =========================
    # АДАПТАЦИЯ CONCURRENCY
    # =========================

    def adapt(self, global_limit: int):

        # Если API плохой → уменьшаем concurrency
        if self.success_rate < 0.7 or self.avg_response_ms > 2000:

            self.current_concurrency = max(
                1,
                self.current_concurrency - 1
            )

        # Если API хороший → увеличиваем
        elif self.success_rate > 0.95 and self.avg_response_ms < 500:

            self.current_concurrency = min(
                global_limit,
                self.current_concurrency + 1
            )


# =========================
# ГЛОБАЛЬНОЕ ХРАНИЛИЩЕ
# =========================

stats_storage = {}


def get_host(url: str):

    return urlparse(url).netloc


def get_api_stats(url: str):

    host = get_host(url)

    if host not in stats_storage:
        stats_storage[host] = APIStats()

    return stats_storage[host]


def get_all_stats():

    result = {}

    for host, stats in stats_storage.items():

        result[host] = {
            "success_rate": round(stats.success_rate, 2),
            "avg_ms": round(stats.avg_response_ms, 2),
            "adjusted_concurrency": stats.current_concurrency
        }

    return result