from http import HTTPStatus
from ipaddress import IPv4Address
from multiprocessing import get_context
from typing import Generator

import pytest
import requests

from common.types import NetworkPort, SocketAddress
from plugintoolbox import HTTPBytesServer
from infection_monkey.network import TCPPortSelector


@pytest.fixture
def ip() -> IPv4Address:
    return IPv4Address("127.0.0.1")


@pytest.fixture
def tcp_port_selector() -> TCPPortSelector:
    context = get_context("spawn")
    return TCPPortSelector(context, context.Manager())


@pytest.fixture
def port(tcp_port_selector: TCPPortSelector) -> NetworkPort:
    return tcp_port_selector.get_free_tcp_port()


@pytest.fixture
def socket_address(ip: IPv4Address, port: NetworkPort) -> SocketAddress:
    return SocketAddress(ip=ip, port=port)


@pytest.fixture
def bytes_to_serve() -> bytes:
    return b"\xde\xad\xbe\xef"


@pytest.fixture
def server(
    socket_address: SocketAddress, bytes_to_serve: bytes
) -> Generator[HTTPBytesServer, None, None]:
    server = HTTPBytesServer(socket_address, bytes_to_serve, 0.01)
    server.start()

    yield server

    server.stop()


@pytest.fixture
def second_server(
    ip: IPv4Address, bytes_to_serve: bytes, tcp_port_selector: TCPPortSelector
) -> Generator[HTTPBytesServer, None, None]:
    second_socket_address = SocketAddress(ip=ip, port=tcp_port_selector.get_free_tcp_port())
    server = HTTPBytesServer(second_socket_address, bytes_to_serve, 0.01)
    server.start()

    yield server

    server.stop()


@pytest.fixture
def download_url(ip: IPv4Address, port: NetworkPort) -> str:
    return f"http://{ip}:{port}/"


@pytest.mark.usefixtures("server")
def test_only_single_download_allowed(download_url: str, bytes_to_serve: bytes):
    response_1 = requests.get(download_url)
    assert response_1.status_code == 200
    assert response_1.content == bytes_to_serve

    response_2 = requests.get(download_url)
    assert response_2.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert response_2.content != bytes_to_serve


def test_download_requested(server: HTTPBytesServer, download_url: str):
    assert not server.download_requested.is_set()

    requests.get(download_url)

    assert server.download_requested.is_set()


def test_thread_safety(server: HTTPBytesServer, second_server: HTTPBytesServer, download_url: str):
    assert not server.download_requested.is_set()
    assert not second_server.download_requested.is_set()

    requests.get(download_url)

    assert server.download_requested.is_set()
    assert not second_server.download_requested.is_set()


def test_download_url(server: HTTPBytesServer, download_url: str):
    assert server.download_url == download_url
