from db_conn_pymysql import connect_server, connect_db

# Create database tables.
def create_db(conn: object, sql_statement: str):
    """ 
    Create an instance for submitting SQL transactions
    :param conn: Connection object
    :param sql_statement: Creates MySQL database and tables
    :return:
    """
    try:
        with conn.cursor() as cursor: # Prepare a cursor object using cursor() method
            cursor.execute(sql_statement) # Execute SQL transaction to create database using execute() method.

            print('Database created successfully!')

    except Exception as e:
        print('MySQL Transaction Failed:\n{}'.format(e))
    
    finally:
        conn.close()

# Modify data.
def modify_db(conn: object, sql_statement: str) -> bool:
    """ 
    Create an instance for submitting INSERT, UPDATE and DELETE SQL transactions
    :param conn: Connection object
    :param sql_statement: Modify database table
    :return:
    """
    try:
        with conn.cursor() as cursor: # Prepare a cursor object using cursor() method
            cursor.execute(sql_statement) # Execute SQL transaction to modify data.
            connect_db.commit() # Commit (save) changes to database table.
            
            print('The following transaction was successfully executed:\n{}'.format(sql_statement))

    except Exception as e:
        print('MySQL Transaction Failed:\n{}'.format(e))
    
    finally:
        conn.close()

# Query data.
def query_db(conn: object, sql_statement: str, param: str) -> tuple:
    """ 
    Create an instance for submitting SELECT MySQL transaction
    :param conn: Connection object
    :param sql_statement: Query database table
    :return:
    """
    try:
        with conn.cursor() as cursor: # Prepare a cursor object using cursor() method
            cursor.execute(sql_statement, param) # Execute SQL transaction to query data
            
            print('The following transaction was successfully executed:\n{}'.format(sql_statement))
            return cursor.fetchall() # Fetch all records from cursor object

    except Exception as e:
        print('MySQL Transaction Failed:\n{}'.format(e))
    
    finally:
        conn.close()