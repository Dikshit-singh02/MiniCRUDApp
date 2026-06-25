from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------------
# Database
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            note TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Home + Search
# -----------------------------
@app.route("/")
def home():

    search = request.args.get("search", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students,
        search=search
    )


# -----------------------------
# Add Student
# -----------------------------
@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    note = request.form["note"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name,email,note) VALUES(?,?,?)",
        (name, email, note)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# Delete Student
# -----------------------------
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------------
# Edit Student
# -----------------------------
@app.route("/edit/<int:id>")
def edit_student(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        student=student
    )


# -----------------------------
# Update Student
# -----------------------------
@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):

    name = request.form["name"]
    email = request.form["email"]
    note = request.form["note"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?,
            email=?,
            note=?
        WHERE id=?
    """, (name, email, note, id))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(debug=True)