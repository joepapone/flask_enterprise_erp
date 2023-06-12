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
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS job_history;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS department_history;

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
    job_description VARCHAR(150),
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
'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)