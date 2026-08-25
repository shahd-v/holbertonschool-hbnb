from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import Forbidden

from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        
        review_data = api.payload
        review_data['user_id'] = current_user

        # rating = review_data.get('rating')
        # if not validate_rating(rating):
        #     return {'error': 'Invalid input data'}, 400

        try:
            from app.schemas.review_schema import ReviewCreateSchema
            ReviewCreateSchema.validate(review_data)

            review = facade.create_review(review_data)

            return {
                'id': review.id,
                'comment': review.comment,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': rev.id,
                'comment': rev.comment,
                'rating': rev.rating
            } for rev in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'comment': review.comment,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()
        current_user = get_jwt()

        review_data = api.payload

        if (not current_user.get('is_admin')or
                not str(current_user_id).strip() ==
                str(review_data['user_id']).strip()):
            return ('Unauthorized action'), 403
        try:
            from app.schemas.review_schema import ReviewUpdateSchema
            ReviewUpdateSchema.validate(review_data)

            review = facade.update_review(review_id, review_data)

            return {
                'id': review.id,
                'comment': review.comment,
                'rating': review.rating
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if str(current_user_id).strip() != str(review.user_id).strip():
            return ('Unauthorized action'), 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
