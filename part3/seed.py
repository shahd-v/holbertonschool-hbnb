#!/usr/bin/env python3
"""Seed the development database with sample data for the Part 4 web client.

Usage (from the part3 directory, with the virtualenv active):

    python seed.py

Re-running it is safe: if places already exist, nothing is inserted.
Add --reset to wipe the database and start from scratch.
"""

import sys

from app import create_app, db
from app.models.amenity import Amenity
from app.models.owner import Owner
from app.models.place import Place
from app.models.review import Review
from app.models.user import User

# Accounts created by this script (use these to log in from the web client).
OWNER_EMAIL = 'owner@hbnb.io'
OWNER_PASSWORD = 'owner1234'
USER_EMAIL = 'user@hbnb.io'
USER_PASSWORD = 'user1234'


def seed():
    app = create_app()

    with app.app_context():
        if '--reset' in sys.argv:
            db.drop_all()
            print('Database dropped.')

        db.create_all()

        if Place.query.first():
            print('Database already contains places - nothing to do.')
            print('Run "python seed.py --reset" to rebuild it from scratch.')
            return

        # ---------------- Accounts ----------------
        owner = Owner(
            first_name='Sara',
            last_name='Alharbi',
            email=OWNER_EMAIL,
            password='placeholder'
        )
        owner.hash_password(OWNER_PASSWORD)

        user = User(
            first_name='Shahd',
            last_name='Faisal',
            email=USER_EMAIL,
            password='placeholder'
        )
        user.hash_password(USER_PASSWORD)

        db.session.add_all([owner, user])
        db.session.commit()

        # ---------------- Amenities ----------------
        wifi = Amenity(name='Wi-Fi', description='Fast wireless internet')
        pool = Amenity(name='Pool', description='Outdoor swimming pool')
        parking = Amenity(name='Parking', description='Free private parking')
        db.session.add_all([wifi, pool, parking])
        db.session.commit()

        # ---------------- Places ----------------
        beach = Place(
            title='Beach House',
            description='A cozy house right by the sea, sleeps four.',
            price=120,
            latitude=21,
            longitude=39,
            owner_id=owner.id
        )
        cabin = Place(
            title='Desert Cabin',
            description='A quiet cabin in the dunes, perfect for stargazing.',
            price=45,
            latitude=24,
            longitude=46,
            owner_id=owner.id
        )
        studio = Place(
            title='City Studio',
            description='A small studio in the middle of downtown.',
            price=9,
            latitude=24,
            longitude=46,
            owner_id=owner.id
        )

        beach.amenities.extend([wifi, pool, parking])
        cabin.amenities.append(wifi)
        studio.amenities.extend([wifi, parking])

        db.session.add_all([beach, cabin, studio])
        db.session.commit()

        # ---------------- Reviews ----------------
        db.session.add_all([
            Review(rating=5, comment='Amazing stay, the view was unreal!',
                   place=beach.id, user=user.id),
            Review(rating=4, comment='Very clean and quiet. Would come back.',
                   place=beach.id, user=user.id),
            Review(rating=3, comment='Nice and peaceful, but a long drive.',
                   place=cabin.id, user=user.id),
        ])
        db.session.commit()

        print('Seed complete.')
        print(f'  places   : {Place.query.count()}')
        print(f'  reviews  : {Review.query.count()}')
        print(f'  amenities: {Amenity.query.count()}')
        print()
        print('Log in from the web client with:')
        print(f'  user  -> {USER_EMAIL} / {USER_PASSWORD}')
        print(f'  owner -> {OWNER_EMAIL} / {OWNER_PASSWORD}')


if __name__ == '__main__':
    seed()
