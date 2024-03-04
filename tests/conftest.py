from unittest.mock import MagicMock

import pytest
from agentpluginapi import ITCPPortSelector


@pytest.fixture(scope="session")
def tcp_port_selector():
    return MagicMock(spec=ITCPPortSelector)
