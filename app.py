import requests
import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__, instance_relative_config=True)

# -----------------------------
# TMDB CONFIG
# -----------------------------

TMDB_API_KEY = "6e7eb60ef8fd5b0fde286cfeb14fb692"
TMDB_URL = "https://api.themoviedb.org/3/movie/popular"

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------

def init_db():
    """
    Initialize the SQLite database.

    - Ensures the instance folder exists
    - Creates movies.db if missing
    - Creates the 'watched' table with (title, year) as the primary key
    """

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, "movies.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS watched (
            title TEXT NOT NULL,
            year INTEGER,
            PRIMARY KEY (title, year)
        )
    """)

    conn.commit()
    conn.close()

# Initialize DB at app startup
init_db()

# -----------------------------
# TMDB MOVIE FETCHER
# -----------------------------

def get_all_movies(pages=3):
    """
    Fetch popular movies from TMDB across multiple pages.

    Args:
        pages (int): number of pages to fetch (20 results per page)

    Returns:
        list of dict: movie dictionaries (title, overview, poster, release_date)
    """

    movies = []

    for page in range(1, pages + 1):

        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "page": page
        }

        response = requests.get(TMDB_URL, params=params)

        if response.status_code != 200:
            print("TMDB error:", response.text)
            continue

        data = response.json()

        for m in data["results"]:
            movies.append({
                "title": m["title"],
                "overview": m["overview"],
                "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m["poster_path"] else None,
                "release_date": m["release_date"],
            })

    return movies
    
# -----------------------------
# DATABASE HELPERS
# -----------------------------

def get_watched_movies():
    """
    Read watched movies from database.

    Returns:
        list of tuple: (title, year)
    """
    db_path = os.path.join(app.instance_path, "movies.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT title, year FROM watched")
    rows = cur.fetchall()

    conn.close()
    return rows


def add_watched_movies(movies):
    """
    Insert multiple movies into the watched table.

    Args:
        movies (list of tuple): each tuple is (title, year)
    """
    db_path = os.path.join(app.instance_path, "movies.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for title, year in movies:
        try:
            cur.execute(
                "INSERT OR IGNORE INTO watched (title, year) VALUES (?, ?)",
                (title, year)
            )
        except Exception as e:
            print("DB Insert Error:", e)

    conn.commit()
    conn.close()


def reset_watched_movies():
    """
    Delete all rows from watched table.
    """
    db_path = os.path.join(app.instance_path, "movies.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM watched")
    conn.commit()
    conn.close()

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# -----------------------------
# RUN THE APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
