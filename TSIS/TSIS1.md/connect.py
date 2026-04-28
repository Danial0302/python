import psycopg2
from config import DB_CONFIG

def get_con():
    return psycopg2.connect(**DB_CONFIG)