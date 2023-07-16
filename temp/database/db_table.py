import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS job_history;
DROP TABLE IF EXISTS job_terms;
DROP TABLE IF EXISTS job_status;
DROP TABLE IF EXISTS employee_email;
DROP TABLE IF EXISTS employee_phone;
DROP TABLE IF EXISTS employee_address;
DROP TABLE IF EXISTS employee;


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
    (1, 'José', 'Ferreira', '1983-10-08', 1, 2),
    (2, 'Elvira', 'Ferreira', '1985-12-27', 2, 2)
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
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id),
    FOREIGN KEY (terms_id) REFERENCES job_terms(terms_id),
    FOREIGN KEY (status_id) REFERENCES job_status(status_id)
);

INSERT INTO 
    job_history (employee_id, department_id, job_id, status_id, terms_id, start_date, end_date)
VALUES 
    (1, 1, 1, 1, 1, '2022-06-04', '2022-12-31'),
    (1, 1, 2, 1, 1, '2021-01-01',  NULL)
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
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    employee_email (employee_id, email, label)
VALUES 
    (1, 'jose.ferreira@gmail.com', 'Work'),
    (2, 'elvira.ferreira@gmail.com', 'Home')
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
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    employee_phone (employee_id, dial_code, phone_number, label)
VALUES 
    (1, '+351', '965 140 555','Mobile'),
    (1, '+351', '965 408 555','Mobile'),
    (2, '+351', '965 399 555','Mobile'),
    (2, '+351', '212 166 555','Home')
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
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO 
    employee_address (employee_id, address1, address2, postal_code, city, state, country_id)
VALUES 
    (1, 'Rua Padre Himalaya', 'No.50','2830-555', 'Barreiro', 'Setúbal', 1),
    (2, 'Rua Alfredo da Silava', 'No.25, 1º Dto.', '3844-555', 'Pinhal Novo', 'Setúbal', 1)
;
COMMIT;

'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)