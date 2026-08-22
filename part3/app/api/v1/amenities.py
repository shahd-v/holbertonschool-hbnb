from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden

from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        try:

            from app.schemas.amenity_schema import AmenityCreateSchema
            AmenityCreateSchema.validate(amenity_data)

            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'description': new_amenity.description
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(403, 'Unauthorized action')
    def get(self):
        """Retrieve a list of all amenities"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'description': amenity.description
            } for amenity in amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        amenity = facade.get_amenity(amenity_id)
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'At least one field is required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        amenity_data = api.payload

        try:

            from app.schemas.amenity_schema import AmenityUpdateSchema
            AmenityUpdateSchema.validate(amenity_data)

            facade.update_amenity(amenity_id, amenity_data)
            updated = facade.get_amenity(amenity_id)
            return {
                'id': updated.id,
                'name': updated.name,
                'description': updated.description
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400
