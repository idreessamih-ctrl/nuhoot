"""Symmetric encryption for storing API credentials at rest.

Uses Fernet (AES-128-CBC + HMAC-SHA256) from the ``cryptography`` library.
The encryption key is derived from ``settings.encryption_key`` (or a
default development key if not set).
"""

from __future__ import annotations

import hashlib
import base64

from cryptography.fernet import Fernet, InvalidToken

from nuhoot.config import settings


def _get_fernet() -> Fernet:
    """Return a Fernet instance derived from the configured encryption key."""
    raw = getattr(settings, "encryption_key", "") or "nuhoot-dev-key-change-in-prod"
    # Derive a 32-byte key via SHA-256, then base64-encode for Fernet.
    key = base64.urlsafe_b64encode(hashlib.sha256(raw.encode()).digest())
    return Fernet(key)


def encrypt(plaintext: str) -> str:
    """Encrypt ``plaintext`` and return a URL-safe string."""
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """Decrypt a previously encrypted string. Returns empty string on failure."""
    try:
        return _get_fernet().decrypt(ciphertext.encode()).decode()
    except (InvalidToken, Exception):
        return ""


def mask(value: str) -> str:
    """Return a masked version for display (first 4 + last 4 chars)."""
    if not value or len(value) < 12:
        return "••••••••"
    return f"{value[:4]}{'•' * 8}{value[-4:]}"
