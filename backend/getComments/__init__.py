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

def main(req: HttpRequest) -> HttpResponse:
    logging.info("Processing request to get products.")

    try:
        # Connect to the database
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}

        product_id = req.params.get('product_id') or req_body.get('product_id')

        # Execute query
        sql = "SELECT * FROM comments WHERE product_id = ?"
        cursor.execute(sql, product_id)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        # Transform rows into JSON
        products = [dict(zip(columns, row)) for row in rows]

        # Clean up
        cursor.close()
        conn.close()

        return HttpResponse(json.dumps(products), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return HttpResponse(f"Error: {e}", status_code=500)
    