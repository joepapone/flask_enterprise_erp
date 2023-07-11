import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS employee_address;
DROP TABLE IF EXISTS employee_title;
DROP TABLE IF EXISTS employee_gender;
DROP TABLE IF EXISTS employee_marital;

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
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    employee_address (employee_id, address1, address2, postal_code, city, state, country_id)
VALUES 
    (1, 'Rua Padre Himalaya', 'No.7, R/C Dto.','2830-507', 'Barreiro', 'Setúbal', 1),
    (2, 'Rua Alfredo da Silava', 'No.25, 1º Dto.', '2830-300', 'Pinhal Novo', 'Setúbal', 1)
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
    ('Partnership),
    ('Widowed'),
    ('Divorced'),
    ('Separated')
;
COMMIT;

'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)