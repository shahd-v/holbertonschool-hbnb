from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('admin', description='Admin operations')

# Input model for creating an admin (validation + Swagger docs)
admin_model = api.model('Admin', {
    'first_name': fields.String(required=True, description='First name of the admin'),
    'last_name': fields.String(required=True, description='Last name of the admin'),
    'email': fields.String(required=True, description='Email of the admin'),
    'password': fields.String(required=True, description='Password of the admin')
})


@api.route('/')
class AdminList(Resource):
    @api.expect(admin_model, validate=True)
    @api.response(201, 'Admin successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new admin"""
        admin_data = api.payload

        existing_admin = facade.get_admin_by_email(admin_data['email'])
        if existing_admin:
            return {'error': 'Email already registered'}, 400

        new_admin = facade.create_admin(admin_data)
        return {
            'id': new_admin.id,
            'first_name': new_admin.first_name,
            'last_name': new_admin.last_name,
            'email': new_admin.email
        }, 201

    @api.response(200, 'List of admins retrieved successfully')
    def get(self):
        """Retrieve the list of all admins"""
        admins = facade.get_all_admins()
        return [
            {
                'id': admin.id,
                'first_name': admin.first_name,
                'last_name': admin.last_name,
                'email': admin.email
            } for admin in admins
        ], 200


@api.route('/<admin_id>')
class AdminResource(Resource):
    @api.response(200, 'Admin details retrieved successfully')
    @api.response(404, 'Admin not found')
    def get(self, admin_id):
        """Get admin details by ID"""
        admin = facade.get_admin(admin_id)
        if not admin:
            return {'error': 'Admin not found'}, 404
        return {
            'id': admin.id,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'email': admin.email
        }, 200

    @api.expect(admin_model)
    @api.response(200, 'Admin updated successfully')
    @api.response(404, 'Admin not found')
    @api.response(400, 'Invalid input data')
    def put(self, admin_id):
        """Update an admin's information"""
        admin_data = api.payload
        admin = facade.get_admin(admin_id)
        if not admin:
            return {'error': 'Admin not found'}, 404

        facade.update_admin(admin_id, admin_data)
        updated = facade.get_admin(admin_id)
        return {
            'id': updated.id,
            'first_name': updated.first_name,
            'last_name': updated.last_name,
            'email': updated.email
        }, 200
