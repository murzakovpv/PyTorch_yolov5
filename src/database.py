import psycopg2
from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(env_path)

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS people_counts (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    camera_id INTEGER NOT NULL,
                    scene_id INTEGER NOT NULL,
                    count INTEGER NOT NULL
                )
            """)
            self.conn.commit()

    def insert_record(self, record):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO people_counts (camera_id, scene_id, count) VALUES (%s, %s, %s)",
                (record.camera_id, record.scene_id, record.count)
            )
            self.conn.commit()
            