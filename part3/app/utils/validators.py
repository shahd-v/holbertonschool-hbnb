import re


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not isinstance(email, str):
        raise ValueError('Invalid email format')
    return re.match(email_regex, email) is not None

def validate_empty_input(data):
    # if not data:
    #     return False
    if len(data) < 1 or len(data) > 50:
        raise ValueError('Invalid input data')
    return True
def validate_price(data):
    if data < 1:
        raise ValueError('Invalid price')
    return True

def validate_rating(data):
    if data < 1 or data > 5:
        raise ValueError('Invalid rating')
    return True

    def validate_lat_and_long(latitude,longitude):
        if latitude is None or latitude < -90 or latitude > 90:
            raise ValueError('Invalid latitude')
        if longitude is None or longitude < -180 or longitude > 180:
            raise ValueError('Invalid longitude')
