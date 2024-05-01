import resource

from types import FrameType
from typing import Any, Tuple
from dowser.config import ProfilerMetric
from dowser.common.synchronization import passthrough


__all__ = ["before", "on_call", "on_return", "after"]


before = passthrough
after = passthrough


def get_memory_usage() -> Tuple[float, str]:
    unit = "kb"
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return ProfilerMetric.MEMORY_USAGE.value, float(memory_usage), unit


def on_call(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()


def on_return(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()
