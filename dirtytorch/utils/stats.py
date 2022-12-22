# short_desc: helper for calculating score and time, etc...
from dataclasses import dataclass
from time import perf_counter


@dataclass
class AverageStatistic:
    acc: float = 0
    count: int = 0
    mean: float = 0

    def summarize(self):
        if self.count == 0:
            return self.mean
        mean = self.acc / self.count
        self.mean = (self.mean + mean) / 2
        self.acc = 0
        self.count = 0
        return self.mean

    def append(self, x):
        self.acc += x
        self.count += 1


class TimerStatistic(AverageStatistic):
    def __init__(self):
        super().__init__()
        self.start_time = 0

    def __enter__(self):
        self.start_time = perf_counter()

    def __exit__(self, *a):
        delta = perf_counter() - self.start_time
        self.append(delta)
