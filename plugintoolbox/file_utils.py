import logging
from pathlib import Path
from typing import Callable, Iterable, Set

from monkeytoolbox import apply_filters

logger = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


def filter_files(
    files: Iterable[Path], file_filters: Iterable[Callable[[Path], bool]]
) -> Iterable[Path]:
    return apply_filters(file_filters, files)


def file_extension_filter(file_extensions: Set) -> Callable[[Path], bool]:
    def inner_filter(f: Path) -> bool:
        return f.suffix in file_extensions

    return inner_filter


def is_not_symlink_filter(f: Path) -> bool:
    return not f.is_symlink()


def is_not_shortcut_filter(f: Path) -> bool:
    return f.suffix != ".lnk"
