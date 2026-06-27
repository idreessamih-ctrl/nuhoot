"""Saudi phone number formatting utilities."""

import re


def normalize_saudi_phone(phone: str) -> str:
    """Convert any Saudi phone format to +966 5X XXX XXXX.

    Handles:
      - 0501234567 → +966 50 123 4567
      - 966501234567 → +966 50 123 4567
      - +966501234567 → +966 50 123 4567
      - 501234567 → +966 50 123 4567
    """
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("966"):
        digits = digits[3:]
    elif digits.startswith("0"):
        digits = digits[1:]

    if len(digits) != 9 or not digits.startswith("5"):
        raise ValueError(f"Invalid Saudi phone number: {phone}")

    return f"+966 {digits[:2]} {digits[2:5]} {digits[5:]}"


def format_phone_for_whatsapp(phone: str) -> str:
    """Strip a phone number to pure digits for the WhatsApp Cloud API.

    WhatsApp expects the recipient in international format without '+',
    spaces, or dashes — e.g. ``966501234567``.
    """
    return re.sub(r"\D", "", phone)


def is_whatsapp_capable(phone: str) -> bool:
    """Check if a phone number can receive WhatsApp messages."""
    try:
        normalize_saudi_phone(phone)
        return True
    except ValueError:
        return False
