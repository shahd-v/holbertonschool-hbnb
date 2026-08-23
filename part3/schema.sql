PRAGMA foreign_keys = 0;

DROP TABLE IF EXISTS place_amenities;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS users;

PRAGMA foreign_keys = 1;

------ USERS TABLE ----------------------------

CREATE TABLE users (
    id INTEGER(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
------ Admin TABLE ----------------------------

CREATE TABLE admins (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
------ Owner TABLE ----------------------------

CREATE TABLE owners (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
------ Place TABLE ----------------------------

CREATE TABLE places(
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES owners(id) ON DELETE CASCADE
);
------ Review TABLE ----------------------------

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    comment TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id CHAR(36),
    place_id CHAR(36),
    UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);
------ Amenity TABLE ----------------------------

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
------ Place_Amenity TABLE ----------------------------

CREATE TABLE place_amenities (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (Place_id, Amenity_id),
    CONSTRAINT fk_place FOREIGN KEY (place_id) REFERENCES places(id)
);
