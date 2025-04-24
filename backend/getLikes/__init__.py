import logging
import pyodbc
import os
import json
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

def main(req: HttpRequest, product_id) -> HttpResponse:
    logging.info("Processing request to get products.")

    try:
        # Connect to the database
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Execute query
        cursor.execute("SELECT likes FROM products where id = ?", (product_id))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        # Transform rows into JSON
        results = [dict(zip(columns, row)) for row in rows]

        # Clean up
        cursor.close()
        conn.close()

        return HttpResponse(json.dumps(results), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return HttpResponse(f"Error: {e}", status_code=500)
    