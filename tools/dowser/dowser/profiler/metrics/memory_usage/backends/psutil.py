from psutil import Process
from dowser.common.synchronization import passthrough
from dowser.profiler.types import CapturedTrace


__all__ = ["before", "on_call", "on_return", "after"]


process = Process()


def get_memory_usage() -> float:
    memory_usage = process.memory_info().rss

    return float(memory_usage)


def capture_trace(*_) -> CapturedTrace:
    memory_usage = get_memory_usage()
    return "psutil_memory_usage", memory_usage


def before() -> None:
    globals()["process"] = Process()


after = passthrough
on_call = capture_trace
on_return = capture_trace