'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
'''

# Application configurations
HEADER = 'Business ERP'
ABOUT_TEXT = '''
Enterprise ERP is a web based ERP system for best performance and reliability. 
It was designed for ease of use to offer your business all the necessary tools it requires for monitoring and control. 
'''