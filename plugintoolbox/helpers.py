import logging
import random
import string
from pathlib import Path
from typing import Any, Mapping

from plugintoolbox import VictimHost

logger = logging.getLogger(__name__)

RAND_SUFFIX_LEN = 8


def get_random_file_suffix() -> str:
    character_set = list(string.ascii_letters + string.digits + "_" + "-")
    # random.SystemRandom can block indefinitely in Linux
    random_string = "".join(random.choices(character_set, k=RAND_SUFFIX_LEN))  # noqa: DUO102
    return random_string


def get_agent_dest_path(host: VictimHost, options: Mapping[str, Any]) -> Path:
    if host.os["type"] == "windows":
        path = Path(options["dropper_target_path_win_64"])
    else:
        path = Path(options["dropper_target_path_linux"])

    return _add_random_suffix(path)


#  Turns C:\\monkey.exe into C:\\monkey-<random_string>.exe
#  Useful to avoid duplicate file paths
def _add_random_suffix(path: Path) -> Path:
    stem = path.name.split(".")[0]
    suffixes = path.suffixes
    stem = f"{stem}-{get_random_file_suffix()}"
    rand_filename = "".join([stem, *suffixes])
    path = path.with_name(rand_filename)
    return path
