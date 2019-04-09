import pymysql

# Local database connection
HOST = 'localhost' # host url
DBNAME = 'chatbot' # your database name
USER = 'root'      # your username
PASSWORD = 'password' # your password
PORT = 3306

def get_conn():
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DBNAME)
    except:
        print("Connection error occurred!")
    
    return conn