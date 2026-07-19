# HBnB Evolution — Part 2: Business Logic and API

## Introduction

This part implements the **Business Logic** and **Presentation** layers of the
HBnB application, turning the UML design from Part 1 into working code.

The application is built with **Python**, **Flask**, and **flask-restx**, and
exposes a RESTful API for managing users, owners, admins, places, reviews, and
amenities. Data is held in an **in-memory repository** for now; it will be
replaced by a database in Part 3. Authentication and role-based access control
are also deferred to Part 3.

---

## Project Structure

```
part2/
├── app/
│   ├── __init__.py            # Flask app factory, registers API namespaces
│   ├── api/                   # Presentation layer
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── owner.py
│   │       ├── admin.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/                # Business Logic layer
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── admin.py
│   │   ├── owner.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/              # Facade layer
│   │   ├── __init__.py        # shared facade instance
│   │   └── facade.py
│   ├── persistence/           # Persistence layer
│   │   ├── __init__.py
│   │   └── repository.py      # in-memory repository
│   └── utils/
│       └── validators.py      # email validation helper
├── tests/                     # unit tests (unittest)
│   ├── test_users.py
│   ├── test_owner.py
│   ├── test_admin.py
│   ├── test_places.py
│   ├── test_reviews.py
│   └── test_amenities.py
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## Architecture

The project follows the **three-layer architecture** designed in Part 1:

- **Presentation Layer** (`app/api/`) — defines the REST endpoints with
  flask-restx. It handles requests, input validation, and status codes. It
  contains no business rules.
- **Business Logic Layer** (`app/models/`) — the core entities and the rules
  that govern them.
- **Persistence Layer** (`app/persistence/`) — stores and retrieves objects. The
  `InMemoryRepository` provides `add`, `get`, `get_all`, `update`, `delete`, and
  `get_by_attribute`.

### The Facade pattern

The layers never talk to each other directly. All communication goes through the
**`HBnBFacade`** (`app/services/facade.py`), a single unified interface:

```
API endpoint  ->  Facade  ->  Repository
```

The API depends only on the Facade, not on individual models or repositories.
This keeps the layers decoupled, so the in-memory storage can be swapped for a
database in Part 3 without touching the endpoints.

A single shared facade instance lives in `app/services/__init__.py`, so every
endpoint operates on the same data. The Facade holds one repository per entity:
`user_repo`, `owner_repo`, `admin_repo`, `place_repo`, `review_repo`, and
`amenity_repo`.

---

## Business Logic Entities

All entities inherit from **`BaseModel`**, which provides:

- `id` — a UUID4 string, unique per object
- `created_at` / `updated_at` — audit timestamps
- `save()` — refreshes `updated_at`
- `update(data)` — updates attributes from a dictionary, then saves
- `_store()` — per-class in-memory instance list

| Entity | Attributes | Key methods |
|--------|------------|-------------|
| **User** | `first_name`, `last_name`, `email`, `password` | `register()`, `update_profile(data)` |
| **Admin** (extends User) | inherited from User | Management methods that delegate to the Facade: `get_all_users()`, `get_user()`, `create_user()`, `update_user()` — and the equivalents for places, amenities, and reviews |
| **Owner** (extends User) | `places` | `add_place(place)`, `list_places()` |
| **Place** | `title`, `description`, `price`, `latitude`, `longitude`, `owner_id`, `reviews`, `amenities` | `create()`, `list()`, `add_review(review)`, `add_amenity(amenity)` |
| **Review** | `rating`, `comment`, `place`, `user` | `create()`, `list_by_place(place)` |
| **Amenity** | `name`, `description` | `create()`, `list()` |

### Relationships

- A **User/Owner** can own many **Places** (one-to-many). A place stores its
  `owner_id`.
- A **Place** can have many **Reviews** (one-to-many), held in `place.reviews`.
- A **Place** can have many **Amenities**, and an amenity can belong to many
  places (many-to-many), held in `place.amenities`.
- A **Review** belongs to exactly one **Place** and one **User**.

---

## API Endpoints

Base URL: `http://127.0.0.1:5000/api/v1`

