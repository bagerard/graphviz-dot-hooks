import argparse
import os.path
import sys
import shutil
from subprocess import CalledProcessError
from typing import Tuple, List, Sequence, Optional
import tempfile

from graphviz import render


def read_file(p: str) -> Optional[bytes]:
    if not os.path.exists(p):
        return None

    with open(p, "rb") as fin:
        return fin.read()


def _render_dotfile_to_png(dot_filepath: str) -> Tuple[bool, Optional[str]]:
    expected_rendered_file_path = dot_filepath + ".png"
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpf:
        try:
            print(f"render {dot_filepath}")
            render("dot", "png", dot_filepath, outfile=tmpf.name)
        except CalledProcessError as ex:
            return False, str(ex)

        else:
            new_file_content = read_file(tmpf.name)
            old_file_content = read_file(expected_rendered_file_path)

            if new_file_content != old_file_content:
                print(f"Overwriting {expected_rendered_file_path}")
                shutil.copy(tmpf.name, expected_rendered_file_path)
                return False, f"Re-generated file {expected_rendered_file_path}"
            else:
                print(f"{expected_rendered_file_path} is up to date")
                return True, None


def render_dotfiles_to_png(dot_filepaths: Sequence[str]) -> Tuple[bool, List[str]]:
    all_succeeded = True
    messages = []

    for dot_filepath in dot_filepaths:
        is_ok, error_message = _render_dotfile_to_png(dot_filepath)
        if not is_ok:
            messages.append(error_message)
            all_succeeded = all_succeeded and False

    return all_succeeded, messages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instancefiles", nargs="+", help="JSON or YAML files to check.")

    args = parser.parse_args()

    success, messages = render_dotfiles_to_png(args.instancefiles)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
