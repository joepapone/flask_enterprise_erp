import pymysql
from pymysql.constants import CLIENT
from db_config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE_NAME

# Connect to server.
def connect_server() -> object:
    """ 
    Create a connection to MySQL server
    :return: Connection object or None
    """
    try:
        # Connect to MySQL server.
        conn = pymysql.connect(host=DB_HOST,
                               user=DB_USER,
                               password=DB_PASS,                             
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               client_flag=CLIENT.MULTI_STATEMENTS)
        
        print('MySQL Server Connection Successful!')

    except Exception as e:
        print('MySQL Server Connection Failed:\n{}'.format(e))
        conn = None

    return conn

# Connect to database.
def connect_db() -> object:
    """ 
    Create a connection to MySQL database
    :return: Connection object or None
    """
    try:
        # Connect to MySQL server.
        conn = pymysql.connect(host=DB_HOST,
                               user=DB_USER,
                               password=DB_PASS,                             
                               db=DB_DATABASE_NAME,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               client_flag=CLIENT.MULTI_STATEMENTS)
        
        print('MySQL Database Connection Successful!')

    except Exception as e:
        print('MySQL Database Connection Failed:\n{}'.format(e))
        conn = None

    return conn