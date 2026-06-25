
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

## Requierment

## Environment

## Usage 

## Diagram structure

### High level Package diagram

![Package Diagram](Package%20Diagram.drawio.png)

### Class diagram

```mermaid
classDiagram
class BaseModel {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +save() void
    +update(data) void
    +delete() void
}
 
class User {
    +string first_name
    +string last_name
    +string email
    -string password
    +bool is_admin
    +register() void
    +update_profile(data) void
    +delete() void
}
 
class Place {
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +create() void
    +update(data) void
    +delete() void
    +list() List~Place~
    +add_amenity(amenity) void
}
 
class Review {
    +int rating
    +string comment
    +create() void
    +update(data) void
    +delete() void
    +list_by_place(place) List~Review~
}
 
class Amenity {
    +string name
    +string description
    +create() void
    +update(data) void
    +delete() void
    +list() List~Amenity~
}
 
BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity
 
User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : offers
```

## API ( Usage & Discription )

## Authors
- Mayasem Muneer
- Abdulwahab Almatrudi
- Shahad Fahad
