import time

from typing import Callable, Any
from functools import wraps
from toolz import curry
from dowser.common import get_function_path
from dowser.logger import get_logger
from ...report import ProfilerReport
from .types import TimeLog


def to_time_log(start_time: float, end_time: float) -> TimeLog:
    execution_time = end_time - start_time
    return [
        ("START", start_time),
        ("END", end_time),
        ("EXECUTION_TIME", execution_time),
    ]


@curry
def profile_time(report: ProfilerReport, function: Callable) -> Callable:
    logger = get_logger()
    logger.info(f'Setting up time profiler for function "{function.__name__}"')

    metadata = {
        "function_path": get_function_path(function),
        "unit": "seconds",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()

        time_profile = to_time_log(start_time, end_time)
        logger.debug(f"Amount of collected profile points: {len(time_profile)}")
        logger.debug(f"Sample data point: {time_profile[0]}")
        logger.debug(f"Total execution time: {time_profile[-1][1]}s")

        report.add_profile("time", time_profile, metadata)

        return result

    return wrapper


__all__ = ["profile_time"]
