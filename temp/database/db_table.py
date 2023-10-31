import db_transaction as db

# Create database SQL transaction.
sql_transact = '''
USE business_erp;

-- Delete tables
DROP TABLE IF EXISTS citizen_data;
DROP TABLE IF EXISTS employee_info;

-- Employee info
CREATE TABLE employee_info(
    info_id INT NOT NULL AUTO_INCREMENT,
    title_id INT NOT NULL,
    given_name VARCHAR(50),
    surname VARCHAR(50),
    passport_no VARCHAR(50),
    id_card_no VARCHAR(50),
    nationality VARCHAR(50),
    place_of_birth_id INT NOT NULL,
    birthdate DATE NOT NULL,
    gender_id INT NOT NULL,
    marital_id INT NOT NULL,
    tin VARCHAR(50),
    ssn VARCHAR(50),
    iban VARCHAR(50),
    employee_id INT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (info_id),
    FOREIGN KEY (title_id) REFERENCES employee_title(title_id),
    FOREIGN KEY (place_of_birth_id) REFERENCES country(country_id),
    FOREIGN KEY (gender_id) REFERENCES employee_gender(gender_id),
    FOREIGN KEY (marital_id) REFERENCES employee_marital(marital_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

INSERT INTO 
    employee_info (employee_id, title_id, given_name, surname, passport_no, id_card_no, nationality, place_of_birth_id, birthdate, gender_id, marital_id, tin, ssn, iban)
VALUES 
    (1, 1, 'John', 'Doe', 'A123456', 'A123456708', 'Portuguese', 1, '1983-10-08', 1, 2, 'A123456789', 'A987654321', 'PT50 0002 0123 1234 5678 9015 4'),
    (2, 2, 'Janet', 'Smith', 'B123456', 'B123456708', 'British', 2, '1985-12-27', 2, 1, 'B123456789', 'B987654321', 'PT50 0002 0123 1234 5678 9015 4'),
    (3, 2, 'Margaret', 'Thatcher', 'C123456', 'C123456708', 'British', 2, '1975-12-27', 1, 2, 'C123456789', 'C987654321', 'PT50 0002 0123 1234 5678 9015 4'),
    (4, 1, 'Jack', 'Daniels', 'D123456', 'D123456708', 'American', 4, '1965-12-27', 1, 5, 'D123456789', 'D987654321', 'PT50 0002 0123 1234 5678 9015 4'),
    (5, 1, 'Joe', 'Bagger', 'E123456', 'E123456708', 'South African', 5, '1955-12-27', 2, 4, 'E123456789', 'E987654321', 'PT50 0002 0123 1234 5678 9015 4')
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
