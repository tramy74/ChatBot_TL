import psycopg2

# Database connection details
DATABASE_URL = "postgresql://postgres:TRAmy_1960%@localhost/chatbot"  # Update with actual credentials

def get_db():
    return psycopg2.connect(DATABASE_URL)
