from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Unauthorized

from app.models import place
from app.services import facade

api = Namespace('places', description='Place operations')

'''Define the models for related entities'''
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

'''Define the place model for input validation and documentation'''
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Owner or admin privileges required')
    def post(self):

        current_user = get_jwt()
        if (not current_user.get('is_admin') or
                current_user.get('is_owner')):
            raise Unauthorized('Owner or admin privileges required')

        account_id = get_jwt_identity()

        """Register a new place"""
        place_data = api.payload.copy()
        place_data['owner_id'] = account_id

        from app.schemas.place_schema import PlaceCreateSchema
        PlaceCreateSchema.validate(place_data)

        existing_place = facade.get_place_by_title(place_data['title'])
        if existing_place:
            return {'error': 'Invalid input data'}, 400

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'amenities': new_place.amenities
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': place.amenities
            } for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'amenities': place.amenities
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')

    def put(self, place_id):
        """Update a place's information"""
        facade.get_place(place_id)

        current_user = get_jwt()
        if (not current_user.get('is_admin') or
                current_user.get('is_owner')):
            raise Unauthorized('Unauthorized action')

        place_data = api.payload

        try:
            from app.schemas.place_schema import PlaceUpdateSchema
            PlaceUpdateSchema.validate(place_data)

            facade.update_place(place_id, place_data)
            updated = facade.get_place(place_id)
            return {
                'id': updated.id,
                'title': updated.title,
                'description': updated.description,
                'price': updated.price,
                'latitude': updated.latitude,
                'longitude': updated.longitude,
                'amenities': updated.amenities
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            raise Unauthorized('Unauthorized action')
        facade.get_place(place_id)
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': rev.id,
                'comment': rev.comment,
                'rating': rev.rating
            } for rev in reviews
        ], 200
