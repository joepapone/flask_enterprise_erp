import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS job_history;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS department_history;


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