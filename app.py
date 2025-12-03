import requests
import os
import sqlite3
import csv
import io
from flask import Flask, render_template, request, redirect

# ------------------------------------------------------------
# FLASK APP INITIALIZATION
# ------------------------------------------------------------
# `instance_relative_config=True` allows Flask to use the /instance
# folder for files that shouldn’t be committed (like the SQLite DB).
app = Flask(__name__, instance_relative_config=True)


# ------------------------------------------------------------
# TMDB API CONFIGURATION
# ------------------------------------------------------------
TMDB_API_KEY = "6e7eb60ef8fd5b0fde286cfeb14fb692"
TMDB_URL = "https://api.themoviedb.org/3/movie/popular"


# ------------------------------------------------------------
# DATABASE SETUP
# ------------------------------------------------------------
def init_db():
    """
    Initialize the SQLite database.

    Responsibilities:
    - Make sure the instance/ directory exists.
    - Create the movies.db file if it does not exist.
    - Create a table `watched` with (title, year) as a composite key.

    This runs ONCE at app startup.
    """

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Path to the SQLite DB inside /instance
    db_path = os.path.join(app.instance_path, "movies.db")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create a simple table storing watched movies
    cur.execute("""
        CREATE TABLE IF NOT EXISTS watched (
            title TEXT NOT NULL,
            year INTEGER,
            PRIMARY KEY (title, year)
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB when app starts
init_db()


# ------------------------------------------------------------
# MOVIE CACHE (prevents slow re-fetching)
# ------------------------------------------------------------
cached_movies = []
cached_timestamp = None


# ------------------------------------------------------------
# TMDB API HELPER — Fetch Movies
# ------------------------------------------------------------
# Fetch a large and diverse pool of movies using TMDB Discover.
# This increases variety compared to the standard 'popular' endpoint.
# We fetch: 1. Most popular movies 2. Highest rated movies 3. Movies with high vote counts 4. Movies from random years 
import time

def get_all_movies():

    global cached_movies, cached_timestamp

    # If cache exists and is not older than 6 hours -> use it
    if cached_movies and cached_timestamp:
        if time.time() - cached_timestamp < 6 * 3600:
            return cached_movies

    # Otherwise fetch fresh movie
    movies = []
    movie_ids = set() # prevents duplicates

    base_url = "https://api.themoviedb.org/3/discover/movie"

    # Different Discover configurations (more variety)
    discover_sets = [
        {"sort_by": "popularity.desc"},
        {"sort_by": "vote_average.desc", "vote_count.gte": 500},
        {"sort_by": "vote_count.desc"},
        {"sort_by": "release_date.desc"},
    ]

    # Add RANDOM YEARS for even more variety
    import random
    random_years = random.sample(range(1980, 2024), 5)  # 5 random years

    for year in random_years:
        discover_sets.append({
            "primary_release_year": year,
            "sort_by": "popularity.desc"
        })

    # Fetch movies from all configurations
    for params in discover_sets:
        # Required API params
        params["api_key"] = TMDB_API_KEY
        params["language"] = "en-US"
        params["page"] = 1  # Only first page needed because we use many variations

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            print("TMDB Discover error:", response.text)
            continue

        results = response.json().get("results", [])

        for m in results:
            movie_id = m["id"]

            # Skip duplicates
            if movie_id in movie_ids:
                continue

            movie_ids.add(movie_id)

            movies.append({
                "title": m["title"],
                "overview": m["overview"],
                "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m["poster_path"] else None,
                "release_date": m["release_date"] if m["release_date"] else "N/A",
            })
    # Save to cache
    cached_movies = movies
    cached_timestamp = time.time()

    return movies


# ------------------------------------------------------------
# DATABASE HELPERS — READ, WRITE, RESET
# ------------------------------------------------------------
def get_watched_movies():
    """
    Returns all watched movies as a list of (title, year) tuples.
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
    Insert a list of (title, year) into the database.

    - Uses INSERT OR IGNORE to avoid duplicate primary keys.
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
    Clears the entire watched list.
    (Used by the Reset CSV button.)
    """

    db_path = os.path.join(app.instance_path, "movies.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM watched")
    conn.commit()
    conn.close()



# ------------------------------------------------------------
# ROUTE — HOME PAGE
# ------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page containing:
    - CSV upload
    - "Pick for me" button
    - Movie-card display
    - Reset state messages

    POST actions:
    - Upload a CSV
    - Pick a random unwatched movie
    """

    upload_message = None
    picked_movie = None

    # Used to show a green success message after reset
    reset_message = request.args.get("reset")

    if request.method == "POST":

        # ----------------------------------------------------
        # 1. CSV UPLOAD HANDLER
        # ----------------------------------------------------
        if "csv_file" in request.files:
            file = request.files.get("csv_file")

            if file and file.filename.endswith(".csv"):

                # Read CSV content
                text = file.read().decode("utf-8")
                csv_reader = csv.DictReader(io.StringIO(text))

                movies_to_add = []

                # Extract title + year per row
                for row in csv_reader:
                    title = row.get("Name")
                    year = row.get("Year")

                    # Convert year to int safely
                    try:
                        year = int(year)
                    except:
                        year = None

                    if title:
                        movies_to_add.append((title, year))

                # Add to DB
                add_watched_movies(movies_to_add)

                upload_message = len(movies_to_add)

                # Clear RESET message if CSV is uploaded
                reset_message = None

            else:
                upload_message = "Please upload a valid CSV file"
                reset_message = None



        # ----------------------------------------------------
        # 2. PICK-FOR-ME BUTTON HANDLER
        # ----------------------------------------------------
        elif request.form.get("action") == "pick":

            all_movies = get_all_movies()
            watched = get_watched_movies()

            # Extract just the titles we have already watched
            watched_titles = {w[0] for w in watched}

            # Filter TMDB movies to get unwatched ones
            unwatched = [m for m in all_movies if m["title"] not in watched_titles]

            # Randomly choose a movie if available
            if unwatched:
                import random
                picked_movie = random.choice(unwatched)
            else:
                picked_movie = None
                upload_message = "You've watched all available movies!"

    # Count how many movies are in the database
    watched_count = len(get_watched_movies())

    # Render the home page
    return render_template(
        "index.html",
        upload_message=upload_message,
        watched_count=watched_count,
        picked_movie=picked_movie,
        reset_message=reset_message
    )



# ------------------------------------------------------------
# ROUTE — RESET WATCHED MOVIES
# ------------------------------------------------------------
@app.route("/reset", methods=["POST"])
def reset():
    """
    Clears the database, then redirects back to the homepage
    with a success message.
    """
    reset_watched_movies()
    return redirect("/?reset=1")



# ------------------------------------------------------------
# ROUTE — ABOUT PAGE
# ------------------------------------------------------------
@app.route("/about")
def about():
    """
    Static About page (HTML + JS guessing game)
    """
    return render_template("about.html")


# ------------------------------------------------------------
# ROUTE — GUESSING GAME
# ------------------------------------------------------------
@app.route("/guess")
def guess_page():
    return render_template("guess.html")


# ------------------------------------------------------------
# ROUTE — UPLOAD
# ------------------------------------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        return index()  # reuse your existing CSV processing logic
    return render_template("upload.html")


# ------------------------------------------------------------
# RUN THE APP
# ------------------------------------------------------------
if __name__ == "__main__":
    # Debug mode enabled for development
    app.run(debug=True)
