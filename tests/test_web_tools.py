from ipaddress import IPv4Address

import pytest
from monkeytypes import NetworkPort

from plugintoolbox.web_tools import build_urls

HOST_IP = IPv4Address("1.1.1.1")


def test_build_urls__no_extensions():
    expected_url_list = ["http://1.1.1.1:8080/", "https://1.1.1.1:80/", "http://1.1.1.1:443/"]

    actual_url_list = build_urls(
        HOST_IP, [(NetworkPort(8080), False), (NetworkPort(80), True), (NetworkPort(443), False)]
    )

    assert expected_url_list == actual_url_list


@pytest.mark.parametrize("path_components", [["/api/agents", "api/"]])
def test_build_urls__path_components(path_components):
    expected_url_list = ["https://1.1.1.1:80/api/agents", "https://1.1.1.1:80/api/"]

    actual_url_list = build_urls(HOST_IP, [(NetworkPort(80), True)], path_components)

    assert len(expected_url_list) == len(actual_url_list)
    assert expected_url_list == actual_url_list


def test_build_urls__raise_value_error():
    with pytest.raises(ValueError):
        build_urls(HOST_IP, [(NetworkPort(8080),)])  # type: ignore [list-item]
