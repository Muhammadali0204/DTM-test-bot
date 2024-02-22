import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False, fetchmany : int = 0):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        if fetchmany != 0:
            data = cursor.fetchmany(fetchmany)
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (

            );
        """
        self.execute(sql, commit=True)
        
    