import db_transaction as db
from db_encrypt import encode, decode
from db_config import ADMIN, ADMIN_EMAIL, ADMIN_PW

# Encrypt admin password.
salt, pw_hash = encode(ADMIN_PW)

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
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS job_history;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS department_history;
DROP TABLE IF EXISTS phone;
DROP TABLE IF EXISTS email;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS employee_terms;
DROP TABLE IF EXISTS employee_status;
DROP TABLE IF EXISTS employee_history;

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
    ('Production Manager'),
    ('Production Supervisor'),
    ('Sales Manager'),
    ('Salesperson'),
    ('Procurement Manager'),
    ('Procurement'),
    ('Accounting')
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
    FOREIGN KEY (role_id) REFERENCES role(role_id)
);

-- Admin user
INSERT INTO 
    user (user_name,role_id,email,_salt,_hash) 
VALUES 
    ('{ADMIN}',{1},'{ADMIN_EMAIL}',X'{salt}',X'{pw_hash}');
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
    ('Production'),
    ('Sales'),
    ('Maintenance'),
    ('Utility Services'),
    ('Management'),
    ('Human Resources'),
    ('Procurement'),
    ('Accounting'),
    ('Administration')
;
COMMIT;

-- Department history
CREATE TABLE department_history (
    event_id INT NOT NULL AUTO_INCREMENT,
    department_id INT NOT NULL,
    event_description VARCHAR(150),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id)
);
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
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

INSERT INTO 
    job (department_id, job_title, job_description)
VALUES 
    (1,'Cook','Prepare sandwiches and soup'),
    (2,'Salesman','Order Handling'),
    (5,'Supervisor','Support production and sales, and monitor store upkeeping'),
    (5,'Manager','Manage store inventory and financials')
;
COMMIT;

-- Job history
CREATE TABLE job_history (
    event_id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    event_description VARCHAR(150),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id)
);
COMMIT;

-- Employee Terms
CREATE TABLE employee_terms (
    terms_id INT NOT NULL AUTO_INCREMENT,
    terms VARCHAR(50),
    PRIMARY KEY (terms_id)
);

INSERT INTO 
    employee_terms (terms)
VALUES 
    ('Full-time contract'),
    ('Part-time contract'),
    ('Zero-hour contract'),
    ('Casual contract'),
    ('Freelance contract'),
    ('Executive contract'),
    ('Fixed-term contract'),
    ('Non-compete and confientiality contract')
;
COMMIT;

-- Employee Status
CREATE TABLE employee_status (
    status_id INT NOT NULL AUTO_INCREMENT,
    status_title VARCHAR(50),
    PRIMARY KEY (status_id)
);

INSERT INTO 
    employee_status (status_title)
VALUES 
    ('Employed'),
    ('Retired'),
    ('Resigned'),
    ('Dismissed')
;
COMMIT;

-- Employee
CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT,
    employee_name VARCHAR(50),
    employee_surname VARCHAR(50),
    department_id INT NOT NULL,
    job_id INT NOT NULL,
    terms_id INT NOT NULL,
    status_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id),
    FOREIGN KEY (terms_id) REFERENCES employee_terms(terms_id),
    FOREIGN KEY (status_id) REFERENCES employee_status(status_id)
);

INSERT INTO 
    employee (employee_name, employee_surname, department_id, job_id, terms_id, status_id)
VALUES 
    ('José', 'Ferreira', 1, 1, 1, 1),
    ('Elvira', 'Ferreira', 5, 5, 1, 1)
;
COMMIT;

-- Employee history
CREATE TABLE employee_history (
    event_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    event_description VARCHAR(150),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id)
);
COMMIT;

-- Email
CREATE TABLE email(
    email_id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(120),
    label VARCHAR(20),
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (email_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    email (employee_id, email, label)
VALUES 
    (1, 'jose.ferreira@gmail.com', 'Work'),
    (2, 'elvira.ferreira@gmail.com', 'Home')
;
COMMIT;

-- Phone
CREATE TABLE phone(
    phone_id INT NOT NULL AUTO_INCREMENT,
    dial_code CHAR(4) NOT NULL,
    phone_number VARCHAR(50),
    label VARCHAR(20),
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (phone_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    phone (employee_id, dial_code, phone_number, label)
VALUES 
    (1, '+351', '965 140 801','Mobile'),
    (1, '+351', '965 408 908','Mobile')
;
COMMIT;
'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)