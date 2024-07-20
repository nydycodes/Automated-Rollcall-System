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
('100', 'Neha Sharma', '__________', '__________', 'CSE', 'neha2003@gmail.com'), 
('102', 'Ananya Singh', '__________', '__________', 'IT','ananyas@gmail.com'),
('103', 'Samhitaa Kaur', '__________', '__________', 'BIOT', 'samhitaa.kaur@gmail.com');

-- insert more students as per need

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(4),
    time DATETIME,
    FOREIGN KEY (student_id) REFERENCES student(reg_no)
);
