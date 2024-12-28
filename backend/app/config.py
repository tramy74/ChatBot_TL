import os
import openai
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Connect to PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
