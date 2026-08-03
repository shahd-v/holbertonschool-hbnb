from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.utils.validators import validate_email

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate a user and return a JWT access token"""
        login_data = api.payload or {}
        email = login_data.get('email')
        password = login_data.get('password')

        if not email or not password or not validate_email(email):
            return {'error': 'Invalid credentials'}, 400

        user = facade.get_user_by_email(email) or facade.get_owner_by_email(email) or facade.get_admin_by_email(email)
        if not user or user.password != password:
            return {'error': 'Invalid credentials'}, 400

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
