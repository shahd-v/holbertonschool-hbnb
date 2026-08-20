from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden

from app.services import facade

api = Namespace('users', description='User operations')

# Input model for creating a user (validation + Swagger docs)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Bad request')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        try:

            # this is like a blueprint for how the user data 
            # should look like
            from app.schemas.user_schema import UserCreateSchema
            UserCreateSchema.validate(user_data)

            new_user = facade.create_user(user_data)

            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

        except ValueError as e:
            return {'message': str(e)}, 400
        # old implementation now in model
        # existing_user = facade.get_user_by_email(user_data['email'])
        # if existing_user:
        #     return {'error': 'Email already registered'}, 400
        # email = user_data.get('email')
        # if not validate_email(email):
        #     return {'error': 'Invalid email format'}, 400



    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Unauthorized action')
    def get(self):
        """Retrieve the list of all users"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        user = facade.get_user(user_id)
        # old implementation now in facade
        # if not user:
        #     return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Input must be 1 to 50 characters; Input can not be empty;\
                         Invalid email format')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt()

        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')

        user_data = api.payload

        try:

            from app.schemas.user_schema import UserUpdateSchema
            UserUpdateSchema.validate(user_data)

            user = facade.update_user(user_id, user_data)

            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200

        except ValueError as e:
            return {'message': str(e)}, 400

        # old implementations now it's all in the model
        # if not user:
        #      return {'error': 'User not found'}, 404
        # user = facade.get_user(user_id)
        # if not user:
        #     return {'error': 'User not found'}, 404
        #
        # facade.update_user(user_id, user_data)
        # updated = facade.get_user(user_id)

    @api.response(200, 'User deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Forbidden('Unauthorized action')
        facade.get_user(user_id)
        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
