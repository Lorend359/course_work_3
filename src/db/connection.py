import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname="hh_vacancies",
        user="postgres",
        password="159753Cdznjckfd!",
        host="localhost",
        port="5432",
        client_encoding="UTF8"
    )


