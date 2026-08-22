from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden

from app.services import facade

api = Namespace('owner', description='Owner operations')

# Input model for creating a owner (validation + Swagger docs)
owner_model = api.model('Owner', {
    'first_name': fields.String(required=True, description='First name of the owner'),
    'last_name': fields.String(required=True, description='Last name of the owner'),
    'email': fields.String(required=True, description='Email of the owner'),
    'password': fields.String(required=True, description='Password of the owner')
})


@api.route('/')
class Owner(Resource):
    @jwt_required()
    @api.expect(owner_model, validate=True)
    @api.response(201, 'Owner successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new owner"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        owner_data = api.payload

        try:
            from app.schemas.user_schema import UserCreateSchema
            UserCreateSchema.validate(owner_data)

            new_owner = facade.create_owner(owner_data)

            return {
                'id': new_owner.id,
                'first_name': new_owner.first_name,
                'last_name': new_owner.last_name,
                'email': new_owner.email
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of owners retrieved successfully')
    @api.response(403, 'Unauthorized action')
    def get(self):
        """Retrieve the list of all owners"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')
        owners = facade.get_all_owners()
        return [
            {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } for owner in owners
        ], 200


@api.route('/<owner_id>')
class OwnerResource(Resource):
    @api.response(200, 'Owner details retrieved successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Owner not found')
    def get(self, owner_id):
        """Get owner details by ID"""
        current_user = get_jwt()
        current_user_id = get_jwt_identity()

        if (not current_user.get('is_admin') or
                not str(current_user_id).strip() == str(owner_id).strip()):
            raise Forbidden('Unauthorized action')

        owner = facade.get_owner(owner_id)
        return {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        }, 200

    @api.expect(owner_model)
    @api.response(200, 'Owner updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Owner not found')
    def put(self, owner_id):
        """Update a owner's information"""
        current_user = get_jwt()
        current_user_id = get_jwt_identity()

        if (not current_user.get('is_admin') or
                not str(current_user_id).strip() == str(owner_id).strip()):
            raise Forbidden('Unauthorized action')

        owner_data = api.payload
        try:

            from app.schemas.owner_schema import OwnerUpdateSchema
            OwnerUpdateSchema.validate(owner_data)

            owner = facade.update_owner(owner_id, owner_data)
            return {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }, 200

        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Owner deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Owner not found')
    def delete(self, owner_id):
        """Delete a owner"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')
        facade.get_owner(owner_id)
        facade.delete_owner(owner_id)
        return {'message': 'Owner deleted successfully'}, 200
