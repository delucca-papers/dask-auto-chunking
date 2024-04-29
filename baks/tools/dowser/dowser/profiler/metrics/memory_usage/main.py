from typing import Callable
from toolz import compose, curry, identity
from dowser.common import Report
from dowser.logger import get_logger
from dowser.profiler.context import profiler_context
from dowser.profiler.types import Metadata
from .backends import kernel, mprof, psutil, resource, tracemalloc


@curry
def profile_memory_usage(
    report: Report,
    metadata: Metadata,
    function: Callable,
) -> Callable:
    logger = get_logger()
    logger.info(f'Setting up memory usage profiler for function "{function.__name__}"')

    enabled_backends = profiler_context.memory_usage_enabled_backends
    logger.debug(f"Enabled memory usage backends: {enabled_backends}")

    return compose(
        (
            kernel.profile_memory_usage(report, metadata)
            if "kernel" in enabled_backends
            else identity
        ),
        (
            mprof.profile_memory_usage(report, metadata)
            if "mprof" in enabled_backends
            else identity
        ),
        (
            psutil.profile_memory_usage(report, metadata)
            if "psutil" in enabled_backends
            else identity
        ),
        (
            resource.profile_memory_usage(report, metadata)
            if "resource" in enabled_backends
            else identity
        ),
        (
            tracemalloc.profile_memory_usage(report, metadata)
            if "tracemalloc" in enabled_backends
            else identity
        ),
    )(function)


__all__ = ["profile_memory_usage"]