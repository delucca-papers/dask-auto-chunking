from argparse import _SubParsersAction
from toolz import compose, do, curry
from traceq.common.cli import AppendUnique
from .main import compare_profiles


__all__ = ["attach_args"]


def attach_args(subparsers: _SubParsersAction) -> _SubParsersAction:
    analyzer_parser = subparsers.add_parser(
        "analyze",
        help="Analyze outputs generated by TraceQ",
    )

    analyzer_subparsers = analyzer_parser.add_subparsers()

    compose(curry(do)(attach_compare_profiles))(analyzer_subparsers)

    return subparsers


def attach_compare_profiles(subparsers: _SubParsersAction) -> _SubParsersAction:
    compare_parser = subparsers.add_parser(
        "compare-profiles",
        help="Compare different profiles generated by TraceQ",
    )

    compare_parser.add_argument(
        "--session",
        "-s",
        help="Adds a new session to the comparison. The value should be in the format name=path",
        action=AppendUnique,
    )

    compare_parser.add_argument(
        "--unit",
        "-u",
        help="Unit to use for memory usage comparison (default: MB)",
        choices=["b", "kb", "mb", "gb"],
    )

    compare_parser.set_defaults(func=compare_profiles)

    return subparsers