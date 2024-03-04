from typing import Sequence, Set

from agentpluginapi import TargetHost
from monkeytypes import NetworkPort, NetworkProtocol, NetworkService

# NOTE: Don't migrate these functions to a user-facing interface
#       without properly thinking about it. Are these functions stable enough?
#       Are they promises that we want to keep to users who build their own plugins?


def all_tcp_ports_are_closed(host: TargetHost, tcp_ports: Sequence[NetworkPort]) -> bool:
    closed_tcp_ports = host.ports_status.tcp_ports.closed
    return all([p in closed_tcp_ports for p in tcp_ports])


def all_udp_ports_are_closed(host: TargetHost, udp_ports: Sequence[NetworkPort]) -> bool:
    """
    Check if all UDP ports in a given sequence are closed on the host

    :param host: The host to check
    :param udp_ports: The sequence of UDP ports to check
    :return: True if all ports are closed, False otherwise
    """
    closed_udp_ports = host.ports_status.udp_ports.closed
    return all([p in closed_udp_ports for p in udp_ports])


def filter_out_closed_ports(host: TargetHost, ports: Sequence[NetworkPort]) -> Set[NetworkPort]:
    return {port for port in ports if port not in host.ports_status.tcp_ports.closed}


def get_known_service_ports(
    host: TargetHost, protocol: NetworkProtocol, service: NetworkService
) -> Sequence[NetworkPort]:
    ports = (
        host.ports_status.tcp_ports
        if protocol == NetworkProtocol.TCP
        else host.ports_status.udp_ports
    )

    return [port for port in ports.open if ports[port].service == service]
