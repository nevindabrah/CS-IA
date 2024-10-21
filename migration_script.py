import sys
import os
from sqlalchemy import text

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import create_app, db

app = create_app()

with app.app_context():
    # Check if the column already exists to avoid duplication
    with db.engine.connect() as connection:
        result = connection.execute(text("PRAGMA table_info(image);"))
        columns = [row[1] for row in result]  # Access the second element of the tuple, which is the column name
        if 'title' not in columns:
            # Add the new column to the Image table
            connection.execute(text('ALTER TABLE image ADD COLUMN title VARCHAR(150)'))
            print("Column 'title' added to 'image' table.")
        else:
            print("Column 'title' already exists in 'image' table.")