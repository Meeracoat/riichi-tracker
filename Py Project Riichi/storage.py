import sqlite3
from pathlib import Path


DB = Path("data/tracker.db")


def get_connection():

    DB.parent.mkdir(
        exist_ok=True
    )

    return sqlite3.connect(DB)


def create_database():

    conn = get_connection()

    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE

    )
    """)

    # Matches table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        replay TEXT,

        date TEXT,

        mode TEXT,

        placement INTEGER,

        points INTEGER,

        riichi INTEGER,

        wins INTEGER,

        ron INTEGER,

        tsumo INTEGER,

        deal_ins INTEGER,

        UNIQUE(user_id, replay),

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    conn.commit()
    conn.close()


def get_user(username):

    create_database()

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users(username)
        VALUES (?)
        """,
        (username,)
    )

    conn.commit()

    cur.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user_id = cur.fetchone()[0]

    conn.close()

    return user_id


def save_match(match, username):

    user_id = get_user(username)

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO matches
        (
            user_id,
            replay,
            date,
            mode,
            placement,
            points,
            riichi,
            wins,
            ron,
            tsumo,
            deal_ins
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (
            user_id,
            match["Replay"],
            match["Date"],
            match["Mode"],
            match["Placement"],
            match["Points"],
            match["Riichi"],
            match["Wins"],
            match["Ron"],
            match["Tsumo"],
            match["Deal-ins"]
        )

    )

    conn.commit()

    conn.close()


def load_matches(username):

    user_id = get_user(username)

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            replay,
            date,
            mode,
            placement,
            points,
            riichi,
            wins,
            ron,
            tsumo,
            deal_ins

        FROM matches

        WHERE user_id = ?

        ORDER BY id

        """,

        (user_id,)

    )

    rows = cur.fetchall()

    conn.close()

    return [

        {
            "Replay": r[0],
            "Date": r[1],
            "Mode": r[2],
            "Placement": r[3],
            "Points": r[4],
            "Riichi": r[5],
            "Wins": r[6],
            "Ron": r[7],
            "Tsumo": r[8],
            "Deal-ins": r[9]
        }

        for r in rows

    ]
