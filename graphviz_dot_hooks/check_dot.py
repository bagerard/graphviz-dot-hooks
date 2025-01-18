import argparse
import sys
from subprocess import CalledProcessError
from typing import Tuple, List, Sequence, Optional
import tempfile

from graphviz import render


def _verify_dot_rendering(dot_filepath: str) -> Tuple[bool, Optional[str]]:
    """Trying to render it would detect syntax error, there are probably cheaper way to check this
    but we aren't really looking after performance here"""
    with tempfile.NamedTemporaryFile(suffix=f".{format}") as tmpf:
        try:
            # arbitrary render as svg (more generic than png)
            # but it doesn't matter much as we are mostly interested in .dot syntax
            render("dot", "svg", dot_filepath, outfile=tmpf.name)
        except CalledProcessError as ex:
            return False, str(ex)

    return True, None


def verify_dots_rendering(dot_filepaths: Sequence[str]) -> Tuple[bool, List[str]]:
    all_succeeded = True
    messages = []

    for dot_filepath in dot_filepaths:
        is_ok, error_message = _verify_dot_rendering(dot_filepath)
        if not is_ok:
            messages.append(error_message)
            all_succeeded = all_succeeded and False

    return all_succeeded, messages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instancefiles", nargs="+", help=".dot files to check")

    args = parser.parse_args()

    success, messages = verify_dots_rendering(args.instancefiles)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
