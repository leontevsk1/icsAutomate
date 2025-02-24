import psycopg2
from user_secr import secrets as s


def create_connection(secrets):
    try:
        conn =  psycopg2.connect (
            dbname=secrets['n'],
            user=secrets['u'],
            password=secrets['pw'],
            host=secrets['h'],
            port=secrets['p']
        )
        print('Connected')
    except ConnectionError as e:
        print(f"Error: {e}")
    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    return result

def insert_query(conn,query):
    cursor =conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def close_connection(conn):
    conn.close()
    print('Connection closed')
    
if __name__ == '__main__':
    secr = s()
    f = create_connection(secr)
    print(execute_query(f,'SELECT * FROM date')[0])
    close_connection(f)   