from typing import Callable, Iterable, List, Set

import pytest
from monkeytypes import (
    Credentials,
    EmailAddress,
    Identity,
    LMHash,
    NTHash,
    Password,
    Secret,
    Username,
)

from plugintoolbox import generate_brute_force_credentials, identity_type_filter, secret_type_filter
from tests.propagation_credentials import IDENTITIES, SECRETS


def generate_and_compare_credentials(
    input_credentials: Iterable[Credentials],
    expected_credentials: Set[Credentials],
    identity_filter: Callable[[Identity], bool] = lambda identity: True,
    secret_filter: Callable[[Secret], bool] = lambda secret: True,
):
    generated_credentials = generate_brute_force_credentials(
        input_credentials, identity_filter=identity_filter, secret_filter=secret_filter
    )

    assert len(generated_credentials) == len(expected_credentials)
    assert set(generated_credentials) == expected_credentials


def test_generate_all_combinations_1():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=None),
        Credentials(identity=IDENTITIES[2], secret=None),
        Credentials(identity=None, secret=SECRETS[0]),
        Credentials(identity=None, secret=SECRETS[3]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    }

    generate_and_compare_credentials(input_credentials, expected_credentials)


def test_generate_all_combinations_2():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    }

    generate_and_compare_credentials(input_credentials, expected_credentials)


def test_generate_all_combinations_3():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=None, secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[5]),
    }

    generate_and_compare_credentials(input_credentials, expected_credentials)


def test_generate_all_combinations_4():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=None),
        Credentials(identity=None, secret=SECRETS[5]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[5]),
    }

    generate_and_compare_credentials(input_credentials, expected_credentials)


def test_generate_all_combinations_single_result():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=None),
        Credentials(identity=None, secret=SECRETS[0]),
    ]
    expected_credentials = [Credentials(identity=IDENTITIES[0], secret=SECRETS[0])]

    generated_credentials = generate_brute_force_credentials(input_credentials)

    assert generated_credentials == expected_credentials


def test_generate_all_combinations_duplicates():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=None),
        Credentials(identity=IDENTITIES[2], secret=None),
        Credentials(identity=None, secret=SECRETS[5]),
        Credentials(identity=None, secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[5]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[5]),
    }

    generate_and_compare_credentials(input_credentials, expected_credentials)


def test_only_identities():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=None),
        Credentials(identity=IDENTITIES[2], secret=None),
    ]

    generate_and_compare_credentials(input_credentials, set())


def test_only_secrets():
    input_credentials = [
        Credentials(identity=None, secret=SECRETS[0]),
        Credentials(identity=None, secret=SECRETS[1]),
        Credentials(identity=None, secret=SECRETS[2]),
    ]

    generate_and_compare_credentials(input_credentials, set())


def test_order_complete_credentials_first_1():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=None, secret=SECRETS[5]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    ]

    generated_credentials = generate_brute_force_credentials(input_credentials)

    assert set(generated_credentials[0:2]) == {input_credentials[0], input_credentials[2]}


def test_generate_with_secret_type_filter():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
        Credentials(identity=None, secret=SECRETS[4]),
        Credentials(identity=None, secret=SECRETS[5]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[4]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[4]),
    }

    generate_and_compare_credentials(
        input_credentials,
        expected_credentials,
        secret_filter=lambda secret: type(secret) in {LMHash, NTHash},
    )


def test_generate_with_secret_type_filter_order():
    input_credentials = [
        Credentials(identity=None, secret=SECRETS[4]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[2]),
    ]

    generated_credentials = generate_brute_force_credentials(
        input_credentials, secret_filter=lambda secret: type(secret) is Password
    )
    assert set(generated_credentials[0:2]) == {input_credentials[1], input_credentials[2]}


def test_generate_with_identity_filter():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[1]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[2]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    ]
    expected_credentials = {
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[1]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[2]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[3]),
    }

    generate_and_compare_credentials(
        input_credentials,
        expected_credentials,
        identity_filter=lambda identity: identity == IDENTITIES[0],
    )


def test_generate_with_identity_filter_order():
    input_credentials = [
        Credentials(identity=IDENTITIES[0], secret=SECRETS[0]),
        Credentials(identity=IDENTITIES[0], secret=SECRETS[1]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[2]),
        Credentials(identity=IDENTITIES[2], secret=SECRETS[3]),
    ]

    generated_credentials = generate_brute_force_credentials(
        input_credentials, identity_filter=lambda identity: identity == IDENTITIES[0]
    )
    assert set(generated_credentials[0:2]) == {input_credentials[0], input_credentials[1]}


@pytest.mark.parametrize(
    "secret_type_filter,expected_secrets",
    [
        (
            secret_type_filter([Password]),
            [SECRETS[0], SECRETS[1], SECRETS[2]],
        ),
        (
            secret_type_filter([LMHash]),
            [SECRETS[3]],
        ),
        (
            secret_type_filter([LMHash, NTHash]),
            [SECRETS[3], SECRETS[4]],
        ),
        (
            secret_type_filter([LMHash, Password]),
            [SECRETS[0], SECRETS[1], SECRETS[2], SECRETS[3]],
        ),
    ],
)
def test_secret_type_filter(
    secret_type_filter: secret_type_filter,
    expected_secrets: List[Secret],
):
    filtered_secrets: Iterable[Secret] = filter(secret_type_filter, SECRETS)

    assert list(filtered_secrets) == expected_secrets


@pytest.mark.parametrize(
    "identity_type_filter,expected_identities",
    [
        (
            identity_type_filter([Username]),
            [IDENTITIES[0], IDENTITIES[2]],
        ),
        (
            identity_type_filter([EmailAddress]),
            [IDENTITIES[3]],
        ),
        (
            identity_type_filter([Username, EmailAddress]),
            [IDENTITIES[0], IDENTITIES[2], IDENTITIES[3]],
        ),
    ],
)
def test_identity_type_filter(
    identity_type_filter: identity_type_filter,
    expected_identities: List[Identity],
):
    filtered_secrets: Iterable[Identity] = filter(identity_type_filter, IDENTITIES)

    assert list(filtered_secrets) == expected_identities
