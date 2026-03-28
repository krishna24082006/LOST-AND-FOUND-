# cd "C:\Users\deeps\OneDrive\Desktop\Coading\lostfound_portal"
# python app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "lostfound.db")

app = Flask(__name__, static_folder="static")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            location TEXT,
            contact TEXT,
            status TEXT NOT NULL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/", methods=["GET","POST"])
def index():
    # If user submits search from homepage
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("query","").strip()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""SELECT * FROM items
                     WHERE name LIKE ? OR description LIKE ? OR location LIKE ?
                     ORDER BY id DESC""",
                  (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()
    else:
        # show recent items
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM items ORDER BY id DESC LIMIT 6")
        results = c.fetchall()
        conn.close()

    return render_template("index.html", results=results, query=query)

@app.route("/report", methods=["GET","POST"])
def report():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        description = request.form.get("description","").strip()
        location = request.form.get("location","").strip()
        contact = request.form.get("contact","").strip()
        status = request.form.get("status","Lost").strip()

        created_at = datetime.utcnow().isoformat()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO items (name, description, location, contact, status, created_at)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (name, description, location, contact, status, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("report.html")

@app.route("/items")
def items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    all_items = c.fetchall()
    conn.close()
    return render_template("items.html", items=all_items)

@app.route("/search", methods=["GET","POST"])
def search():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("keyword","").strip()
    else:
        query = request.args.get("q","").strip()

    if query:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""SELECT * FROM items
                     WHERE name LIKE ? OR description LIKE ? OR location LIKE ?
                     ORDER BY id DESC""",
                  (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()
    return render_template("search.html", results=results, query=query)


if __name__ == "__main__":

    init_db()
    app.run(debug=True)
