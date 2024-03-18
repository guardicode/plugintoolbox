from ipaddress import IPv4Address
from posixpath import join
from typing import List, Optional, Tuple

from monkeytypes import NetworkPort


def build_urls(
    ip: IPv4Address,
    ports: List[Tuple[NetworkPort, bool]],
    path_components: Optional[List[str]] = None,
) -> List[str]:
    """
    Build all possibly-vulnerable URLs on a specific host, based on the relevant ports and
    extensions.

    :param ip: IP address of the victim
    :param ports: List of port where a port is consisted of: [NetworkPort, isHTTPS?(bool)]
        Eg. ports: [[80, False], [443, True]]
    :param path_components: List of strings representing path components of a URL.
        Eg. www.domain.com[/extension]
    :return: Array of url's to try and attack
    """
    if path_components is None:
        path_components = [""]
    else:
        # Remove leading slashes from extensions if present
        path_components = [e.lstrip("/") for e in path_components]

    url_list = []
    for port, is_https in ports:
        protocol = "https" if is_https else "http"
        url = f"{protocol}://{ip}:{port}"
        for component in path_components:
            url_list.append(join(url, component))

    return url_list
