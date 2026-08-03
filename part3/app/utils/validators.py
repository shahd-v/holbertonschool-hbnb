import re


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not isinstance(email, str):
        return False
    return re.match(email_regex, email) is not None


def validate_empty_input(data):
    if not isinstance(data, str):
        return False
    return 1 <= len(data) <= 50


def validate_price(data):
    try:
        return data is not None and float(data) >= 1
    except (TypeError, ValueError):
        return False


def validate_rating(data):
    try:
        numeric = int(data)
    except (TypeError, ValueError):
        return False
    return 1 <= numeric <= 5







    
