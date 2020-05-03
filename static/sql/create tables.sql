CREATE DATABASE IF NOT EXISTS Devices;
USE Devices;

CREATE TABLE IF NOT EXISTS Device (
	device_id INT PRIMARY KEY AUTO_INCREMENT,
	device_name VARCHAR(30),
	status VARCHAR(30),
	device_type VARCHAR(30),
	os_type VARCHAR(10),
	os_version VARCHAR(10),
	ram VARCHAR(10),
	device_cpu VARCHAR(50),
	device_bit CHAR(2),
	resolution VARCHAR(30),
	grade VARCHAR(10),
	uuid VARCHAR(50),
	acquisition_date DATE
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS Employee (
	employee_id INT PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	location VARCHAR(30),
    permissions INT
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS DeviceLoan (
	device_id INT,
	employee_id INT,
	loan_date DATE,
	duration VARCHAR(30),
	FOREIGN KEY (device_id) REFERENCES Device(device_id),
	FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
	PRIMARY KEY (device_id, employee_id)
) engine = InnoDB;