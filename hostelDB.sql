CREATE DATABASE hostel;

USE hostel;

CREATE TABLE student (
    reg_no VARCHAR(4) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    parents_phone_number VARCHAR(15) NOT NULL,
    department VARCHAR(20),
    email VARCHAR(50)
);

INSERT INTO student (reg_no, name, phone_number, parents_phone_number, department, email) VALUES
('3209', 'Nidhi Upadhye', '+919880507681', '+919880507680', 'CSE', 'nidhiu2003@gmail.com'),
('3100', 'Radha Upadhye', '+919632805076', '+919880507680', 'IT','radhau@gmail.com'),
('3108', 'Sree Shamhithaa', '+919900456378', '+916361452314', 'BIOT', 'sreeshami@gmail.com'),
('3914', 'Dharani Guru', '+919456781223', '+919234516724', 'BIN', 'dharanig@gmail.com'),
('3021', 'Sahaana A', '+918925361879', '+919823461278', 'AIDS', 'sahaana0907@gmail.com');

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(4),
    time DATETIME,
    FOREIGN KEY (student_id) REFERENCES student(reg_no)
);