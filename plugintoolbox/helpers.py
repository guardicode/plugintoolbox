import logging
import random
import string
from pathlib import PurePath, PurePosixPath, PureWindowsPath

from plugintoolbox import VictimHost

logger = logging.getLogger(__name__)

RAND_SUFFIX_LEN = 8

# Where to upload agent binaries on victims
AGENT_BINARY_PATH_LINUX = "/tmp/monkey"
AGENT_BINARY_PATH_WIN64 = r"C:\Windows\temp\monkey64.exe"


def get_agent_dest_path(host: VictimHost) -> PurePath:
    if host.os["type"] == "windows":
        path = PureWindowsPath(AGENT_BINARY_PATH_WIN64)
    else:
        path = PurePosixPath(AGENT_BINARY_PATH_LINUX)

    return _add_random_suffix(path)


def get_random_file_suffix() -> str:
    character_set = list(string.ascii_letters + string.digits + "_" + "-")
    # random.SystemRandom can block indefinitely in Linux
    random_string = "".join(random.choices(character_set, k=RAND_SUFFIX_LEN))  # noqa: DUO102
    return random_string


#  Turns C:\\monkey.exe into C:\\monkey-<random_string>.exe
#  Useful to avoid duplicate file paths
def _add_random_suffix(path: PurePath) -> PurePath:
    stem = path.name.split(".")[0]
    stem = f"{stem}-{get_random_file_suffix()}"
    rand_filename = "".join([stem, *path.suffixes])
    return path.with_name(rand_filename)
