from unittest.mock import MagicMock

import pytest
from agentpluginapi import ITCPPortSelector
from monkeytypes import NetworkPort


@pytest.fixture(scope="session")
def tcp_port_selector():
    tcp_port_selector = MagicMock(spec=ITCPPortSelector)
    tcp_port_selector.get_free_tcp_port.side_effect = (NetworkPort(p) for p in range(54321, 65536))
    return tcp_port_selector
