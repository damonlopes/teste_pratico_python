from psycopg2 import connect, DatabaseError
import os

class PostgresDB():
    def __init__(self):
        self.conn = self.new_connection()
        self.create_table()

    def new_connection(self):
        conn = connect(
            host = os.environ["HOST_DB"],
            database = os.environ["DATABASE_DB"],
            port = os.environ["PORT_DB"],
            user = os.environ["USERNAME_DB"],
            password = os.environ["PASSWORD_DB"],
            keepalives = 1,
            keepalives_idle = 30,
            keepalives_interval = 10,
            keepalives_count = 5,
        )
        return conn
    
    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(open("app/db/schema.sql", "r").read())
        self.conn.commit()

    def insert_flight(self, flight):
        insert_sql = f"INSERT INTO {os.environ["SCHEMA_DB"]}.{os.environ["TABLE_DB"]} (flight_date, flight_iata, flight_status, airline, dep_iata, dep_delay, arr_iata, arr_delay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur = self.conn.cursor()
        cur.execute(insert_sql, flight)
        self.conn.commit()

    def conn_close(self):
        self.conn.close()