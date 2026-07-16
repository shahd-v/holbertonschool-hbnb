from flask_restx import Namespace, Resource, fields
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
    @api.expect(owner_model, validate=True)
    @api.response(201, 'Owner successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new owner"""
        owner_data = api.payload

        existing_owner = facade.get_owner_by_email(owner_data['email'])
        if existing_owner:
            return {'error': 'Email already registered'}, 400

        new_owner = facade.create_owner(owner_data)
        return {
            'id': new_owner.id,
            'first_name': new_owner.first_name,
            'last_name': new_owner.last_name,
            'email': new_owner.email
        }, 201

    @api.response(200, 'List of owners retrieved successfully')
    def get(self):
        """Retrieve the list of all owners"""
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
    @api.response(404, 'Owner not found')
    def get(self, owner_id):
        """Get owner details by ID"""
        owner = facade.get_owner(owner_id)
        if not owner:
            return {'error': 'Owner not found'}, 404
        return {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        }, 200

    @api.expect(owner_model)
    @api.response(200, 'Owner updated successfully')
    @api.response(404, 'Owner not found')
    @api.response(400, 'Invalid input data')
    def put(self, owner_id):
        """Update a owner's information"""
        owner_data = api.payload
        owner = facade.get_owner(owner_id)
        if not owner:
            return {'error': 'Owner not found'}, 404

        facade.update_owner(owner_id, owner_data)
        updated = facade.get_owner(owner_id)
        return {
            'id': updated.id,
            'first_name': updated.first_name,
            'last_name': updated.last_name,
            'email': updated.email
        }, 200
