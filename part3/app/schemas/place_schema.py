from app.utils.validators import (
    validate_empty_input,
    validate_input_length,
    validate_lat_and_long,
    validate_price
)


class PlaceCreateSchema:
    """Schema validates the creation of place."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        required_fields = ['title', 'description',
                           'price', 'latitude',
                           'longitude']

        for field in required_fields:
            if field not in data:
                errors[field] = f"Missing required field: {field}"
        if errors:
            raise ValueError(errors)

        try:
            validate_input_length(data['title'])
        except ValueError as e:
            errors['title'] = str(e)
        try:
            validate_empty_input(data['description'])
        except ValueError as e:
            errors['description'] = str(e)
        try:
            validate_price(data['price'])
        except ValueError as e:
            errors['price'] = str(e)
        try:
            validate_lat_and_long(data['latitude'], data['longitude'])
        except ValueError as e:
            errors['latitude', 'longitude'] = str(e)

        if errors:
            raise ValueError(errors)

        return True


class PlaceUpdateSchema:
    """Schema validates the updating of place."""

    @staticmethod
    def validate(data):
        """Validates fields of the payload."""
        errors = {}

        if not data:
            raise ValueError('At least one field is required')

        p_title = data.get('title')
        if p_title:
            try:
                validate_input_length(data['title'])
            except ValueError as e:
                errors['title'] = str(e)

        p_desc = data.get('description')
        if p_desc:
            try:
                validate_empty_input(data['description'])
            except ValueError as e:
                errors['description'] = str(e)

        p_price = data.get('price')
        if p_price:
            try:
                validate_price(data['price'])
            except ValueError as e:
                errors['price'] = str(e)


        if errors:
            raise ValueError(errors)

        return True
