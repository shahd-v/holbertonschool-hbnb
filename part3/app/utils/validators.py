import re


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not isinstance(email, str) or not re.match(email_regex, email):
        raise ValueError('Invalid email format')
    return True

def validate_input_length(value):
    if len(value) < 1 or len(value) > 50:
        raise ValueError('Input must be 1 to 50 characters')
    return True

def validate_empty_input(value):
    if len(value) < 1:
        raise ValueError("Input can not be empty")
    return True

def validate_price(price):
    if price < 1:
        raise ValueError('Invalid price')
    return True

def validate_rating(rating):
    if rating < 1 or rating > 5:
        raise ValueError('Rating must be 1 to 5')
    return True

def validate_lat_and_long(latitude, longitude):
    if latitude is None or latitude < -90 or latitude > 90:
        raise ValueError('Invalid latitude')
    if longitude is None or longitude < -180 or longitude > 180:
        raise ValueError('Invalid longitude')
    return True



# I changed the validation from decorators to
# schema based.
# def email_validator(f):
#     """Decorator for validate_email"""
#     def wrapper(self, key, value):
#         try:
#             validate_email(value)
#             return f(self, key, value)
#         except ValueError as e:
#             abort(400, str(e))
#     return wrapper


# def legth_validator(f):
#     """Decorator for validate_empty_input"""
#     def wrapper(self, key, value):
#         try:
#             validate_empty_input(value)
#             return f(self, key, value)
#         except ValueError as e:
#             abort(400, str(e))
#     return wrapper
