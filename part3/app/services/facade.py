from werkzeug.exceptions import NotFound

from app.persistence.admin_repository import AdminRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.owner_repository import OwnerRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.owner_repo = OwnerRepository()
        self.admin_repo = AdminRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ---------------- User ----------------
    def create_user(self, user_data):
        from app.models.user import User
        user = User(**user_data)
        if self.get_user_by_email(user.email):
            raise ValueError('Email already registered')
        user.hash_password(user.password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError('User not found')
        return user

    def get_user_by_email(self, email):
        user = self.user_repo.get_by_attribute('email', email)
        # if not user:
        #     abort(400, message='User not found')
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)

        user.update_profile(user_data)
        return user
        # old implementation now in get_user
        # user = self.user_repository.get(user_id)
        # if not user:
        #     abort(404, message='User not found')

    def delete_user(self, user_id):
        """Delete a user."""
        self.get_user(user_id)
        self.user_repo.delete(user_id)


    # ---------------- Admin ----------------
    def create_admin(self, admin_data):
        from app.models.admin import Admin
        admin = Admin(**admin_data)
        if self.get_admin_by_email(admin.email):
            raise ValueError('Email already registered')
        admin.hash_password(admin.password)
        self.admin_repo.add(admin)
        return admin

    def get_admin(self, admin_id):
        admin = self.admin_repo.get(admin_id)

        if not admin:
            raise NotFound('Admin not found')
        return admin

    def get_admin_by_email(self, email):
        return self.admin_repo.get_by_attribute('email', email)

    def get_all_admins(self):
        return self.admin_repo.get_all()

    def update_admin(self, admin_id, admin_data):
        admin = self.get_admin(admin_id)

        if not admin:
            raise NotFound('Admin not found')

        admin.update_profile(admin_data)
        return admin

    def is_admin(self, id):
        return self.admin_repo.check_is_admin(id)


    # ---------------- Owner ----------------
    def create_owner(self, owner_data):
        from app.models.owner import Owner
        owner = Owner(**owner_data)
        if self.get_owner_by_email(owner.email):
            raise ValueError('Email already registered')
        owner.hash_password(owner.password)
        self.owner_repo.add(owner)
        return owner

    def get_owner(self, owner_id):
        owner = self.owner_repo.get(owner_id)
        if not owner:
            raise NotFound('Owner not found')
        return owner

    def get_owner_by_email(self, email):
        return self.owner_repo.get_by_attribute('email', email)

    def get_all_owners(self):
        return self.owner_repo.get_all()

    def update_owner(self, owner_id, owner_data):
        owner = self.get_owner(owner_id)
        owner.update_profile(owner_data)
        return owner

    def is_owner(self, id):
        return self.owner_repo.check_is_owner(id)

    def delete_owner(self, owner_id):
        """Delete a owner."""
        self.get_owner(owner_id)
        self.owner_repo.delete(owner_id)


    # ---------------- Amenity ----------------
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        if self.get_amenity(amenity.id):
            raise ValueError('Amenity already exists')
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        amenity.save()
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete a amenity."""
        self.get_amenity(amenity_id)
        self.amenity_repo.delete(amenity_id)

    # ---------------- Place ----------------
    def create_place(self, place_data):
        from app.models.place import Place
        # old implementation new in model
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
            raise NotFound('Place nat found')
        return place

    def get_place_by_title(self, title):
        return self.place_repo.get_by_attribute('title', title)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        """Delete a place."""
        self.get_place(place_id)
        self.place_repo.delete(place_id)


    # ---------------- Review ----------------
    def create_review(self, review_data):
        from app.models.review import Review
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
            raise ValueError('Invalid input data')
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
            raise ValueError('Invalid input data')
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = [rev for rev in self.review_repo.get_all()
            if rev.place.id == place_id]
        return reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        review.update_rev(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise NotFound('Review not found')
        self.review_repo.delete(review_id)
        return review
