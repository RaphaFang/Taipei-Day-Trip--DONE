-- the user_info table

CREATE TABLE user_info (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
    username VARCHAR(255) NOT NULL COMMENT 'User name',
    password VARCHAR(255) NOT NULL COMMENT 'User password',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'User email',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Builded time'
);
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | Field      | Type         | Null | Key | Default           | Extra             |
-- +------------+--------------+------+-----+-------------------+-------------------+
-- | id         | int          | NO   | PRI | NULL              | auto_increment    |
-- | username   | varchar(255) | NO   |     | NULL              |                   |
-- | password   | varchar(255) | NO   |     | NULL              |                   |
-- | email      | varchar(255) | NO   | UNI | NULL              |                   |
-- | created_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- +------------+--------------+------+-----+-------------------+-------------------+

INSERT INTO `user_info` (id, username, password, email) VALUES 
(1,'test1','test1','abcd@gmail.com'),
(2,'test2','test2','efgh@gmail.com'),
(3,'test3','test3','ijkl@gmail.com');


-- search
SELECT * FROM user_info WHERE email = 'abcd@gmail.com' AND password = 'test1';
-- search, but just check if exist
SELECT EXISTS (
    SELECT 1 
    FROM user_info 
    WHERE email = 'AAA' AND password = 'BBB'
) AS record_exists;

-- 高效的search api_user
-- 我的版本
SELECT email FROM user_info WHERE email = %s;
-- 更有效率版本
SELECT COUNT(*) FROM user_info WHERE email = %s;
SELECT EXISTS(SELECT 1 FROM user_info WHERE email = %s);


-- -----------------------------------------------------------------------------
-- CREATE TABLE user_booking_tentative ();
CREATE TABLE user_booking_tentative (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
    creator_id INT UNIQUE COMMENT 'User ID who added the attraction',  -- UNIQUE ，唯一的一筆，允許覆蓋
    attraction_id INT COMMENT 'Attraction ID',
    name VARCHAR(255) NOT NULL COMMENT 'Attraction name',
    address VARCHAR(255) NOT NULL COMMENT 'Attraction address',
    image VARCHAR(255) NOT NULL COMMENT 'Attraction image URL',
    date DATE NOT NULL COMMENT 'Attraction date',
    time VARCHAR(50) NOT NULL COMMENT 'Attraction time period',
    price DECIMAL(10) NOT NULL COMMENT 'Attraction price',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',

    FOREIGN KEY (creator_id) REFERENCES user_info(id) ON DELETE CASCADE
);



-- -----------------------------------------------------------------------------
-- CREATE TABLE user_booking_finalized ();
CREATE TABLE user_booking_finalized (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
    order_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Unique order id',
    creator_id INT COMMENT 'User ID who added the attraction', 
    given_status VARCHAR(255) NOT NULL COMMENT 'PAID or UNPAID',
    bank_status INT NOT NULL COMMENT 'Return status code from bank',
    bank_msg VARCHAR(255) NOT NULL COMMENT 'Return msg from bank',


    price DECIMAL(10) NOT NULL COMMENT 'Attraction price',
    attr_id INT NOT NULL COMMENT 'Attraction ID',
    attr_name VARCHAR(255) NOT NULL COMMENT 'Attraction name',
    attr_address VARCHAR(255) NOT NULL COMMENT 'Attraction address',
    attr_image VARCHAR(255) NOT NULL COMMENT 'Attraction image URL',
    attr_date DATE NOT NULL COMMENT 'Attraction date',
    attr_time VARCHAR(50) NOT NULL COMMENT 'Attraction time period',

    contact_name VARCHAR(255) NOT NULL COMMENT 'Contact name',
    contact_email VARCHAR(255) NOT NULL COMMENT 'Contact email',
    contact_phone VARCHAR(255) NOT NULL COMMENT 'Contact tel',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',

    card_secret JSON,
    card_info JSON,

    FOREIGN KEY (creator_id) REFERENCES user_info(id)
);



-- -----------------------------------------------------------------------------
CREATE INDEX order_number_search ON user_booking_finalized(order_number);



ALTER TABLE user_info MODIFY password VARCHAR(255) COMMENT 'User password';

ALTER TABLE user_info
ADD COLUMN auth_provider VARCHAR(50) COMMENT 'Authentication provider',
ADD COLUMN provider_id VARCHAR(255) COMMENT 'Provider user ID',
ADD COLUMN profile_picture TEXT COMMENT 'Profile picture URL';