from typing import Iterable, Set

from tests.propagation_credentials import IDENTITIES, SECRETS

from common.credentials import Credentials
from plugintoolbox import generate_brute_force_credentials


def generate_and_compare_credentials(
    input_credentials: Iterable[Credentials], expected_credentials: Set[Credentials]
):
    generated_credentials = generate_brute_force_credentials(input_credentials)

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
