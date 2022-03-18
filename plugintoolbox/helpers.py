import logging
import random
import string
from typing import Any, Mapping

from plugintoolbox import VictimHost

logger = logging.getLogger(__name__)


def try_get_target_monkey(host):
    src_path = get_target_monkey(host)
    if not src_path:
        raise Exception("Can't find suitable monkey executable for host %r", host)
    return src_path


def get_target_monkey(host):
    raise NotImplementedError("get_target_monkey() has been retired. Use IAgentRepository instead.")


def get_random_file_suffix() -> str:
    character_set = list(string.ascii_letters + string.digits + "_" + "-")
    # random.SystemRandom can block indefinitely in Linux
    random_string = "".join(random.choices(character_set, k=8))  # noqa: DUO102
    return random_string


def get_agent_dest_path(host: VictimHost, options: Mapping[str, Any]) -> str:
    if host.os["type"] == "windows":
        return options["dropper_target_path_win_64"]
    else:
        return options["dropper_target_path_linux"]
