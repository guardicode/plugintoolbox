from unittest.mock import Mock

import pytest

from plugintoolbox.helpers import (
    AGENT_BINARY_PATH_LINUX,
    AGENT_BINARY_PATH_WIN64,
    RAND_SUFFIX_LEN,
    get_agent_dest_path,
)


def _get_host(os):
    host = Mock()
    host.os = {"type": os}
    return host


@pytest.mark.parametrize(
    "os, path", [("linux", AGENT_BINARY_PATH_LINUX), ("windows", AGENT_BINARY_PATH_WIN64)]
)
def test_get_agent_dest_path(os, path):
    host = _get_host(os)
    rand_path = get_agent_dest_path(host)

    # Assert that filename got longer by RAND_SUFFIX_LEN and one dash
    assert len(str(rand_path)) == (len(str(path)) + RAND_SUFFIX_LEN + 1)


def test_get_agent_dest_path_randomness():
    host = _get_host("windows")

    path1 = get_agent_dest_path(host)
    path2 = get_agent_dest_path(host)

    assert path1 != path2


def test_get_agent_dest_path_str_place():
    host = _get_host("windows")

    rand_path = get_agent_dest_path(host)

    assert str(rand_path).startswith(r"C:\Windows\temp\monkey")
    assert str(rand_path).endswith(".exe")
