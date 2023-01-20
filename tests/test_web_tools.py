import pytest

from plugintoolbox.web_tools import build_urls


def test_build_urls__no_extensions():
    expected_url_list = ["http://1.1.1.1:8080/", "https://1.1.1.1:80/", "http://1.1.1.1:443/"]

    actual_url_list = build_urls("1.1.1.1", [("8080", False), ("80", True), ("443", False)])

    assert expected_url_list == actual_url_list


@pytest.mark.parametrize("extension", [["/api/agents", "api/"]])
def test_build_urls__extensions(extension):
    expected_url_list = ["https://1.1.1.1:80/api/agents", "https://1.1.1.1:80/api/"]

    actual_url_list = build_urls("1.1.1.1", [("80", True)], extension)

    assert len(expected_url_list) == len(actual_url_list)
    assert expected_url_list == actual_url_list


def test_build_urls__raise_key_error():
    with pytest.raises(IndexError):
        build_urls("1.1.1.1", [("8080",)])
