import re


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not isinstance(email, str):
        return False
    return re.match(email_regex, email) is not None
