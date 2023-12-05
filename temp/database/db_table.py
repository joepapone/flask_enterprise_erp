import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS income_tax;
DROP TABLE IF EXISTS payroll;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS allowance;
DROP TABLE IF EXISTS allowance_type;
DROP TABLE IF EXISTS period;
DROP TABLE IF EXISTS attendance_log;
DROP TABLE IF EXISTS payment_status;
DROP TABLE IF EXISTS holiday;


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
    gross_value DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (salary_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    salary (employee_id, gross_value, currency_id)
VALUES 
    (1, 600, 1),
    (2, 1200, 1),
    (3, 2400, 1),
    (4, 4800, 1),
    (5, 9600, 1)
;
COMMIT;

    
-- Allowance type
CREATE TABLE allowance_type(
    allowance_type_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    PRIMARY KEY (allowance_type_id)
);

INSERT INTO 
    allowance_type (title)
VALUES 
    ('Commission'),
    ('Bonus'),
    ('Performance award'),
    ('Health insurance'),
    ('Life insurance'),
    ('Food and beverage')
;
COMMIT;


-- Employee allowance
CREATE TABLE allowance(
    allowance_id INT NOT NULL AUTO_INCREMENT,
    allowance_type_id INT NOT NULL,
    period_id INT NOT NULL, 
    gross_value DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (allowance_id),
    FOREIGN KEY (allowance_type_id) REFERENCES allowance_type(allowance_type_id),
    FOREIGN KEY (period_id) REFERENCES period(period_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    allowance (employee_id, allowance_type_id, period_id, gross_value, currency_id, start_date, end_date)
VALUES 
    (1, 6, 2, 5.00, 1, '2023-01-01', '2023-12-31'),
    (1, 2, 1, 0.30, 1, '2023-01-01', '2023-12-31'),
    (2, 6, 2, 5.00, 1, '2023-01-01', '2023-12-31'),
    (2, 2, 2, 4.00, 1, '2023-01-01', '2023-12-31'),
    (3, 6, 2, 5.00, 1, '2023-01-01', '2023-12-31'),
    (3, 2, 3, 50.00, 1, '2023-01-01', '2023-12-31'),
    (4, 6, 2, 5.00, 1, '2023-01-01', '2023-12-31'),
    (4, 2, 3, 100.00, 1, '2023-01-01', '2023-12-31'),
    (5, 6, 2, 5.00, 1, '2023-01-01', '2023-12-31'),
    (5, 2, 5, 1000.00, 1, '2023-01-01', '2023-12-31'),
    (5, 3, 5, 1500.00, 1, '2023-01-01', '2023-12-31'),
    (5, 4, 4, 150.00, 1, '2023-01-01', '2023-12-31'),
    (1, 5, 4, 50.00, 1, '2023-01-01', '2023-12-31')
;
COMMIT;


-- Employee attendance log
CREATE TABLE attendance_log(
    log_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    attendance_log (employee_id, start_time, end_time)
VALUES 
    (1, '2022-10-01 09:00:00', '2022-10-01 17:00:00'),
    (2, '2023-11-01 09:05:00', '2023-11-01 17:05:00'),
    (3, '2023-11-01 08:55:00', '2023-11-01 17:55:00'),
    (4, '2023-11-01 09:00:00', '2023-11-01 16:05:00'),
    (1, '2023-10-02 09:00:00', '2023-10-02 17:10:00'),
    (2, '2023-11-02 09:00:00', '2023-11-02 16:00:00'),
    (1, '2023-10-02 09:00:00', '2023-10-02 17:00:00'),
    (1, '2023-11-01 09:00:00', '2023-11-01 13:00:00'),
    (5, '2023-11-01 09:00:00', '2023-11-01 17:00:00'),
    (1, '2023-11-13 09:00:00', '2023-11-13 10:00:00')
;
COMMIT;

-- Income tax
CREATE TABLE income_tax(
    tax_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    lower_limit DECIMAL(10,2) DEFAULT 0,
    upper_limit DECIMAL(10,2) DEFAULT 0,
    tax_rate DECIMAL(10,2) DEFAULT 0,
    is_married BOOLEAN,
    children TINYINT,
    holders TINYINT,
    has_deficiency BOOLEAN DEFAULT 0,
    wife_has_deficiency BOOLEAN DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (tax_id)
);

INSERT INTO
    income_tax (title, lower_limit, upper_limit, tax_rate, is_married, children, holders)
VALUES 
    ('Single, children=0, holders=1,', 0.00, 750.00, 0.00, 0, 0, 1),
    ('Single, children=0, holders=1,', 751.00, 1000.00, 5.00, 0, 0, 1),
    ('Single, children=0, holders=1,', 1001.00, 1500.00, 20.00, 0, 0, 1),
    ('Married, children=0, holders=1,', 0.00, 750.00, 0.00, 1, 0, 1),
    ('Married, children=0, holders=2,', 0.00, 750.00, 0.00, 1, 0, 2),
    ('Married, children=0, holders=2,', 1001.00, 1500.00, 20.00, 1, 0, 2),
    ('Married, children=1, holders=2,', 1001.00, 1500.00, 15.00, 1, 1, 2),
    ('Married, children=2, holders=2,', 1001.00, 1500.00, 10.00, 1, 2, 2)
;
COMMIT;


-- Payroll
CREATE TABLE payroll(
    payroll_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    gross_income DECIMAL(10,2) DEFAULT 0,
    adjustment DECIMAL(10,2) DEFAULT 0,
    income_tax DECIMAL(10,2) DEFAULT 0,
    net_income DECIMAL(10,2) DEFAULT 0,
    currency_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (payroll_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO
    payroll (employee_id, start_date, end_date, gross_income, adjustment, income_tax, net_income, currency_id)
VALUES 
    (1, '2023-09-01', '2023-09-29', 650, 0, 100, 550, 1),
    (2, '2023-09-01', '2023-09-29', 1200, 0, 200, 1000, 1),
    (4, '2023-09-01', '2023-09-29', 4800, 0, 800, 4000, 1),
    (5, '2023-09-01', '2023-09-29', 9600, 0, 1600, 8000, 1),
    (1, '2023-10-01', '2023-10-29', 600, -50, 50, 550, 1),
    (2, '2023-10-01', '2023-10-29', 1300, 100, 200, 1000, 1),
    (3, '2023-10-01', '2023-10-29', 2400, 0, 400, 2000, 1),
    (4, '2023-10-01', '2023-10-29', 4800, 0, 800, 4000, 1),
    (5, '2023-10-01', '2023-10-29', 9600, 0, 1600, 8000, 1),
    (1, '2023-11-01', '2023-11-29', 650, 0, 100, 550, 1),
    (2, '2023-11-01', '2023-11-29', 1200, 0, 200, 1000, 1),
    (3, '2023-11-01', '2023-11-29', 2400, 0, 400, 2000, 1),
    (4, '2023-11-01', '2023-11-29', 4800, 0, 800, 4000, 1),
    (5, '2023-11-01', '2023-11-29', 9600, 0, 1600, 8000, 1)
;
COMMIT;


-- Holidays
CREATE TABLE holiday(
    holiday_id INT NOT NULL AUTO_INCREMENT,
    holiday VARCHAR(50),
    holiday_date DATE NOT NULL,
    PRIMARY KEY (holiday_id)
);

INSERT INTO
    holiday (holiday, holiday_date)
VALUES 
    ('New Year', '2023-01-01'),
    ('Good Friday', '2023-04-07'),
    ('Easter', '2023-04-09'),
    ('Freedom Day', '2023-04-25'),
    ('Labour Day', '2023-05-01'),
    ('Corpus Christi', '2023-06-08'),
    ('Portugal Day', '2023-06-10'),
    ('Assumption Day', '2023-08-15'),
    ('Republic day', '2023-10-05'),
    ("All Saint's Day", '2023-11-01'),
    ('Restoration of Independence', '2023-12-01'),
    ('Immaculate Conception Day', '2023-12-08'),
    ('Christmas', '2023-12-25')
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


    
-- Employee salary adjustment
CREATE TABLE adjustment(
    adjustment_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50),
    adjustment_amount DECIMAL(10,2) DEFAULT 0,
    adjustment_percentage DECIMAL(10,2) DEFAULT 0,
    is_attendance_adjustment BOOLEAN,
    is_amount_adjustment BOOLEAN,
    is_percentage BOOLEAN,
    PRIMARY KEY (adjustment_id),
);

INSERT INTO 
    adjustment (title, adjustment_percentage, is_attendance_adjustment, is_amount_adjustment)
VALUES 
    ('Overtime', 20.00, 1, 0),
    ('Sick leave', 0.00, 1, 0),
    ('Absent', 0.00, 1, 0),
    ('Social security', 0.00, 1, 0),
    ('Income tax 10%', 0.00, 1, 0),
    ('Absent', 0.00, 1, 0),
    ('Commission', 1.00, 0, 1),
    ('Bonus', 10.00, 0, 1),
    ('Performance award', 10.00, 0, 1),
    ('Food and beverage', 0, 1),
    ('Health insurance', 0, 1),
    ('Life insurance', 0, 1)
;
COMMIT;

    
-- Employee salary adjustment amount
CREATE TABLE salary_adjustment_amount(
    adjustment_amount_id INT NOT NULL AUTO_INCREMENT,
    payment_id INT NOT NULL,
    adjustment_id INT NOT NULL,
    adjustment_amount DECIMAL(10,2) DEFAULT 0,
    adjustment_percentage DECIMAL(10,2) DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (adjustment_amount_id),
    FOREIGN KEY (payment_id) REFERENCES salary_payment(payment_id),
    FOREIGN KEY (adjustment_id) REFERENCES salary_adjustment(adjustment_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    salary_adjustment_amount (payment_id, adjustment_id, adjustment_amount, adjustment_percentage)
VALUES 
    ('Working hours', 1, 0),
    ('Commission', 0, 1),
    ('Bonus', 0, 1),
    ('Performance award', 0, 1),
    ('Food and beverage', 0, 1),
    ('Health insurance', 0, 1),
    ('Life insurance', 0, 1)
;
COMMIT;

-- Employee working time adjustment
CREATE TABLE time_adjustment(
    adjustment_id INT NOT NULL AUTO_INCREMENT,
    time_log_id INT NOT NULL,
    adjustment_id INT NOT NULL,
    adjustment_amount DECIMAL(10,2) DEFAULT 0,
    adjustment_percentage DECIMAL(10,2) DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (adjustment_amount_id),
    FOREIGN KEY (time_log_id) REFERENCES time_log(time_log_id),
    FOREIGN KEY (adjustment_id) REFERENCES salary_adjustment(adjustment_id),
    FOREIGN KEY (payment_id) REFERENCES salary_payment(payment_id) ON DELETE CASCADE
);

INSERT INTO 
    salary_adjustment_amount (payment_id, adjustment_id, adjustment_amount, adjustment_percentage)
VALUES 
    ('Working hours', 1, 0),
    ('Commission', 0, 1),
    ('Bonus', 0, 1),
    ('Performance award', 0, 1),
    ('Food and beverage', 0, 1),
    ('Health insurance', 0, 1),
    ('Life insurance', 0, 1)
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
