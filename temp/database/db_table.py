import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS benefit;
DROP TABLE IF EXISTS period;
DROP TABLE IF EXISTS benefit_type;
DROP TABLE IF EXISTS clock_log;
DROP TABLE IF EXISTS clock_event;


-- Period
CREATE TABLE period(
    period_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    PRIMARY KEY (period_id)
);

INSERT INTO 
    period (title)
VALUES 
    ('hour'),
    ('day'),
    ('week'),
    ('month'),
    ('year')
;
COMMIT;


-- Benefit type
CREATE TABLE benefit_type(
    benefit_type_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    PRIMARY KEY (benefit_type_id)
);

INSERT INTO 
    benefit_type (title)
VALUES 
    ('Commission'),
    ('Bonus'),
    ('Performance award'),
    ('Health insurance'),
    ('Life insurance'),
    ('Food and beverage')
;
COMMIT;

    
-- Employee salary
CREATE TABLE salary(
    salary_id INT NOT NULL AUTO_INCREMENT,
    period_id INT NOT NULL,
    gross_value DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (salary_id),
    FOREIGN KEY (period_id) REFERENCES period(period_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    salary (employee_id, period_id, gross_value, currency_id)
VALUES 
    (1, 1, 10.0, 1),
    (2, 2, 80.5, 1),
    (3, 3, 200.10, 1),
    (4, 4, 1500.50, 1),
    (5, 5, 40000.11, 1)
;
COMMIT;


-- Employee benefit
CREATE TABLE benefit(
    benefit_id INT NOT NULL AUTO_INCREMENT,
    benefit_type_id INT NOT NULL,
    period_id INT NOT NULL, 
    series DECIMAL(10,2) DEFAULT 0,
    gross_value DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (benefit_id),
    FOREIGN KEY (benefit_type_id) REFERENCES benefit_type(benefit_type_id),
    FOREIGN KEY (period_id) REFERENCES period(period_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    benefit (employee_id, benefit_type_id, period_id, series, gross_value, currency_id)
VALUES 
    (1, 6, 2, 1, 5.00, 1),
    (1, 2, 1, 1, 0.30, 1),
    (2, 6, 2, 1, 5.00, 1),
    (2, 2, 2, 1, 4.00, 1),
    (3, 6, 2, 1, 5.00, 1),
    (3, 2, 3, 1, 50.00, 1),
    (4, 6, 2, 1, 5.00, 1),
    (4, 2, 3, 1, 100.00, 1),
    (5, 6, 2, 1, 5.00, 1),
    (5, 2, 5, 1, 1000.00, 1),
    (5, 3, 5, 2, 1500.00, 1),
    (5, 4, 4, 1, 150.00, 1)
;
COMMIT;

-- Clock event
CREATE TABLE clock_event(
    event_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    PRIMARY KEY (event_id)
);

INSERT INTO 
    clock_event (title)
VALUES 
    ('Clock-in'),
    ('Clock-out')
;
COMMIT;


-- Clock log
CREATE TABLE clock_log(
    log_id INT NOT NULL AUTO_INCREMENT,
    event_id INT NOT NULL,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    FOREIGN KEY (event_id) REFERENCES clock_event(event_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    clock_log (event_id, employee_id, created, modified)
VALUES 
    (1, 1, '2023-10-01 9:00:00', '2023-10-01 9:00:00'),
    (2, 1, '2023-10-01 17:00:00', '2023-10-01 17:00:00'),
    (1, 2, '2023-10-01 9:05:00', '2023-10-01 9:05:00'),
    (2, 2, '2023-10-01 17:00:00', '2023-10-01 17:00:00'),
    (1, 3, '2023-10-01 8:55:00', '2023-10-01 8:55:00'),
    (2, 3, '2023-10-01 17:05:00', '2023-10-01 17:05:00')
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
