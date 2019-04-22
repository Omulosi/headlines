import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
	API_KEY = os.getenv('API_KEY')
	APP_ID = os.getenv('APP_ID')
