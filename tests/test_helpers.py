from unittest.mock import Mock

import pytest

from plugintoolbox.helpers import RAND_SUFFIX_LEN, get_agent_dest_path


def _get_host_and_options(os, path):
    host = Mock()
    host.os = {"type": os}
    options = {"dropper_target_path_win_64": path, "dropper_target_path_linux": path}
    return host, options


@pytest.mark.parametrize("os", ["windows", "linux"])
@pytest.mark.parametrize("path", ["C:\\monkey.exe", "/tmp/monkey-linux-64", "mon.key.exe"])
def test_get_agent_dest_path(os, path):
    host, options = _get_host_and_options(os, path)
    rand_path = get_agent_dest_path(host, options)

    # Assert that filename got longer by RAND_SUFFIX_LEN and one dash
    assert len(str(rand_path)) == (len(str(path)) + RAND_SUFFIX_LEN + 1)


def test_get_agent_dest_path_randomness():
    host, options = _get_host_and_options("windows", "monkey.exe")

    path1 = get_agent_dest_path(host, options)
    path2 = get_agent_dest_path(host, options)

    assert not path1 == path2


def test_get_agent_dest_path_str_place():
    host, options = _get_host_and_options("windows", "C:\\abc\\monkey.exe")

    rand_path = get_agent_dest_path(host, options)

    assert str(rand_path).startswith("C:\\abc\\monkey-")
    assert str(rand_path).endswith(".exe")