### Users

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/users/` | Register a new user | 201, 400 |
| GET | `/users/` | List all users | 200 |
| GET | `/users/<user_id>` | Get a user by ID | 200, 404 |
| PUT | `/users/<user_id>` | Update a user | 200, 400, 404 |

### Owners

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/owner/` | Register a new owner | 201, 400 |
| GET | `/owner/` | List all owners | 200 |
| GET | `/owner/<owner_id>` | Get an owner by ID | 200, 404 |
| PUT | `/owner/<owner_id>` | Update an owner | 200, 400, 404 |

### Admins

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/admin/` | Register a new admin | 201, 400 |
| GET | `/admin/` | List all admins | 200 |
| GET | `/admin/<admin_id>` | Get an admin by ID | 200, 404 |
| PUT | `/admin/<admin_id>` | Update an admin | 200, 400, 404 |

### Amenities

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/amenities/` | Create an amenity | 201, 400 |
| GET | `/amenities/` | List all amenities | 200 |
| GET | `/amenities/<amenity_id>` | Get an amenity by ID | 200, 404 |
| PUT | `/amenities/<amenity_id>` | Update an amenity | 200, 400, 404 |

### Places

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/places/` | Create a place | 201, 400 |
| GET | `/places/` | List all places | 200 |
| GET | `/places/<place_id>` | Get a place by ID | 200, 404 |
| PUT | `/places/<place_id>` | Update a place | 200, 400, 404 |
| GET | `/places/<place_id>/reviews` | List all reviews for a place | 200, 404 |

### Reviews

| Method | Endpoint | Description | Status codes |
|--------|----------|-------------|--------------|
| POST | `/reviews/` | Create a review | 201, 400 |
| GET | `/reviews/` | List all reviews | 200 |
| GET | `/reviews/<review_id>` | Get a review by ID | 200, 404 |
| PUT | `/reviews/<review_id>` | Update a review | 200, 400, 404 |
| DELETE | `/reviews/<review_id>` | Delete a review | 200, 404 |

> **Note:** Reviews are the only entity that supports `DELETE` in Part 2. In the
> Facade, `delete_user` and `delete_place` intentionally raise
> `NotImplementedError`.

---

## Validation

Validation happens at three levels:

**Request level** — flask-restx models (`@api.expect(model, validate=True)`)
reject requests with missing or malformed fields, returning `400`.

**Model level** — `User` validates the email format using
`app/utils/validators.py` and raises `ValueError` on an invalid address. Because
`Owner` and `Admin` extend `User`, they inherit this check.

**Facade level**
- `create_place` validates that `price` is non-negative, `latitude` is between
  -90 and 90, and `longitude` is between -180 and 180, raising `ValueError`
  otherwise.
- `create_review` verifies that the supplied `user_id` and `place_id` refer to
  existing records before creating the review.

**Endpoint level** — user, owner, and admin registration check that the email is
not already in use and return `400` if it is.

Passwords are accepted on input but **never returned** in any API response.

---

## Installation

```bash
cd part2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Application

```bash
python run.py
```

The API runs at `http://127.0.0.1:5000/`.

### Interactive API documentation

flask-restx generates Swagger documentation automatically:

```
http://127.0.0.1:5000/api/v1/
```

Every endpoint can be browsed and tried from that page.

---

## Testing

### Unit tests

The `tests/` directory contains `unittest` suites for the endpoints. Each suite
builds the application with `create_app()` and issues requests through Flask's
test client, covering both valid requests and invalid input.

Run all tests:

```bash
python -m unittest discover tests
```

Run a single suite:

```bash
python -m unittest tests.test_users
```

### Manual testing with cURL

Create a user:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "pass123"}'
```

Expected response:

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

List all users:

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

Create an amenity:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi", "description": "High speed internet"}'
```

Create a review:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"comment": "Great stay!", "rating": 5, "user_id": "<user_id>", "place_id": "<place_id>"}'
```

Delete a review:

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
```

### Error handling

Invalid input returns `400`:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "", "last_name": "", "email": "invalid-email"}'
```

A missing resource returns `404`:

```bash
curl http://127.0.0.1:5000/api/v1/users/does-not-exist
```

---

## Authors

- Mayasem Muneer
- Abdulwahab Almatrudi
- Shahad Alshahrani
