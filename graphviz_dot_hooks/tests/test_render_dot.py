import os
import shutil
from collections import namedtuple
import tempfile

from graphviz_dot_hooks.render_dot import render_dotfiles_to_png, _parse_only_convert

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_DOT_SAMPLE_1 = os.path.join(CUR_DIR, "valid_dot_sample1.dot")
INVALID_DOT_SAMPLE_1 = os.path.join(CUR_DIR, "invalid_dot_sample1.yml")

args_tuple = namedtuple("args", "instancefiles")


def test__parse_only_convert__no_target__use_defaut_png():
    assert _parse_only_convert("s1.dot") == {"s1.dot": "s1.dot.png"}


def test__parse_only_convert__target__use_defaut_png():
    assert _parse_only_convert("s1.dot:renamed.png") == {"s1.dot": "renamed.png"}


def test__parse_only_convert__mixed_case__use_defaut_png():
    assert _parse_only_convert("./some_dir/s0.dot, s1.dot:renamed.png") == {
        "./some_dir/s0.dot": "./some_dir/s0.dot.png",
        "s1.dot": "renamed.png",
    }


def test_render_dotfiles_to_png__not_exist_yet__return_false():
    with tempfile.TemporaryDirectory() as tmpdir_path:
        copied_filepath = tmpdir_path + "/" + os.path.basename(VALID_DOT_SAMPLE_1)
        shutil.copy(VALID_DOT_SAMPLE_1, copied_filepath)

        expected_png_filepath = copied_filepath + ".png"
        assert not os.path.exists(expected_png_filepath)

        ok, msgs = render_dotfiles_to_png({copied_filepath: expected_png_filepath})
        assert not ok
        assert len(msgs) == 1
        assert "Re-generated" in msgs[0]

        assert os.path.exists(expected_png_filepath)
        assert os.path.exists(copied_filepath)


def test_render_dotfiles_to_png__exist_already_but_outdated__return_true():
    with tempfile.TemporaryDirectory() as tmpdir_path:
        copied_filepath = tmpdir_path + "/" + os.path.basename(VALID_DOT_SAMPLE_1)
        shutil.copy(VALID_DOT_SAMPLE_1, copied_filepath)

        expected_png_filepath = copied_filepath + ".png"

        with open(expected_png_filepath, "w") as f:
            f.write("whatever")

        assert os.path.exists(expected_png_filepath)

        ok, msgs = render_dotfiles_to_png({copied_filepath: expected_png_filepath})
        assert not ok
        assert len(msgs) == 1
        assert "Re-generated" in msgs[0]

        assert os.path.exists(expected_png_filepath)
        assert os.path.exists(copied_filepath)


def test_render_dotfiles_to_png__exist_already_uptodate__return_true():
    with tempfile.TemporaryDirectory() as tmpdir_path:
        copied_filepath = tmpdir_path + "/" + os.path.basename(VALID_DOT_SAMPLE_1)
        shutil.copy(VALID_DOT_SAMPLE_1, copied_filepath)

        expected_png_filepath = copied_filepath + ".png"

        # Let it create it on its own
        ok, _ = render_dotfiles_to_png({copied_filepath: expected_png_filepath})
        assert not ok

        assert os.path.exists(expected_png_filepath)
        assert os.path.exists(copied_filepath)

        # Call it a second time
        ok, msgs = render_dotfiles_to_png({copied_filepath: expected_png_filepath})
        assert ok
        assert not msgs
