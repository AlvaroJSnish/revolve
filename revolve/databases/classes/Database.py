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

                self.cursor = self.connection.cursor()

                return self.cursor
            else:
                pass
        except:
            # print("Error connecting to database: ", e)
            return None

    def disconnect(self):
        self.cursor.close()

    def get_tables(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        tables = []
        for table in self.cursor.fetchall():
            tables.append(table)

        return tables

    def get_table(self, table_name, with_headers=False):
        query = "select * from {table_name} limit 20".format(table_name=table_name)
        self.cursor.execute(query)

        rows = []

        if with_headers:
            rows.append([desc[0] for desc in self.cursor.description])

        for row in self.cursor.fetchall():
            rows.append(row)

        return rows

    def execute_query(self, query, with_headers=False):
        result = []
        self.cursor.execute(query)

        if with_headers:
            result.append([desc[0] for desc in self.cursor.description])

        for row in self.cursor.fetchall():
            result.append(row)

        return result

    def create_records(self, table_name):
        sql = f'create table revolve_{table_name}_trainings (id serial PRIMARY KEY, date TIMESTAMP not null)'
        sql_clone_table = f'create table revolve_{table_name}_records as (select * from {table_name}) with no data'
        self.cursor.execute(sql)
        self.cursor.execute(sql_clone_table)
        self.connection.commit()

    def insert_records(self, table_name):
        sql = f'select * from {table_name}'
        self.cursor.execute(sql)

        headers = ', '.join([desc[0] for desc in self.cursor.description])

        for row in self.cursor.fetchall():
            self.cursor.execute(
                f'insert into revolve_{table_name}_records values {row}')

        self.connection.commit()

    # def update_trainings(self, table_name):
