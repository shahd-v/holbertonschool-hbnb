from app.services import facade
from app.models.user import User


class Admin(User):
    """Admin user with capabilities to manage users, places, amenities, and reviews."""

    # ---- User management ----
    def get_all_users(self):
        """Retrieve all users."""
        return facade.get_all_users()

    def get_user(self, user_id):
        """Retrieve a specific user by ID."""
        return facade.get_user(user_id)

    def create_user(self, user_data):
        """Create a new user."""
        return facade.create_user(user_data)

    def update_user(self, user_id, user_data):
        """Update an existing user."""
        return facade.update_user(user_id, user_data)

    def delete_user(self, user_id):
        """Delete a user."""
        raise NotImplementedError

    # ---- Place management ----
    def get_all_places(self):
        """Retrieve all places."""
        return facade.get_all_places()

    def get_place(self, place_id):
        """Retrieve a specific place by ID."""
        return facade.get_place(place_id)

    def create_place(self, place_data):
        """Create a new place."""
        return facade.create_place(place_data)

    def update_place(self, place_id, place_data):
        """Update an existing place."""
        return facade.update_place(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place."""
        raise NotImplementedError

    # ---- Amenity management ----
    def get_all_amenities(self):
        """Retrieve all amenities."""
        return facade.get_all_amenities()

    def get_amenity(self, amenity_id):
        """Retrieve a specific amenity by ID."""
        return facade.get_amenity(amenity_id)

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        return facade.create_amenity(amenity_data)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity."""
        return facade.update_amenity(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        raise NotImplementedError

    # ---- Review management ----
    def get_all_reviews(self):
        """Retrieve all reviews."""
        return facade.get_all_reviews()

    def get_review(self, review_id):
        """Retrieve a specific review by ID."""
        return facade.get_review(review_id)

    def create_review(self, review_data):
        """Create a new review."""
        return facade.create_review(review_data)

    def update_review(self, review_id, review_data):
        """Update an existing review."""
        return facade.update_review(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review."""
        return facade.delete_review(review_id)
