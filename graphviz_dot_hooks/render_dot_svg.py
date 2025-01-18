import argparse
import sys
from typing import Dict

from graphviz_dot_hooks.utils import render_dotfiles, _parse_only_convert

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
    "          --only dotfile1.dot:doc/dotfile1.svg,dotfile2.dot",
)


def main():
    args = parser.parse_args()

    format = "svg"

    convert_map: Dict[str, str]
    if args.only:
        # Take the intersection of the instancefiles and the --only
        convert_map = _parse_only_convert(args.only, format=format)
        convert_map = {
            src: target
            for src, target in convert_map.items()
            if src in args.instancefiles
        }
    else:
        # Take the instancefiles
        convert_map = _parse_only_convert(",".join(args.instancefiles), format=format)

    success, messages = render_dotfiles(convert_map, format=format)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
