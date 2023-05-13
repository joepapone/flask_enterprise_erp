import mysql.connector as mysql
from mysql.connector import Error
from db_config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE_NAME

# Connect to server.
def connect_db() -> object:
    """ 
    Create a connection to MySQL server
    :return: Connection object or None
    """
    conn = None
    try:
        # Connect to MySQL server.
        conn = mysql.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS)
        return conn
    except Error as e:
        print('Failed to connect to database! {}\n'.format(e))

    return conn


# Create database tables.
def create_db(conn: object, sql_statement: str):
    """ 
    Create an instance for submitting SQL transactions
    :param conn: Connection object
    :param sql_statement: Creates SQL database tables
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_statement) # Execute multiple transactions.

        print('Database tables created successfully!')

    except Error as e:
        print('Failed to execute transaction! {}\n'.format(e))


# Modify database tables.
def modify_db(conn: object, sql_statement: str) -> bool:
    """ 
    Create an instance for submitting INSERT, UPDATE and DELETE SQL transactions
    :param conn: Connection object
    :param sql_statement: Modify database table
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_statement) # Execute transaction for modifying table.
        conn.commit() # Commit (save) changes to database table.
        
        print('The following transaction was successfully executed:\n{}'.format(sql_statement))
        return True

    except Error as e:
        print('Failed to execute transaction! {}\n'.format(e))
        return False


# Query database tables.
def query_db(conn: object, sql_statement: str, param: str) -> tuple:
    """ 
    Create an instance for submitting SELECT SQL transaction
    :param conn: Connection object
    :param sql_statement: Query database table
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_statement, param) # Execute transaction for modifying table.
        
        print('The following transaction was successfully executed:\n{}'.format(sql_statement))
        return cursor.fetchall() # Fetch all records from cursor object

    except Error as e:
        print('Failed to execute transaction! {}\n'.format(e))
        return False