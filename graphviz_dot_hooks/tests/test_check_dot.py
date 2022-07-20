import os
from collections import namedtuple

from graphviz_dot_hooks.check_dot import _verify_dot_rendering, verify_dots_rendering

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_DOT_SAMPLE_1 = os.path.join(CUR_DIR, "valid_dot_sample1.dot")
INVALID_DOT_SAMPLE_1 = os.path.join(CUR_DIR, "invalid_dot_sample1.yml")

args_tuple = namedtuple("args", "instancefiles")


def test__verify_dot_rendering__valid_file__successful():
    ok, msg = _verify_dot_rendering(VALID_DOT_SAMPLE_1)
    assert ok is True
    assert msg is None


def test__verify_dot_rendering__invalid_file__return_error_message():
    ok, msg = _verify_dot_rendering(INVALID_DOT_SAMPLE_1)
    assert not ok
    assert "Error: dot: can't open invalid_dot_sample1.yml" in msg


def test_verify_dots_rendering__1_invalid__fails():
    success, msgs = verify_dots_rendering([INVALID_DOT_SAMPLE_1])
    assert not success
    assert len(msgs) == 1
    assert "Error: dot: can't open invalid_dot_sample1.yml" in msgs[0]


def test_verify_dots_rendering__1_valid__pass():
    success, msgs = verify_dots_rendering([VALID_DOT_SAMPLE_1])
    assert success
    assert not msgs


def test_verify_dots_rendering__1_valid_1_invalid__fails():
    success, msgs = verify_dots_rendering([VALID_DOT_SAMPLE_1, INVALID_DOT_SAMPLE_1])
    assert not success
    assert len(msgs) == 1
    assert "Error: dot: can't open invalid_dot_sample1.yml" in msgs[0]
