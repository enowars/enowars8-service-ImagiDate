CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(255) NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    is_public BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- https://github.com/enowars/bambi-service-testify/blob/main/service/mysql/sql-scripts/CreateTable.sql
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'date'@'%';
GRANT SELECT, INSERT ON date.* TO 'date'@'%';
FLUSH PRIVILEGES;

CREATE EVENT IF NOT EXISTS delete_old_users
ON SCHEDULE EVERY 10 MINUTE
DO
  DELETE FROM users WHERE creation_time < NOW() - INTERVAL 10 MINUTE;