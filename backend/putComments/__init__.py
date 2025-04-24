import logging
import pyodbc
import os
import json
import random
from azure.functions import HttpRequest, HttpResponse
import azure.functions as func
from dotenv import load_dotenv
load_dotenv()

import os
from openai import AzureOpenAI

endpoint = "https://team1-m9v4q1sc-eastus2.cognitiveservices.azure.com/"
model_name = "o4-mini"
deployment = "o4-mini"

subscription_key = "FovHvpW6FkibdKMrKh12DTA2hq9G3TeUJhmcqRTy6wMaajA61oJFJQQJ99BDACHYHv6XJ3w3AAAAACOGRZum"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

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
    cursor.execute("SELECT comment_id FROM comments")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    next_id = len(rows) + 1

    try:
        req_body = req.get_json()
    except ValueError:
        req_body = {}

    product_id = req.params.get('product_id') or req_body.get('product_id')
    comment_value = req.params.get('comment_value') or req_body.get('comment_value')

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sentiment analysis assistant. "
                    "When given a user’s comment, you must respond with exactly one word: "
                    "‘Positive’ if the sentiment is positive, or ‘Negative’ if the sentiment is negative. "
                    "Do not add any other words or punctuation."
                )
            },
            {
                "role": "user",
                "content": f"Comment: {comment_value}"
            }
        ],
        max_completion_tokens=100000,
        model=deployment
    )

    sentiment = response.choices[0].message.content

    cursor.execute(
        "INSERT INTO comments (product_id, comment_id, [value], sentiment) VALUES (?,?,?,?)",
        (product_id, next_id, comment_value, sentiment)
    )

    conn.commit()
    # Clean up
    cursor.close()  
    conn.close()

    return func.HttpResponse(
        body=json.dumps({"comment_id": next_id}),
        status_code=201,
        mimetype="application/json"
    )