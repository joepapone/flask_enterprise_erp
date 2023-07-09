import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS employee;

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