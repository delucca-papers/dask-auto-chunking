from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.complex_trace import ResponseAmplitude
    from ..cluster import run_attribute

    quality = ResponseAmplitude()

    return run_attribute(quality, input, n_workers, single_threaded)