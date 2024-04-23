import mysql.connector
import pandas as pd

class Database:
    """
    Call to config the and establish a connection for MySQL Database
    """

    def __init__(self) -> None:
        self.host = '127.0.0.1'
        self.port = '3306'
        self.database = 'demo'
        self.user = 'vinay_dev'
        self.password = 'vinay_dev'

        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_result(self, query, dataframe=False, params=()):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if dataframe:
            columns = [i[0] for i in cursor.description]
            res = pd.DataFrame(cursor.fetchall(), columns=columns)
        else:
            res = cursor.fetchall()

        cursor.close()
        return res
    

    def insert_data(self, query, params = ()):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        cursor.close()

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    db_obj = Database()
    param = None
    query = '''
            select * from user_list;
            '''
    result = db_obj.get_result(query=query, dataframe=True, params=())
    print(result)
    db_obj.close_connection()
