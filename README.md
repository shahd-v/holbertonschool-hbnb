
# HBNB Project


## About 

## Table of content 
- [About](#about)
- [Description](#description)
- [Requirements](#requirements)
- [Environment](#environment)
- [Usage](#usage)
- [Diagram Structure](#diagram-structure)
- [API](#api)
- [Authors](#authors)

## Requirement

## Environment

## Usage 

## Diagram structure

### High level Package diagram

![Package Diagram](part1/Package_Diagram.drawio.png)

### Class diagram

![Class Diagram](part1/Class_Diagram.drawio.png)
---
### Sequence diagram

#### User Registration
##### User story: 
As a new User, I want to register an account with my personal details, so that I can access the platform's features as an authenticated user.
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

#### Place Creation
User story:
As a registered host, I want to list a new place with details like title, description, price, and location, so that other users can discover and book it.
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

#### Review Submission

User Story:
As a user who has visited a place, I want to submit a rating and comment, so that I can share my experience and help other users make informed decisions.

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


#### Fetching a List of Places

User Story:
As a user searching for accommodations, I want to filter places by price, so that I can quickly compare options and make a decision.

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

## API ( Usage & Description )

## Authors
- Mayasem Muneer
- Abdulwahab Almatrudi
- Shahad Alshahrani
