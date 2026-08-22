from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}}) 

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')


    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your token as: Bearer <your_token>'
        }
    }
    api.authorizations = authorizations
    api.security = [{'Bearer': []}]

    bcrypt.init_app(app)

    jwt.init_app(app)
    db.init_app(app)


    from app.api.v1.admin import api as admin_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.owner import api as owner_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns


    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(owner_ns, path='/api/v1/owner')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Make sure every table exists before the first request.
    with app.app_context():
        db.create_all()

    return app
