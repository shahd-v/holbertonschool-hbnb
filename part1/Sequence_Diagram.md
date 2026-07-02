## User Registration
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (post)
API->>BusinessLogic: register ()
BusinessLogic->>Database: INSERT INTO users (UUID, first_name, last_name, email, password, created_at, updated_at)
Database-->>BusinessLogic: Return new user ID and confirmation
BusinessLogic-->>API: Return user object (without password)
API-->>User: 201 Created
```
Purpose: To create a new user account.
Components: User, API (entry point), Business Logic (rules), Database (storage).
Design Choice: The system removes the password before sending data back to the user so sensitive info isn't exposed.
Architecture: A standard way to save new data safely using separate layers.

---
## Place Creation
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (post)
API->>BusinessLogic: create ()
BusinessLogic->>Database: INSERT INTO places (UUID, title, description, price, latitude, longitude, created_at, updated_at)
Database-->>BusinessLogic: Return place_id
BusinessLogic-->>API: Return created place object
API-->>User: 201 Created
```
Purpose: To add a new place to the app.
Components: User, API, Business Logic, Database.
Design Choice: Stores price and location so users can search for places later.
Architecture: A basic way to build the main content (Places) that other features rely on.

---
## Review Submission
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (post)
API->>BusinessLogic: create ()
BusinessLogic->>Database: INSERT INTO reviews (UUID, rating, comment, created_at, updated_at)
Database-->>BusinessLogic: Return review_id
BusinessLogic-->>API: Return created review object
API-->>User: 201 Created
```
Purpose: To let a user leave a review or rating.
Components: User, API, Business Logic, Database.
Design Choice: Connects the review to a specific place using an ID so the system knows what is being reviewed.
Architecture: Adds extra info (user feedback) to existing content (places).

---
## Fetching a List of Places
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (GET)
API->>BusinessLogic: list ()
BusinessLogic->>Database: SELECT * FROM places WHERE price BETWEEN 2000 AND 5000
Database-->>BusinessLogic: Return matching places
loop
BusinessLogic->>Database: SELECT * FROM reviews WHERE place_id = place.id
BusinessLogic->>Database: SELECT * FROM amenities WHERE place_id = place.id
end
BusinessLogic-->>API: Return list of place objects with reviews and amenities
API-->>User: 200 OK
```
Purpose: To show a list of places with all their extra details.
Components: User, API, Business Logic, Database.
Design Choice: The system grabs the place, then goes back to the database to grab reviews and amenities so the user gets everything in one go.
Architecture: A way to turn simple database rows into a complete package that is easy for a website or app to display.
