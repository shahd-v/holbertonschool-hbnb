from app.utils.validators import (
    validate_email,
    validate_empty_input,
    validate_input_length,
)


class UserCreateSchema:
    """Schema validates the creation of user."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        required_fields = ['first_name', 'last_name',
                           'email', 'password']

        for field in required_fields:
            if field not in data:
                errors[field] = f"Missing required field: {field}"
        if errors:
            raise ValueError(errors)

        try:
            validate_input_length(data['first_name'])
        except ValueError as e:
            errors['first_name'] = str(e)
        try:
            validate_input_length(data['last_name'])
        except ValueError as e:
            errors['last_name'] = str(e)
        try:
            validate_empty_input(data['password'])
        except ValueError as e:
            errors['password'] = str(e)
        try:
            validate_email(data['email'])
        except ValueError as e:
            errors['email'] = str(e)

        if errors:
            raise ValueError(errors)

        return True


class UserUpdateSchema:
    """Schema validates the updating of user."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        if not data:
            raise ValueError('At least one field is required')

        firstn = data.get('first_name')
        if firstn:
            try:
                validate_input_length(data['first_name'])
            except ValueError as e:
                errors['first_name'] = str(e)

        lastn = data.get('last_name')
        if lastn:
            try:
                validate_input_length(data['last_name'])
            except ValueError as e:
                errors['last_name'] = str(e)

        password = data.get('password')
        if password:
            try:
                validate_empty_input(data['password'])
            except ValueError as e:
                errors['password'] = str(e)

        email = data.get('email')
        if email:
            try:
                validate_email(data['email'])
            except ValueError as e:
                errors['email'] = str(e)

        if errors:
            raise ValueError(errors)

        return True
