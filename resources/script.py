import json
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Config the DB
DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}


def import_data():
    # Load the data from comments json file
    with open('comments.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Drop the table if it already exists
    cur.execute("DROP TABLE IF EXISTS comments;")

    # Create the comments table
    cur.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY,
            parent INTEGER,
            author TEXT,
            text TEXT,
            date TIMESTAMPTZ DEFAULT NOW(),
            likes INTEGER DEFAULT 0,
            image TEXT
        );
        ''')

    sql = """
  INSERT INTO comments (id, parent, author, text, date, likes, image)
  VALUES (%s, %s, %s, %s, %s, %s, %s)
  """

    # Insert every comment
    for comment in data['comments']:
        parent = comment["parent"] if comment["parent"] != "" else None
        cur.execute(
            sql,
            (comment["id"], parent, comment["author"], comment["text"], comment["date"], comment["likes"],
             comment["image"])
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Comment data imported successfully!")


if __name__ == "__main__":
    import_data()
