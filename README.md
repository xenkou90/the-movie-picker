# 🎬 The Movie Picker

**The Movie Picker** is a personal web app built to solve a very real problem:  
having watched *too many movies* and not knowing what to watch next.

Instead of scrolling endlessly, you either:
- let the app **pick a movie for you**, or
- upload your watched movies and get a recommendation you *haven’t seen* yet.

Simple. Fast. No accounts. No noise.

---

## ✨ Features

- 🎲 **Pick for Me** — instantly suggests a movie from a curated TMDB pool  
- 📄 **CSV Upload** — upload your watched movies (Letterboxd-compatible)
- 🚫 **Duplicate-safe** — already-watched titles are excluded
- ⚡ **Fast** — movie details are fetched lazily only when needed
- 🎥 **Direct links** — IMDb & Letterboxd buttons included
- 🎯 **Guessing Game** — a small personal easter egg on the About page

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (custom, no UI framework styling)
- **Database:** SQLite
- **API:** The Movie Database (TMDB)
- **Server:** Gunicorn + systemd
- **Hosting:** Linux VPS (Ubuntu)

---

## 📂 Project Structure

```

themoviepicker/
├── app.py
├── requirements.txt
├── instance/
│   └── movies.db
├── static/
│   ├── style.css
│   ├── main.js
│   └── favicon.png
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── upload.html
│   ├── guess.html
│   └── components/
│       └── guess_block.html
└── venv/

````

---

## 📄 CSV Format

The app expects a CSV with at least:

```csv
Name,Year
Heat,1995
Alien,1979
````

This format works directly with **Letterboxd exports**.

---

## 🚀 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/xenkou90/the-movie-picker.git
cd the-movie-picker
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🔐 Notes

* The SQLite database lives inside `/instance` and is **not committed**
* TMDB API key is required (replace it in `app.py`)
* No user accounts, no tracking, no cookies

---

## 🎞 About the Project

This project was built as:

* a personal tool
* a learning exercise in Flask + deployment
* a love letter to decision fatigue and movie culture

If you’ve ever spent more time choosing a movie than watching one —
this app is for you.

---

## 👤 Author

Built by **Xenofon**
Product photographer & film obsessive
[Letterboxd → ne0n](https://letterboxd.com/ne0n/)

---

## 📜 License

Personal project — feel free to explore, fork, and learn from it.

```

---

If you want next:
- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- or :contentReference[oaicite:2]{index=2}

say the word 🎥
```
