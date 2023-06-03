SET
    NOCOUNT ON;

GO
;

USE master;

GO
;

if exists (
    select
        *
    from
        sysdatabases
    where
        name = 'ArtworkDB'
) drop database ArtworkDB;

GO
;

/* 使用者 */
CREATE TABLE user (
    id INT PRIMARY KEY,
    username NVARCHAR(255),
    email VARCHAR(255),
    hashed_password VARCHAR(255),
    create_at DATETIME
);

/* 藝術家 */
CREATE TABLE artist (
    id INT PRIMARY KEY,
    slug NVARCHAR(255),
    name NVARCHAR(255),
    biography NVARCHAR(255),
    avatar VARCHAR(512),
);

CREATE TABLE category(
    id INT PRIMARY KEY,
    category_name NVARCHAR(255)
);

/* 我不知道 */
CREATE TABLE artwork (
    id INT PRIMARY KEY,
    artwork_name NVARCHAR(255),
    artist_id INT NOT NULL,
    price MONEY,
    size_in VARCHAR(255),
    size_cm VARCHAR(255),
    description TEXT,
    additional_information TEXT,
    category_id int,
    material VARCHAR(255),
    medium VARCHAR(255),
    FOREIGN KEY (artist_id) REFERENCES artist(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE artwork_image (
    id INT PRIMARY KEY,
    artwork_id INT,
    image_url VARCHAR(255),
    FOREIGN KEY (artwork_id) REFERENCES artwork(id)
);

/* 實體關係 */
CREATE TABLE user_liked_artist (
    user_id INT,
    artiest_id INT,
    create_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (artiest_id) REFERENCES artist(id),
    PRIMARY KEY (user_id, artiest_id)
);

CREATE TABLE user_liked_artwork(
    user_id INT,
    artwork_id INT,
    create_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (artwork_id) REFERENCES artwork(id),
    PRIMARY KEY (user_id, artiest_id)
);