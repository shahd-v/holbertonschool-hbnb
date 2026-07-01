
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
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (post)
API->>BusinessLogic: create ()
BusinessLogic->>Database: INSERT INTO places (UUID, title, description, price, latitude, longitude, created_at, updated_at)
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API-->>User: Return Success/Failure
```

#### Review Submission
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (post)
API->>BusinessLogic: create ()
BusinessLogic->>Database: INSERT INTO reviews (UUID, rating, comment, created_at, updated_at)
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API-->>User: Return Success/Failure
```


#### Fetching a List of Places
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (GET)
API->>BusinessLogic: list ()
BusinessLogic->>Database: SELECT * FROM places WHERE price BETWEEN 2000 AND 5000
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API-->>User: Return Success/Failure
```

## API ( Usage & Description )

## Authors
- Mayasem Muneer
- Abdulwahab Almatrudi
- Shahad Alshahrani
