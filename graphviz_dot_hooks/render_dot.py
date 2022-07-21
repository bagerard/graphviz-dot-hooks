import argparse
import os.path
import sys
import shutil
from subprocess import CalledProcessError
from typing import Tuple, List, Optional, Dict
import tempfile

from graphviz import render


def read_file(p: str) -> Optional[bytes]:
    if not os.path.exists(p):
        return None

    with open(p, "rb") as fin:
        return fin.read()


def _render_dotfile_to_png(
    src_dot_filepath: str, target_png_filepath: str
) -> Tuple[bool, Optional[str]]:
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpf:
        try:
            print(f"rendering {src_dot_filepath} to png")
            render("dot", "png", src_dot_filepath, outfile=tmpf.name)
        except CalledProcessError as ex:
            return False, str(ex)

        else:
            new_file_content = read_file(tmpf.name)
            old_file_content = read_file(target_png_filepath)

            if new_file_content != old_file_content:
                print(f"Overwriting {target_png_filepath}")
                shutil.copy(tmpf.name, target_png_filepath)
                return False, f"Re-generated file {target_png_filepath}"
            else:
                print(f"{target_png_filepath} is up to date")
                return True, None


def render_dotfiles_to_png(dot_filepaths_map: Dict[str, str]) -> Tuple[bool, List[str]]:
    all_succeeded = True
    messages = []

    for src_dot_filepath, target_png_filepath in dot_filepaths_map.items():
        is_ok, error_message = _render_dotfile_to_png(
            src_dot_filepath, target_png_filepath
        )
        if not is_ok:
            messages.append(error_message)
            all_succeeded = all_succeeded and False

    return all_succeeded, messages


def _default_png_path(dot_filepath):
    return dot_filepath + ".png"


def _parse_only_convert(convert: str) -> Dict[str, str]:
    convert_items = convert.split(",")

    convert_map = {}
    for convert_item in convert_items:
        src_target = convert_item.split(":")
        if not len(src_target) <= 2:
            raise ValueError(f"Wrong format of value for --only: {convert_item}")

        src = src_target[0]
        target = src_target[1] if len(src_target) == 2 else _default_png_path(src)
        convert_map[src.strip()] = target.strip()
    return convert_map


parser = argparse.ArgumentParser()
parser.add_argument("instancefiles", nargs="+", help=".dot files to check")
parser.add_argument(
    "--only",
    action="store",
    type=str,
    default=None,
    required=False,
    help="string with coma-separated values, target files can be specified as well in the format '--only src1:target1,src2:target2'"
    " Example: --only dotfile1.dot,dotfile2.dot"
    "          --only dotfile1.dot:doc/dotfile1.png,dotfile2.dot",
)


def main():
    args = parser.parse_args()

    convert_map: Dict[str, str]
    if args.only:
        # Take the intersection of the instancefiles and the --only
        convert_map = _parse_only_convert(args.only)
        convert_map = {
            src: target
            for src, target in convert_map.items()
            if src in args.instancefiles
        }
    else:
        # Take the instancefiles
        convert_map = _parse_only_convert(",".join(args.instancefiles))

    success, messages = render_dotfiles_to_png(convert_map)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
