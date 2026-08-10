from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Unauthorized

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
class Admin(Resource):
    @api.expect(admin_model, validate=True)
    @api.response(201, 'Admin successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new admin"""
        admin_data = api.payload
        try:
            from app.schemas.user_schema import UserCreateSchema
            UserCreateSchema.validate(user_data)

            new_admin = facade.create_admin(admin_data)

            return {
                'id': new_admin.id,
                'first_name': new_admin.first_name,
                'last_name': new_admin.last_name,
                'email': new_admin.email
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of admins retrieved successfully')
    @api.response(403, 'Unauthorized action')
    def get(self):
        """Retrieve the list of all admins"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Unauthorized('Unauthorized action')

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
    @jwt_required()
    @api.response(200, 'Admin details retrieved successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Admin not found')
    def get(self, admin_id):
        """Get admin details by ID"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Unauthorized('Unauthorized action')

        admin = facade.get_admin(admin_id)
        return {
            'id': admin.id,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'email': admin.email
        }, 200

    @api.expect(admin_model)
    @api.response(200, 'Admin updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Admin not found')
    def put(self, admin_id):
        """Update an admin's information"""
        current_user = get_jwt()

        admin_data = api.payload

        if not current_user.get('is_admin'):
            raise Unauthorized('Unauthorized action')

        admin = facade.update_admin(admin_id, admin_data)
        return {
            'id': admin.id,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'email': admin.email
        }, 200
