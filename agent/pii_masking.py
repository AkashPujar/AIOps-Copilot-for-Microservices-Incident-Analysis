import re


def mask_pii(text):
    """
    Redacts common PII patterns.
    """

    text = re.sub(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        '[EMAIL_REDACTED]',
        text
    )

    text = re.sub(
        r'\b\d{10}\b',
        '[PHONE_REDACTED]',
        text
    )

    return text