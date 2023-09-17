import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS leave_taken;
DROP TABLE IF EXISTS leave_balance;
DROP TABLE IF EXISTS leave_type;

-- Employee leave type
CREATE TABLE leave_type (
    type_id INT NOT NULL AUTO_INCREMENT,
    type_title VARCHAR(50),
    PRIMARY KEY (type_id)
);

INSERT INTO leave_type (type_title)
VALUES ('Vacation'),
    ('Compensation Leave'),
    ('Maternity Leave'),
    ('Paternity Leave'),
    ('Family Leave'),
    ('Sick Leave')
;
COMMIT;


-- Employee leave balance
CREATE TABLE leave_balance (
    balance_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    type_id INT NOT NULL,
    leave_days DECIMAL(5,2) DEFAULT 0.00,
    leave_taken DECIMAL(5,2) DEFAULT 0.00,
    leave_balance DECIMAL(5,2) DEFAULT 0.00,
    expiry_date DATETIME,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (balance_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES leave_type(type_id)
);

INSERT INTO leave_balance (employee_id, type_id, leave_days, leave_taken, leave_balance, expiry_date)
VALUES (1, 1, 23.00, 3.00, 20.00, '2023-12-31'),
	(1, 4, 14.00, 0.00, 14.00, '2023-12-31')
;
COMMIT;


-- Employee leave taken
CREATE TABLE leave_taken (
    taken_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    balance_id INT NOT NULL,
    start_date DATETIME,
    end_date DATETIME,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (taken_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (balance_id) REFERENCES leave_balance(balance_id) ON DELETE CASCADE
);

INSERT INTO leave_taken (employee_id, balance_id, start_date, end_date)
VALUES (1, 1, '2023-02-01', '2023-02-05'),
(1, 2, '2023-01-15', '2023-04-15')
;
COMMIT;



'''

# Create connection to MySQL server
conn = db.connect_server()

# Check connection before excecuting transaction
if conn is not None:
    # Create MySQL database with default data
    db.create_db(conn, sql_transact)



'''






DROP TABLE IF EXISTS leave_record;

-- Employee leave record
CREATE TABLE leave_record (
    record_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT,
    type_id INT,
    start_date DATETIME,
    end_date DATETIME,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (record_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES leave_type(type_id)
);

INSERT INTO leave_record (employee_id, type_id, start_date, end_date)
VALUES (1, 1, '2023-02-01', '2023-02-05'),
(2, 3, '2023-01-15', '2023-04-15')
;
COMMIT;

'''
'''
    balance_year DATE,
    leave_balance DECIMAL(5,2),
    leave_taken DECIMAL(5,2),
    leave_remaining DECIMAL(5,2),

    INSERT INTO leave_balance (employee_id, balance_year, type_id, leave_balance, leave_taken, leave_remaining)
    VALUES (1, '2023-01-01', 1, '23.00', '3.00', '20.00'),
	(1, '2023-01-01', 4, '14.00', '0.00', '14.00')
'''
