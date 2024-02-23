import pymysql

class DB:
    def getConnection():
        try:
            conn = pymysql.connect(
            host="localhost",
            db="mychatapp",
            user="mychatappuser",
            password="mychatappuser",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()
