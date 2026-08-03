from flask_restx import abort

from app.models.admin import Admin
from app.models.amenity import Amenity
from app.models.owner import Owner
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.owner_repo = InMemoryRepository()
        self.admin_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- User ----------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.get_user_by_email(user.email)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            abort(400, message='User not found')
        return user

    def get_user_by_email(self, email):
        user = self.user_repo.get_by_attribute('email', email)
        if user:
            abort(400, message='Email already registered')
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        # old implemntation now in get_user
        # user = self.user_repo.get(user_id)
        # if not user:
        #     abort(404, message='User not found')
        user.update_profile(user_data)
        return user

    def delete_user(self, user_id):
        """Delete a user."""
        raise NotImplementedError


    # ---------------- Admin ----------------
    def create_admin(self, admin_data):
        admin = Admin(**admin_data)
        self.admin_repo.add(admin)
        return admin

    def get_admin(self, admin_id):
        admin = self.admin_repo.get(admin_id)
        if not admin:
            abort(404, message='Admin not found')
        return admin

    def get_admin_by_email(self, email):
        admin = self.admin_repo.get_by_attribute('email', email)
        if admin:
            abort(400, message='Email already registered')
        return admin

    def get_all_admins(self):
        return self.admin_repo.get_all()

    def update_admin(self, admin_id, admin_data):
        admin = self.get_admin(admin_id)
        admin.update_profile(admin_data)
        return admin

    # ---------------- Owner ----------------
    def create_owner(self, owner_data):
        owner = Owner(**owner_data)
        self.get_owner_by_email(owner.email)
        self.owner_repo.add(owner)
        return owner

    def get_owner(self, owner_id):
        owner = self.owner_repo.get(owner_id)
        if not owner:
            abort(404, message='Owner not found')
        return owner

    def get_owner_by_email(self, email):
        owner = self.owner_repo.get_by_attribute('email', email)
        if owner:
            abort(400, message='Email already registered')
        return owner

    def get_all_owners(self):
        return self.owner_repo.get_all()

    def update_owner(self, owner_id, owner_data):
        owner = self.get_owner(owner_id)
        owner.update_profile(owner_data)
        return owner


    # ---------------- Amenity ----------------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        user = self.amenity_repo.get(amenity_id)
        if not user:
            abort(400, message='Amenity not found')

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = get_amenity(amenity_id)
        amenity.update(amenity_data)
        return amenity

    # ---------------- Place ----------------
    def create_place(self, place_data):
        # old implemntation new in model
        # price = place_data.get('price')
        # latitude = place_data.get('latitude')
        # longitude = place_data.get('longitude')
        #
        # if price is None or price < 0:
        #     raise ValueError("Invalid price")
        # if latitude is None or latitude < -90 or latitude > 90:
        #     raise ValueError("Invalid latitude")
        # if longitude is None or longitude < -180 or longitude > 180:
        #     raise ValueError("Invalid longitude")

        owner_id = place_data.get('owner_id')
        self.get_owner(owner_id)
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            abort(400, message='Place nat found')
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        """Delete a place."""
        raise NotImplementedError

    # ---------------- Review ----------------
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
            abort(400, message='Invalid input data')
        review = Review(
            review_data['rating'],
            review_data['comment'],
            place,
            user
        )
        self.review_repo.add(review)
        place.add_review(review)              # link it to the place
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            abort(400, message='Invalid input data')
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        reviews = [rev for rev in self.review_repo.get_all()
            if rev.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        review.update_rev(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
