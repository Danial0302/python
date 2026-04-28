import psycopg2
from config import DB_CONFIG


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            """)


init_db()


def get_or_create_player(username):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO players(username)
                VALUES (%s)
                ON CONFLICT (username) DO NOTHING
            """, (username,))

            cur.execute("SELECT id FROM players WHERE username=%s", (username,))
            return cur.fetchone()[0]


def save_game(player_id, score, level):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (player_id, score, level))