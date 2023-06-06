use ArtworkDB;

CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(255),
    email VARCHAR(255),
    avatar VARCHAR(255),
    password VARCHAR(255),
    create_at DATETIME
);

CREATE TABLE artist (
    slug NVARCHAR(255) PRIMARY KEY,
    name NVARCHAR(255),
    biography TEXT,
    avatar VARCHAR(512)
);

CREATE TABLE artwork (
    slug NVARCHAR(255) PRIMARY KEY,
    artwork_name NVARCHAR(255),
    artist_slug NVARCHAR(255),
    price MONEY,
    size_in NVARCHAR(255),
    size_cm NVARCHAR(255),
    description TEXT,
    additional_information TEXT,
    material NVARCHAR(255),
    medium NVARCHAR(255),
    image NVARCHAR(max),
    FOREIGN KEY (artist_slug) REFERENCES artist(slug),
);

CREATE TABLE user_liked_artist (
    user_id INT,
    artist_slug NVARCHAR(255),
    create_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (artist_slug) REFERENCES artist(slug),
    PRIMARY KEY (user_id, artist_slug)
);

CREATE TABLE user_liked_artwork(
    user_id INT,
    artwork_slug NVARCHAR(255),
    create_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (artwork_slug) REFERENCES artwork(slug),
    PRIMARY KEY (user_id, artwork_slug)
);

CREATE TABLE user_order(
    order_id INT IDENTITY(1, 1) PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_order_item (
    order_id INT,
    artwork_slug NVARCHAR(255),
    FOREIGN KEY (artwork_slug) REFERENCES artwork(slug),
    FOREIGN KEY (order_id) REFERENCES user_order(order_id),
    PRIMARY KEY (order_id, artwork_slug)
);
