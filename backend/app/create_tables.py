from app.database import engine, Base
from app.models import Document, User  # Ensure all models are imported

# Create tables in the database
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
