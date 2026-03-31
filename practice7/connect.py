import psycopg2
from config import parametrs
def get_con():
    conn = psycopg2.connect(**parametrs)
    return conn