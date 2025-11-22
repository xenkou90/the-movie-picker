import requests
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__, instance_relative_config=True)

# Load TMDB API key (hardcode it for now - to-be-updated)
TMDB_API_KEY = "6e7eb60ef8fd5b0fde286cfeb14fb692"

# Base URL for TMDB API
TMDB_URL = "https://api.themoviedb.org/3/movie/popular"

# Fetches popular movies from TMDB across multiple pages
# Returns a list of simplified movie dictionaries
def get_all_movies(pages=3):

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
