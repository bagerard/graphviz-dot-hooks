import os.path
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


def _render_dotfile(
    src_dot_filepath: str, target_filepath: str, format: str
) -> Tuple[bool, Optional[str]]:
    assert format in ("png", "svg")
    with tempfile.NamedTemporaryFile(suffix=f".{format}") as tmpf:
        try:
            print(f"rendering {src_dot_filepath} to {format}")
            render("dot", format, src_dot_filepath, outfile=tmpf.name)
        except CalledProcessError as ex:
            return False, str(ex)

        else:
            new_file_content = read_file(tmpf.name)
            old_file_content = read_file(target_filepath)

            if new_file_content != old_file_content:
                print(f"Overwriting {target_filepath}")
                shutil.copy(tmpf.name, target_filepath)
                return False, f"Re-generated file {target_filepath}"
            else:
                print(f"{target_filepath} is up to date")
                return True, None


def render_dotfiles(
    dot_filepaths_map: Dict[str, str], format: str
) -> Tuple[bool, List[str]]:
    assert format in ("png", "svg")

    all_succeeded = True
    messages = []

    for src_dot_filepath, target_filepath in dot_filepaths_map.items():
        is_ok, error_message = _render_dotfile(
            src_dot_filepath=src_dot_filepath,
            target_filepath=target_filepath,
            format=format,
        )
        if not is_ok:
            messages.append(error_message)
            all_succeeded = all_succeeded and False

    return all_succeeded, messages


def _default_target_path(dot_filepath, format: str):
    return dot_filepath + f".{format}"


def _parse_only_convert(convert: str, format: str) -> Dict[str, str]:
    convert_items = convert.split(",")

    convert_map = {}
    for convert_item in convert_items:
        src_target = convert_item.split(":")
        if not len(src_target) <= 2:
            raise ValueError(f"Wrong format of value for --only: {convert_item}")

        src = src_target[0]
        target = (
            src_target[1]
            if len(src_target) == 2
            else _default_target_path(src, format=format)
        )
        convert_map[src.strip()] = target.strip()
    return convert_map
