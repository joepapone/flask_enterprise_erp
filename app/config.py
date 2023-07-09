'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
'''

# Application configurations
DEBUG = True
SECRET_KEY = '1650414995b5442d8bb75ec46a355879' # Generate via terminal: $ python3 -c "import uuid; print(uuid.uuid4().hex)"
DATABASE_URI = 'mysql+pymysql://admin:admin@localhost/business_erp' # username:password@host:port/database
WTF_CSRF = '86ece5f425614cbdbc3d3c8079de4154'
HEADER = 'Enterprise ERP'
ABOUT_TEXT = '''
Enterprise ERP is a web based ERP system for best performance and reliability. 
It was designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
'''