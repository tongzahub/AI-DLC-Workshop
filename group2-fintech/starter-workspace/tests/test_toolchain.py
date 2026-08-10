"""Toolchain smoke test.

Asserts nothing about SwiftKYC - only that the workspace is wired up correctly, so
`python -m pytest` gives you a green result before you start. Delete it once you have real
tests, or leave it; it costs nothing.
"""
import os
import sys


def test_runs_on_python_312_or_newer() -> None:
    assert sys.version_info[:2] >= (3, 12)


def test_required_libraries_are_installed() -> None:
    import fastapi  # noqa: F401
    import httpx  # noqa: F401
    import pydantic  # noqa: F401
    import sqlalchemy  # noqa: F401


def test_aes_256_gcm_is_available() -> None:
    """The security baseline needs real crypto, never a home-made cipher."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    secret = b"1103700123456"
    assert aes.decrypt(nonce, aes.encrypt(nonce, secret, None), None) == secret
