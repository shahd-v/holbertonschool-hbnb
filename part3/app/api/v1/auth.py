from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate any account type and return a JWT token"""
        credentials = api.payload            # Get the email and password from the request payload
        email = credentials['email']

        # Step 1: Retrieve the account by email, checking each account type.
        #         get_*_by_email returns None when not found, so the `or`
        #         chain falls through to the next repo. The first match wins.
        account = (
            facade.get_user_by_email(email)
            or facade.get_owner_by_email(email)
            or facade.get_admin_by_email(email)
        )

        # Step 2: Check the account exists AND the password is correct.
        #         One check covers all three types.
        if (not account or
            not account.verify_password(credentials['password'].replace('Bearer ', '', 1)
                                        if credentials['password'].startswith('Bearer ')
                                        else credentials['password'])):
            return {'error': 'Invalid credentials'}, 401

        is_admin = facade.is_admin(account.id)
        is_owner = facade.is_owner(account.id)

        if is_admin:
            access_token = create_access_token(
                identity=str(account.id),
                additional_claims={'is_admin': True, 'is_owner': False}
            )
        elif is_owner:
            access_token = create_access_token(
                identity=str(account.id),
                additional_claims={'is_admin': False, 'is_owner': True}
            )
        else:
            access_token = create_access_token(
                identity=str(account.id),
                additional_claims={'is_admin': False, 'is_owner': False}
            )

        # Step 4: Return the JWT token to the client.
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Step 1: Read the identity (the account id) stored in the token.
        current_user = get_jwt_identity()

        # Step 2: (Optional) read extra claims to check admin rights:
        #         from flask_jwt_extended import get_jwt
        #         claims = get_jwt()
        #         if not claims["is_admin"]:
        #             return {'error': 'Admin privileges required'}, 403

        # Step 3: Return the response.
        return {'message': f'Hello, user {current_user}'}, 200
