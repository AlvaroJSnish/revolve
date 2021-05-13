import psycopg2 as pg


class Database:
    database_host = ''
    database_port = ''
    database_user = ''
    database_password = ''
    database_type = ''
    database_name = ''
    connection = None

    def __init__(self, database_host, database_port, database_password, database_type, database_user, database_name):
        self.database_host = database_host
        self.database_port = database_port
        self.database_user = database_user
        self.database_password = database_password
        self.database_type = database_type
        self.database_name = database_name

    def connect(self):
        try:
            if self.database_type == 'postgres':
                self.connection = pg.connect(
                    host=self.database_host,
                    database=self.database_name,
                    user=self.database_user,
                    password=self.database_password,
                    port=self.database_port
                )

                cursor = self.connection.cursor()

                print(cursor)

                cursor.close()
            else:
                pass
        except ValueError:
            pass
