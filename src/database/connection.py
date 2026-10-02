import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

# Resolve .env relative to project root regardless of where the script is called from
project_root = Path(__file__).resolve().parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)


def create_connection():
    """Return an open psycopg3 connection using credentials from .env."""
    conn = psycopg.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    return conn


if __name__ == "__main__":
    conn = create_connection()
    print("Connection successful!")
    conn.close()
