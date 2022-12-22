# short_desc: helper for calculating score and time, etc...
from dataclasses import dataclass
from typing import Optional, Union, Callable
from time import perf_counter


@dataclass
class ReduceStatistic:
    accumulate: Union[float, int, bool] = 0
    mode: sum

    def summarize(self):
        return self.accumulate

    def append(self, x):
        self.accumulate = self.mode(self.accumulate, x)
        return self.accumulate


@dataclass
class AverageStatistic:
    acc: float = 0
    count: int = 0
    mean: Optional[float] = None

    def summarize(self):
        if self.count == 0:
            return self.mean
        if self.mean is None:
            self.mean = self.acc / self.count
        else:
            self.mean = (self.mean + mean) / 2
        self.acc = 0
        self.count = 0
        return self.mean

    def append(self, x):
        self.acc += x
        self.count += 1


@dataclass
class TimerStatistic:
    stats: Union[AverageStatistic, ReduceStatistic]

    def summarize(self):
        self.stats.summarize()

    def __enter__(self):
        self.start_time = perf_counter()

    def __exit__(self, *a):
        delta = perf_counter() - self.start_time
        self.stats.append(delta)


def TotalTimer():
    return TimerStatistic(ReduceStatistic(sum))


def AverageTimer():
    return TimerStatistic(AverageStatistic())


@dataclass
class Benchmark:
    desc: str = "Time"
    print_function: Callable = print

    def __enter__(self):
        self.start_time = perf_counter()

    def __exit__(self, *a):
        end_time = perf_counter()
        delta = end_time - self.start_time
        self.print_function(f"{self.desc}: {delta:8f}(s)")
