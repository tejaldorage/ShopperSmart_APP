import os
from database import Base, engine

# Delete existing database file if it exists
if os.path.exists("shopsmart.db"):
    os.remove("shopsmart.db")

# Recreate tables fresh
Base.metadata.create_all(bind=engine)

print("Database reset and tables created.")
