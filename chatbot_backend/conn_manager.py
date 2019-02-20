import pymysql

# Server database connection
# HOST = 'fyp.cshcsxar5far.ap-southeast-1.rds.amazonaws.com'
# DBNAME = 'chatbot'
# USER = 'zhzhang'
# PASSWORD = 'sqcgcwddhyhh'
# PORT = '5432'

# Local database connection
HOST = 'localhost'
DBNAME = 'chatbot'
USER = 'root'
PASSWORD = 'Ljn@920506'
PORT = 3306

def get_conn():
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DBNAME)
    except:
        print("Connection error occurred!")
    
    return conn