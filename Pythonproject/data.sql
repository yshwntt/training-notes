CREATE DATABASE productivity_app;

USE productivity_app;

CREATE TABLE user_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(20),
    study_hours FLOAT,
    total_screen_time FLOAT,
    earned_points INT,
    earned_minutes INT
);

select user_logs