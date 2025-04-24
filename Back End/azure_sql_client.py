import pymysql
import pandas

conn = pymssql.connect(
    server='yourserver.database.windows.net',
    user='yourusername@yourserver',
    password='yourpassword',
    database='yourdbname'
)

cursor = conn.cursor()
cursor.execute('SELECT TOP 5 * FROM your_table')
print(cursor.fetchall())