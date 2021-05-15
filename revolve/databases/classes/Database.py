import psycopg2 as pg


class DatabaseConnector:
    database_host = ''
    database_port = ''
    database_user = ''
    database_password = ''
    database_type = ''
    database_name = ''
    connection = None

    cursor = None

    def __init__(self, database_host, database_port, database_password, database_type, database_user, database_name):
        self.database_host = database_host
        self.database_port = database_port
        self.database_user = database_user
        self.database_password = database_password
        self.database_type = database_type
        self.database_name = database_name

    def connect(self):
        try:
            if self.database_type == 'postgresql':
                self.connection = pg.connect(
                    host=self.database_host,
                    database=self.database_name,
                    user=self.database_user,
                    password=self.database_password,
                    port=self.database_port
                )

                cursor = self.connection.cursor()
                self.cursor = cursor

                return cursor
            else:
                pass
        except:
            # print("Error connecting to database: ", e)
            return None

    def disconnect(self):
        self.cursor.close()

    def get_tables(self, cursor):
        self.cursor = cursor
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            print(table)
