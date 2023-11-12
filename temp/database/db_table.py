import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS employee_payment;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS benefit;
DROP TABLE IF EXISTS benefit_type;
DROP TABLE IF EXISTS period;
DROP TABLE IF EXISTS time_log;
DROP TABLE IF EXISTS payment_status;


-- Payment status
CREATE TABLE payment_status(
    status_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    PRIMARY KEY (status_id)
);

INSERT INTO 
    payment_status (title)
VALUES 
    ('Pending'),
    ('Complete'),
    ('Overdue'),
    ('Refunded'),
    ('Failed'),
    ('Abandoned'),
    ('Revoked'),
    ('Cancelled'),
    ('Other')
;
COMMIT;


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


-- Employee payment
CREATE TABLE employee_payment(
    payment_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    salary_id INT NOT NULL,
    gross_value DECIMAL(10,2) DEFAULT 0,
    tax_deduction DECIMAL(10,2) DEFAULT 0,
    net_value DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    payment_date DATE NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (payment_id),
    FOREIGN KEY (salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    employee_payment (employee_id, salary_id, gross_value, tax_deduction, net_value, currency_id, payment_date)
VALUES 
    (1, 1, 600, 100, 500, 1, '2023-10-29 9:00:00'),
    (2, 2, 1200, 200, 1000, 1, '2023-10-29 9:00:00'),
    (3, 3, 2400, 400, 2000, 1, '2023-10-29 9:00:00'),
    (4, 4, 4800, 800, 4000, 1, '2023-10-29 9:00:00'),
    (5, 5, 9600, 1600, 8000, 1, '2023-10-29 9:00:00')
;
COMMIT;


-- Employee time log
CREATE TABLE time_log(
    log_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    time_log (employee_id, start_time, end_time)
VALUES 
    (1, '2023-10-01 9:00:00', '2023-10-01 17:00:00'),
    (2, '2023-10-01 9:05:00', '2023-10-01 17:05:00'),
    (3, '2023-10-01 8:55:00', '2023-10-01 17:55:00'),
    (4, '2023-10-01 9:50:00', '2023-10-01 16:55:00')
;
COMMIT;


-- Employee time adjustment
DROP TABLE IF EXISTS time_adjustment;
    CREATE TABLE time_adjustment (
    adjustment_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT,
    time_period DATE,
    time_balance DECIMAL(5,2),
    time_logged DECIMAL(5,2),
    time_correction DECIMAL(5,2),
    last_update DATETIME NOT NULL,
    PRIMARY KEY (adjustment_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO time_adjustment (employee_id, time_period, time_balance, time_logged, time_correction, last_update)
VALUES (1, 2023-01-01', '40.00', '39.00', '-1.00', '2023-01-25 09:00:00')
	(2, 2023-01-01', '40.00', '42.00', '2.00', '2023-01-25 09:00:00')
;



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
