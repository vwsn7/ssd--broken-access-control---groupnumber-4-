
from flask import Flask, request, redirect, session, render_template_string, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "demo-secret-key"
DB = "vulnerable.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            owner_id INTEGER,
            title TEXT,
            content TEXT
        )
    """)

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO users VALUES (1, ?, ?)",
            ("alice@example.com",
             generate_password_hash("AliceDemo123!"))
        )
        conn.execute(
            "INSERT INTO users VALUES (2, ?, ?)",
            ("bob@example.com",
             generate_password_hash("BobDemo123!"))
        )

        conn.execute("""
            INSERT INTO documents VALUES
            (1, 1, 'Alice Private Document',
             'This document belongs to Alice.')
        """)
        conn.execute("""
            INSERT INTO documents VALUES
            (2, 2, 'Bob Private Document',
             'This is Bob private information.')
        """)

    conn.commit()
    conn.close()

LOGIN_PAGE = """
<h2>Vulnerable Document System</h2>
<form method="POST">
    <input name="email" placeholder="Email" required><br><br>
    <input name="password" type="password"
           placeholder="Password" required><br><br>
    <button>Login</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (request.form["email"],)
        ).fetchone()
        conn.close()

        if user and check_password_hash(
            user["password"], request.form["password"]
        ):
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            return redirect("/dashboard")

        return "Invalid login", 401

    return render_template_string(LOGIN_PAGE)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()
    documents = conn.execute(
        "SELECT * FROM documents WHERE owner_id = ?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    html = "<h2>Welcome " + session["email"] + "</h2>"
    html += "<h3>Your Documents</h3>"

    for doc in documents:
        html += (
            f'<p><a href="/documents/{doc["id"]}">'
            f'{doc["title"]}</a></p>'
        )

    html += '<a href="/logout">Logout</a>'
    return html

@app.route("/documents/<int:document_id>")
def view_document(document_id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    # VULNERABILITY:
    # The query checks document ID only.
    # It does NOT check document ownership.
    document = conn.execute(
        "SELECT * FROM documents WHERE id = ?",
        (document_id,)
    ).fetchone()

    conn.close()

    if document is None:
        abort(404)

    return f"""
        <h2>{document['title']}</h2>
        <p>{document['content']}</p>
        <a href="/dashboard">Back</a>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    initialize_db()
    app.run(host="127.0.0.1", port=5001, debug=False)