import os
import logging
import json
import pyodbc
import azure.functions as func

# Database connection string (store this in Azure Function App settings as SQL_CONN_STR)
CONN_STR = (
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

# Helper to get a DB connection
def get_db_connection():
    if not CONN_STR:
        raise ValueError("Missing SQL_CONN_STR environment variable")
    return pyodbc.connect(CONN_STR)

# Azure Function entry point

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing vote request for product")

    try:
        # Parse parameters (from query or JSON body)
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}

        product_id = req.params.get('product_id') or req_body.get('product_id')
        action = req.params.get('action') or req_body.get('action')

        # Validate input
        if product_id is None or action not in ('up', 'down'):
            return func.HttpResponse(
                body=json.dumps({"error": "Please provide 'product_id' and 'action' ('up' or 'down')"}),
                status_code=400,
                mimetype="application/json"
            )

        product_id = int(product_id)
        delta = 1 if action == 'up' else -1

        # Update the score and return new value
        conn = get_db_connection()
        cursor = conn.cursor()

        # Use OUTPUT clause to get the updated score in one round-trip
        sql = (
            "UPDATE products "
            "SET likes = likes + ? "
            "OUTPUT INSERTED.likes "
            "WHERE id = ?"
        )
        cursor.execute(sql, (delta, product_id))
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if not row:
            return func.HttpResponse(
                body=json.dumps({"error": "Product not found"}),
                status_code=404,
                mimetype="application/json"
            )

        new_score = row[0]
        return func.HttpResponse(
            body=json.dumps({"product_id": product_id, "new_score": new_score}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            body=json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )