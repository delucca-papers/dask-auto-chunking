import sys

from typing import Optional, Callable
from pathlib import Path
from dowser.common.logger import logger


__all__ = ["execute_file"]


def execute_file(
    filepath: Path,
    args: tuple,
    kwargs: dict,
    function_name: Optional[str] = None,
    before: Callable = lambda: None,
    after: Callable = lambda: None,
) -> None:
    logger.info(
        f'Starting new profiler session for file "{filepath}" with entrypoint set to: "{function_name if function_name else "__main__"}"'
    )
    logger.debug(f"Using args: {args}")
    logger.debug(f"Using kwargs: {kwargs}")

    original_argv = sys.argv.copy()
    sys.argv = [str(filepath)] + list(args)
    exec_globals = {
        "__name__": "__main__.sub" if function_name else "__main__",
        "__file__": str(filepath),
        "__package__": None,
        "__builtins__": __builtins__,
    }

    with open(filepath, "r") as f:
        file_content = f.read()

    try:
        compiled_code = compile(file_content, str(filepath), "exec")

        logger.info("Running before hooks")
        before()

        logger.info(f"Executing file: {filepath}")
        exec(compiled_code, exec_globals)

        if function_name:
            logger.debug(f'Using function "{function_name}" as entrypoint')
            function = exec_globals[function_name]
            function(*args, **kwargs)

        logger.info("Running after hooks")
        after()
    finally:
        sys.argv = original_argv
        logger.info(f'File "{filepath}" finished execution')
