from pathlib import Path
from unittest.mock import MagicMock

import pytest

from plugintoolbox import (
    filter_files,
    file_extension_filter,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)


@pytest.fixture
def mock_files():
    files = [
        MagicMock(spec=Path, suffix=".txt", is_symlink=MagicMock(return_value=False)),
        MagicMock(spec=Path, suffix=".jpg", is_symlink=MagicMock(return_value=True)),
        MagicMock(spec=Path, suffix=".lnk", is_symlink=MagicMock(return_value=False)),
    ]
    return files


def test_filter_files(mock_files):
    file_filters = [file_extension_filter({".txt"}), is_not_symlink_filter]
    filtered_files = list(filter_files(mock_files, file_filters))

    assert len(filtered_files) == 1
    assert filtered_files[0].suffix == ".txt"


def test_file_extension_filter(mock_files):
    txt_filter = file_extension_filter({".txt"})

    assert txt_filter(mock_files[0]) is True
    assert txt_filter(mock_files[1]) is False


def test_is_not_symlink_filter(mock_files):
    assert is_not_symlink_filter(mock_files[0]) is True
    assert is_not_symlink_filter(mock_files[1]) is False


def test_is_not_shortcut_filter(mock_files):
    assert is_not_shortcut_filter(mock_files[0]) is True
    assert is_not_shortcut_filter(mock_files[2]) is False
