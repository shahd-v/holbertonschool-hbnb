from flask_bcrypt import check_password_hash, generate_password_hash

from app import db
from app.models.base_model import BaseModel


class User(BaseModel):

    # this is not needed because we can
    # ask the database using the user repo
    # if the admin exest in the admin table
    # is_admin = False

    __tablename__ = 'Users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    # I found that vahlidating input farmat is best put
    # in the api to check inputs even before creating
    # the opjects so I moved it to the api
    # @validates('first_name', 'last_name', 'password')
    # @non_empty_validator
    # def validate_fields(self, key, value):
    #     return value
    #
    # @validates('email')
    # @email_validator
    # def validate_user_email(self, key, value):
    #     return value

    # try:
    #     validate_empty_input(first_name)
    #     validate_empty_input(last_name)
    #     validate_empty_input(password)
    # except ValueError as e:
    #     abort(400, str(e))
    # try:
    #     validate_email(email)
    # except ValueError as e:
    #     abort(400, str(e))


    def register(self):
        type(self)._store().append(self)
        return self

    def update_profile(self, data):
        self.update(data)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = generate_password_hash(password).decode('utf-8')

        # this was a mistak by me because nothing will catch the returned password
        # return generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password, password)
