import db_transaction as db
from db_encrypt import encode, decode
from db_config import ADMIN, ADMIN_EMAIL, ADMIN_PW

# Encrypt admin password.
salt, pw_hash = encode(ADMIN_PW)

# Create database SQL transaction.
sql_transact = '''
-- Create database business_erp 
DROP DATABASE IF EXISTS business_erp;

CREATE DATABASE business_erp;
USE business_erp;

-- Role
DROP TABLE IF EXISTS role;

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
DROP TABLE IF EXISTS user   ;

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
    ('{0}',{1},'{2}',X'{3}',X'{4}');
COMMIT;

'''.format(ADMIN,1,ADMIN_EMAIL,salt,pw_hash)

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)