import db_transaction as db
from db_encrypt import encode, decode
from db_config import ADMIN, ADMIN_EMAIL, ADMIN_PW

# Encrypt admin password.
admin_salt, admin_password = encode(ADMIN_PW)
user_salt, user_password = encode('user')

# Create database SQL transaction.
sql_transact = f'''
-- Create database business_erp 
DROP DATABASE IF EXISTS business_erp;

CREATE DATABASE business_erp;
USE business_erp;

-- Delete tables according to foreign key sequence
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS currency;
DROP TABLE IF EXISTS tax;
DROP TABLE IF EXISTS job_history;
DROP TABLE IF EXISTS job_terms;
DROP TABLE IF EXISTS job_status;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS employee_title;
DROP TABLE IF EXISTS employee_gender;
DROP TABLE IF EXISTS employee_marital;
DROP TABLE IF EXISTS employee_email;
DROP TABLE IF EXISTS employee_phone;
DROP TABLE IF EXISTS employee_address;
DROP TABLE IF EXISTS employee;


-- Role
CREATE TABLE role (
    role_id INT NOT NULL AUTO_INCREMENT,
    role_name VARCHAR(50),
    PRIMARY KEY (role_id)
);

INSERT INTO 
    role (role_name)
VALUES 
    ('Admin'),
    ('Financial managment'),
    ('Accounting'),
    ('Procurement'),
    ('Sales management'),
    ('Sales'),
    ('Production management'),
    ('production'),
    ('Asset management'),
    ('Maintenance'),
    ('Human resouce management'),
    ('Human resorces')
;
COMMIT;


-- User
CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(50),
    role_id INT NOT NULL,
    email VARCHAR(120),
    _salt VARBINARY(255),
    _hash VARBINARY(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (email),
    PRIMARY KEY (user_id),
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE
);


-- Admin user
INSERT INTO 
    user (user_name,role_id,email,_salt,_hash) 
VALUES 
    ('{ADMIN}',{1},'{ADMIN_EMAIL}',X'{admin_salt}',X'{admin_password}'),
    ('Joseph Smith', 11, 'joseph.smith@gmail.com', X'{user_salt}', X'{user_password}'),
    ('Jessica Baker', 12, 'jessica.baker@gmail.com', X'{user_salt}', X'{user_password}')
;
COMMIT;

-- Value Added Tax (VAT)
CREATE TABLE tax(
    tax_id INT NOT NULL AUTO_INCREMENT,
    tax_description VARCHAR(50),
    tax_rate DECIMAL(10,2) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (tax_id)
);

INSERT INTO 
    tax (tax_description, tax_rate)
VALUES 
    ('VAT 0%', 0.00),
    ('VAT 5%', 5.00),
    ('VAT 6%', 6.00),
    ('VAT 19%', 19.00),
    ('VAT 20%', 20.00),
    ('VAT 21%', 21.00),
    ('VAT 23%', 23.00)
;
COMMIT;


-- Currency (according ISO 4217)
CREATE TABLE currency(
    currency_id INT NOT NULL AUTO_INCREMENT,
    currency_name VARCHAR(50),
    currency_code CHAR(3) NOT NULL,
    currency_no INT NOT NULL,
    PRIMARY KEY (currency_id)
);

INSERT INTO 
    currency (currency_name, currency_code, currency_no)
VALUES 
    ('Euro', 'EUR', 978),
    ('Pound Sterling', 'GPB', 826)
;
COMMIT;


-- Country (according ISO 3166-1 and E.164 codes)
CREATE TABLE country(
    country_id INT NOT NULL AUTO_INCREMENT,
    country_name VARCHAR(50),
    country_no INT NOT NULL,
    alpha2_code CHAR(2) NOT NULL,
    dial_code CHAR(4) NOT NULL,
    currency_id INT NOT NULL,
    PRIMARY KEY (country_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id)
);

INSERT INTO 
    country (country_name, country_no, alpha2_code, dial_code, currency_id)
VALUES 
    ('Portugal', 620, 'PT', '+351', 1),
    ('United Kingdom', 826, 'GB', '+44', 2),
    ('Netherlands', 528, 'NL', '+31', 1)
;
COMMIT;


-- Department
CREATE TABLE department (
    department_id INT NOT NULL AUTO_INCREMENT,
    department_name VARCHAR(50),
    PRIMARY KEY (department_id)
);

INSERT INTO 
    department (department_name)
VALUES 
    ('Administration'),
    ('Financial'),
    ('Sales & Marketing'),
    ('Production'),
    ('Maintenance'),
    ('Human Resources')
;
COMMIT;


-- Job
CREATE TABLE job (
    job_id INT NOT NULL AUTO_INCREMENT,
    job_title VARCHAR(50),
    job_description TEXT,
    department_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id) ON DELETE CASCADE
);

INSERT INTO 
    job (department_id, job_title, job_description)
VALUES 
    (1,'Store manager','Manage financials, inventory and staff'),
    (3,'Salesman','Order intake and handling'),
    (3,'Supervisor','Support sales and production, and monitor store upkeeping'),
    (4,'Cook','Prepare sandwiches and soup'),
    (4,'Cook assistant','Cleaning dishes, pots and pans, sweeping and mopping floors'),
    (5,'Maintenance','Check equipment operation and safety')
;
COMMIT;


-- Job Terms
CREATE TABLE job_terms (
    terms_id INT NOT NULL AUTO_INCREMENT,
    terms VARCHAR(50),
    PRIMARY KEY (terms_id)
);

INSERT INTO 
    job_terms (terms)
VALUES 
    ('Full-time'),
    ('Part-time'),
    ('Zero-hour'),
    ('Casual'),
    ('Freelance'),
    ('Executive'),
    ('Fixed-term'),
    ('Non-compete and confientiality')
;
COMMIT;


-- Job Status
CREATE TABLE job_status (
    status_id INT NOT NULL AUTO_INCREMENT,
    status_title VARCHAR(50),
    PRIMARY KEY (status_id)
);

INSERT INTO 
    job_status (status_title)
VALUES 
    ('Active'),
    ('Promoted'),
    ('Changed job'),
    ('Changed department'),
    ('Retired'),
    ('Resigned'),
    ('Dismissed')
;
COMMIT;


-- Employee title
CREATE TABLE employee_title (
    title_id INT NOT NULL AUTO_INCREMENT,
    title_name VARCHAR(10),
    PRIMARY KEY (title_id)
);

INSERT INTO employee_title (title_name)
VALUES ('Mr.'),
	('Mrs.'),
	('Ms.'),
	('Dr.'),
	('Prof.')
;
COMMIT;


-- Employee gender
CREATE TABLE employee_gender (
    gender_id INT NOT NULL AUTO_INCREMENT,
    gender VARCHAR(50),
    PRIMARY KEY (gender_id)
);

INSERT INTO employee_gender (gender)
VALUES ('Male'),
	('Female')
;
COMMIT;


-- Employee marital status
CREATE TABLE employee_marital (
    marital_id INT NOT NULL AUTO_INCREMENT,
    marital_status VARCHAR(50),
    PRIMARY KEY (marital_id)
);

INSERT INTO employee_marital (marital_status)
VALUES ('Single'),
    ('Married'),
    ('Partnership'),
    ('Widowed'),
    ('Divorced'),
    ('Separated')
;
COMMIT;


-- Employee
CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT,
    title_id INT NOT NULL,
    employee_name VARCHAR(50),
    employee_surname VARCHAR(50),
    birthdate DATE NOT NULL,
    gender_id INT NOT NULL,
    marital_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (title_id) REFERENCES employee_title(title_id),
    FOREIGN KEY (gender_id) REFERENCES employee_gender(gender_id),
    FOREIGN KEY (marital_id) REFERENCES employee_marital(marital_id)
);

INSERT INTO 
    employee (title_id, employee_name, employee_surname, birthdate, gender_id, marital_id)
VALUES 
    (1, 'John', 'Doe', '1983-10-08', 1, 2),
    (2, 'Janet', 'Smith', '1985-12-27', 2, 1),
    (2, 'Margaret', 'Thatcher', '1975-12-27', 1, 2),
    (1, 'Jack', 'Daniels', '1965-12-27', 1, 5),
    (1, 'Joe', 'Bagger', '1955-12-27', 2, 4)
;
COMMIT;


-- Employee job history
CREATE TABLE job_history(
    job_history_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    department_id INT NOT NULL,
    job_id INT NOT NULL,
    terms_id INT NOT NULL,
    status_id INT DEFAULT 1 NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (job_history_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id),
    FOREIGN KEY (terms_id) REFERENCES job_terms(terms_id),
    FOREIGN KEY (status_id) REFERENCES job_status(status_id)
)

INSERT INTO 
    job_history (employee_id, department_id, job_id, status_id, terms_id, start_date, end_date)
VALUES 
    (1, 1, 1, 1, 1, '2020-12-10', NULL),
    (2, 3, 2, 1, 1, '2020-05-05', NULL),
    (3, 3, 3, 1, 1, '2023-01-01', NULL),
    (4, 4, 5, 2, 1, '2022-06-04', '2022-12-31'),
    (4, 4, 4, 1, 1, '2023-01-01', NULL),
    (5, 5, 6, 1, 1, '2021-02-14', NULL)
;
COMMIT;


-- Email
CREATE TABLE employee_email(
    email_id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(120),
    label VARCHAR(20),
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (email_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    employee_email (employee_id, email, label)
VALUES 
    (1, 'john.doe@gmail.com', 'Work'),
    (2, 'janet.smith@gmail.com', 'Home'),
    (3, 'roger.smith@gmail.com', 'Mobile'),
    (4, 'jack.daniels@gmail.com', 'Work'),
    (5, 'mary.popens@gmail.com', 'Home')
;
COMMIT;


-- Phone
CREATE TABLE employee_phone(
    phone_id INT NOT NULL AUTO_INCREMENT,
    dial_code CHAR(4) NOT NULL,
    phone_number VARCHAR(50),
    label VARCHAR(20),
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (phone_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    employee_phone (employee_id, dial_code, phone_number, label)
VALUES 
    (1, '+351', '965 140 555','Mobile'),
    (1, '+351', '965 408 555','Mobile'),
    (2, '+351', '965 399 555','Mobile'),
    (3, '+351', '213 234 555','Home'),
    (4, '+351', '965 898 555','Mobile'),
    (2, '+351', '214 888 555','Home'),
    (2, '+351', '223 976 555','Home')
;
COMMIT;


-- Employee address
CREATE TABLE employee_address(
    address_id INT NOT NULL AUTO_INCREMENT,
    address1 VARCHAR(50),
    address2 VARCHAR(50),
    postal_code VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country_id INT NOT NULL,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (address_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    employee_address (employee_id, address1, address2, postal_code, city, state, country_id)
VALUES 
    (1, 'Rua Padre Himalaya', 'No.50','2830-555', 'Barreiro', 'Setúbal', 1),
    (2, 'Rua Castelo Branco', 'No.1, 1º Dto.', '3844-555', 'Pinhal Novo', 'Setúbal', 1),
    (3, 'Av. da Liberdade', 'No.25, 1º Dto.', '3844-555', 'Lisboa', 'Lisboa', 1),
    (4, 'Rua Antero Henriques', 'No.117, 1º Dto.', '3844-555', 'Setúbal', 'Setúbal', 1),
    (5, 'Rua Bordalo Pinheiro', 'No.3','2830-555', 'Barreiro', 'Lisboa', 1)
;
COMMIT;


'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)