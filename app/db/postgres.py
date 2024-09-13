from psycopg2 import connect
import os

class PostgresDB():
    #Inicialização da classe
    def __init__(self):
        self.conn = self.new_connection()
        self.create_table()

    #Estabelendo conexão com o banco de dados
    def new_connection(self):
        conn = connect(
            host = os.environ["PG_HOST"],
            database = os.environ["PG_DATABASE"],
            port = os.environ["PG_PORT"],
            user = os.environ["PG_USERNAME"],
            password = os.environ["PG_PASSWORD"],
            keepalives = 1,
            keepalives_idle = 30,
            keepalives_interval = 10,
            keepalives_count = 5,
        )
        return conn
    
    #Criação da tabela de dados
    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(open("app/db/schema.sql", "r").read())
        self.conn.commit()

    #Inserção de dados de vôo
    def insert_flight(self, flight):
        insert_sql = f"INSERT INTO {os.environ["PG_SCHEMA"]}.flights (flight_date, flight_iata, flight_status, airline, dep_iata, dep_delay, arr_iata, arr_delay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur = self.conn.cursor()
        cur.execute(insert_sql, flight)
        self.conn.commit()

    #Consulta de todos os vôos registrados no banco
    def select_flights_date(self):
        select_sql = f"SELECT * FROM {os.environ["PG_SCHEMA"]}.flights"
        array_values = []

        cur = self.conn.cursor()
        cur.execute(select_sql, array_values)
        self.conn.commit()
        result = cur.fetchall()
        return result

    #Fechar conexão
    def conn_close(self):
        self.conn.close()