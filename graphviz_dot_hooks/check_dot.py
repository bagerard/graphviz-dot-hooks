import argparse
import sys
from subprocess import CalledProcessError
from typing import Tuple, List, Sequence, Optional
import tempfile

from graphviz import render


def _verify_dot_rendering(dot_filepath: str) -> Tuple[bool, Optional[str]]:
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpf:
        try:
            render("dot", "png", dot_filepath, outfile=tmpf.name)
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
