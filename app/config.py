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
Business ERP is a web based smart ERP system.
'''