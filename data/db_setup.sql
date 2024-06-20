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
