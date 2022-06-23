from unittest.mock import Mock

import pytest

from common import OperatingSystems
from plugintoolbox.helpers import (
    AGENT_BINARY_PATH_LINUX,
    AGENT_BINARY_PATH_WIN64,
    RAND_SUFFIX_LEN,
    get_agent_dst_path,
)


def _get_host(os):
    host = Mock()
    host.os = {"type": os}
    host.is_windows = lambda: os == OperatingSystems.WINDOWS
    return host


@pytest.mark.parametrize(
    "os, path",
    [
        (OperatingSystems.LINUX, AGENT_BINARY_PATH_LINUX),
        (OperatingSystems.WINDOWS, AGENT_BINARY_PATH_WIN64),
    ],
)
def test_get_agent_dst_path(os, path):
    host = _get_host(os)
    rand_path = get_agent_dst_path(host)
    print(f"{os}: {rand_path}")

    # Assert that filename got longer by RAND_SUFFIX_LEN and one dash
    assert len(str(rand_path)) == (len(str(path)) + RAND_SUFFIX_LEN + 1)


def test_get_agent_dst_path_randomness():
    host = _get_host(OperatingSystems.WINDOWS)

    path1 = get_agent_dst_path(host)
    path2 = get_agent_dst_path(host)

    assert path1 != path2


def test_get_agent_dst_path_str_place():
    host = _get_host(OperatingSystems.WINDOWS)

    rand_path = get_agent_dst_path(host)

    assert str(rand_path).startswith(r"C:\Windows\temp\monkey")
    assert str(rand_path).endswith(".exe")
