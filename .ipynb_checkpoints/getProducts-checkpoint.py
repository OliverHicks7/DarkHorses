{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import pyodbc\
from flask import Flask, jsonify\
\
# Flask app initialization\
app = Flask(__name__)\
\
# Load database connection details from environment variables\
DB_SERVER = os.getenv("DB_SERVER", "<your_server>.database.windows.net")\
DB_DATABASE = os.getenv("DB_DATABASE", "<your_database>")\
DB_USERNAME = os.getenv("DB_USERNAME", "<your_username>")\
DB_PASSWORD = os.getenv("DB_PASSWORD", "<your_password>")\
\
CONNECTION_STRING = (\
    'Driver=\{ODBC Driver 17 for SQL Server\};'\
    f'Server=\{DB_SERVER\};'\
    f'Database=\{DB_DATABASE\};'\
    f'Uid=\{DB_USERNAME\};'\
    f'Pwd=\{DB_PASSWORD\};'\
    'Encrypt=yes;'\
    'TrustServerCertificate=no;'\
    'Connection Timeout=30;'\
)\
\
def get_db_connection():\
    """\
    Establishes and returns a new database connection.\
    """\
    return pyodbc.connect(CONNECTION_STRING)\
\
@app.route("/getProducts", methods=["GET"])\
def get_products():\
    """\
    HTTP endpoint handler that retrieves all products from the database\
    and returns them as JSON.\
    """\
    conn = get_db_connection()\
    cursor = conn.cursor()\
\
    # Execute the query\
    cursor.execute("SELECT * FROM products")\
\
    # Fetch column names and rows\
    columns = [column[0] for column in cursor.description]\
    rows = cursor.fetchall()\
\
    # Transform rows into list of dicts\
    products = [dict(zip(columns, row)) for row in rows]\
\
    # Clean up\
    cursor.close()\
    conn.close()\
\
    return jsonify(products)\
\
if __name__ == "__main__":\
    # Run the Flask development server\
    app.run(host="0.0.0.0", port=5000, debug=True)\
}