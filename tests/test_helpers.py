from pathlib import PurePath
from typing import Callable
from unittest.mock import Mock

import pytest
from monkeytypes import OperatingSystem

from plugintoolbox.helpers import (
    AGENT_BINARY_PATH_LINUX,
    AGENT_BINARY_PATH_WIN64,
    DROPPER_SCRIPT_PATH_LINUX,
    RAND_SUFFIX_LEN,
    get_agent_dst_path,
    get_dropper_script_dst_path,
)
from infection_monkey.i_puppet import TargetHost


def _get_host(os):
    host = Mock()
    host.operating_system = os
    return host


@pytest.mark.parametrize(
    "os, path, generate_path",
    [
        (OperatingSystem.LINUX, AGENT_BINARY_PATH_LINUX, get_agent_dst_path),
        (OperatingSystem.WINDOWS, AGENT_BINARY_PATH_WIN64, get_agent_dst_path),
        (OperatingSystem.LINUX, DROPPER_SCRIPT_PATH_LINUX, get_dropper_script_dst_path),
    ],
)
def test_get_agent_dst_path(
    os: OperatingSystem, path: PurePath, generate_path: Callable[[TargetHost], PurePath]
):
    host = _get_host(os)
    rand_path = generate_path(host)
    print(f"{os}: {rand_path}")

    # Assert that filename got longer by RAND_SUFFIX_LEN and one dash
    assert len(str(rand_path)) == (len(str(path)) + RAND_SUFFIX_LEN + 1)


@pytest.mark.parametrize(
    "os, generate_path",
    [
        (OperatingSystem.LINUX, get_agent_dst_path),
        (OperatingSystem.WINDOWS, get_agent_dst_path),
        (OperatingSystem.LINUX, get_dropper_script_dst_path),
    ],
)
def test_get_agent_dst_path_randomness(
    os: OperatingSystem, generate_path: Callable[[TargetHost], PurePath]
):
    host = _get_host(os)

    path1 = generate_path(host)
    path2 = generate_path(host)

    assert path1 != path2


def test_get_agent_dst_path_str_place():
    host = _get_host(OperatingSystem.WINDOWS)

    rand_path = get_agent_dst_path(host)

    assert str(rand_path).startswith(r"C:\Windows\temp\monkey")
    assert str(rand_path).endswith(".exe")


def test_dropper_script_windows_not_implemented():
    host = _get_host(OperatingSystem.WINDOWS)

    with pytest.raises(NotImplementedError):
        get_dropper_script_dst_path(host)
