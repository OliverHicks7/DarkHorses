import logging
import pyodbc
import os
import json
import random
from azure.functions import HttpRequest, HttpResponse
from dotenv import load_dotenv
load_dotenv()

# Database connection string
CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_DATABASE')};"
    "Authentication=ActiveDirectoryPassword;"
    f"Uid={os.getenv('DB_USERNAME')}@{os.getenv('AZURE_TENANT_NAME')};"
    f"Pwd={os.getenv('DB_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)



def main(req: HttpRequest) -> HttpResponse:
    logging.info("Processing request to get products.")

    # Connect to the database
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT id FROM comments")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    next_id = len(rows) + 1
    alphabet_space = 'abcdefghijklmnopqrstuvwxyz '
    comment_value =  ''.join([random.choice(alphabet_space) for i in range(random.randint(20,100))])
    sentiment = ''.join([random.choice(alphabet_space) for i in range(random.randint(20,100))])


    cursor.execute("INSERT into comments (id, value, sentiment) VALUES (?,?,?)"(next_id, comment_value, sentiment))

    conn.commit()
    # Clean up
    cursor.close()  
    conn.close()