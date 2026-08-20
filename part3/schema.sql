PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS Owner;
DROP TABLE IF EXISTS Places;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Users;


------ USERS TABLE ----------------------------

CREATE TABLE users (
    id INTEGER(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
    --is_admin: BOOLEAN DEFAULT FALSE
);
------ Admin TABLE ----------------------------

CREATE TABLE Admin (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
    --is_admin: BOOLEAN DEFAULT FALSE
);
------ Owner TABLE ----------------------------

CREATE TABLE Owner (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
    --is_admin: BOOLEAN DEFAULT FALSE
);
------ Place TABLE ----------------------------

CREATE TABLE Place(
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) REFERENCES Owner(id)
    
);
------ Review TABLE ----------------------------

CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) REFERENCES Users(id),
    place_id CHAR(36) REFERENCES Places(id),
    UNIQUE (user_id, place_id)
);
------ Amenity TABLE ----------------------------

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
------ Place_Amenity TABLE ----------------------------

CREATE TABLE Place_Amenity (
    Place_id CHAR(36) REFERENCES Place(id),
    Amenity_id CHAR(36) REFERENCES Amenity(id),
    PRIMARY KEY (Place_id, Amenity_id)
);
