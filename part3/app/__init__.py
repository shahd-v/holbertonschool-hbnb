from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.owner import api as owner_ns
from app.api.v1.admin import api as admin_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')
    bcrypt.init_app(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(owner_ns, path='/api/v1/owner')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
