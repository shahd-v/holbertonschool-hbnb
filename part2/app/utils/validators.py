import re


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not isinstance(email, str):
        return False
    return re.match(email_regex, email) is not None

def validate_empty_input(data):
    # if not data:
    #     return False
    if len(data) < 1 or len(data) > 50:
        return False
    return True
def validate_price(data):
    if data < 1:
        return False
    return True

def validate_rating(data):
    if data < 1 or data > 5:
        return False
    return True







    
