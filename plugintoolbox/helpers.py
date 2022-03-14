import logging
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


def get_target_monkey_by_os(is_windows, is_32bit):
    raise NotImplementedError(
        "get_target_monkey_by_os() has been retired. Use IAgentRepository instead."
    )


def get_monkey_depth():
    from infection_monkey.config import WormConfiguration

    return WormConfiguration.depth


def get_agent_dest_path(host: VictimHost, options: Mapping[str, Any]) -> str:
    if host.os["type"] == "windows":
        return options["dropper_target_path_win_64"]
    else:
        return options["dropper_target_path_linux"]
