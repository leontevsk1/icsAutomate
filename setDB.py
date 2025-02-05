import mysql.connector
from mysql.connector import Error
from dbconfig import db_name, pword, user, host

db_name = db_name
user = user
pword = pword
host = host
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
     cursor = connection.cursor()
     try:
         cursor.execute(query)
         connection.commit()
         print("Query executed successfully")
     except Error as e:
         print(f"The error '{e}' occurred")
         
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

conn = create_connection(host, user, pword, db_name)
query = "SELECT date FROM date"
last_date = execute_read_query(conn, query )
if last_date:
    print("Полученные данные:", last_date[0][0])
