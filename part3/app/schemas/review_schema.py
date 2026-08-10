from app.utils.validators import (
    validate_empty_input,
    validate_input_length,
    validate_rating,
)


class ReviewCreateSchema:
    """Schema validates the creation of review."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        required_fields = ['rating', 'comment', 'place', 'user']

        for field in required_fields:
            if field not in data:
                errors[field] = f"Missing required field: {field}"
        if errors:
            raise ValueError(errors)

        try:
            validate_rating(data['rating'])
        except ValueError as e:
            errors['rating'] = str(e)
        try:
            validate_empty_input(data['comment'])
        except ValueError as e:
            errors['comment'] = str(e)

        if errors:
            raise ValueError(errors)

        return True


class ReviewUpdateSchema:
    """Schema validates the updating of review."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        if not data:
            raise ValueError('At least one field is required')

        name = data.get('name')
        if name:
            try:
                validate_input_length(data['name'])
            except ValueError as e:
                errors['name'] = str(e)

        description = data.get('description')
        if description:
            try:
                validate_empty_input(data['description'])
            except ValueError as e:
                errors['description'] = str(e)

        if errors:
            raise ValueError(errors)

        return True
