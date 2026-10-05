import sqlite3  
connection =  sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
""")
#users = cursor.fetchall()

#print(users)
cursor.execute("DROP TABLE IF EXISTS characters")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        character_image TEXT,
        chinese_name_image TEXT,
        english_name_image TEXT
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS builds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        character TEXT,
        build_name TEXT,
        description TEXT
)
""")


connection.commit()

cursor.execute(
    "SELECT * FROM characters WHERE name = ?",
    ("Vindicta",)
)

existing_character = cursor.fetchone()

if existing_character is None:
    cursor.execute("""
        INSERT INTO characters
        (name, character_image, chinese_name_image, english_name_image)
        VALUES (?, ?, ?, ?)
    """, (
        "Vindicta",
        "images/vindicta/vindictapfp.png",
        "images/vindicta/vindictacn.png",
        "images/vindicta/vindictaeng.png"
    ))
cursor.execute(
    "SELECT * FROM characters WHERE name = ?",
    ("Rem",)
)

existing_character = cursor.fetchone()

if existing_character is None:
    cursor.execute("""
        INSERT INTO characters
        (name, character_image, chinese_name_image, english_name_image)
        VALUES (?, ?, ?, ?)
    """, (
        "Rem",
        "images/rem/rempfp.png",
        "images/rem/remCn.png",
        "images/rem/remeng.png"
    ))
connection.commit()
connection.close()


from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = "endminaha"
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    connection.close()

    if user:
        session["username"] = username
        flash("Hello " + username + "!", "success")
        return redirect("/main")
    else:
        flash("Incorrect username or password", "error")
        return redirect("/")

@app.route("/main")
def main():
    if "username" not in session:
        return redirect("/")
    
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM characters")
    characters = cursor.fetchall()

    connection.close()  

    return render_template("main.html", characters=characters)

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/register", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute (
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    existing_user = cursor.fetchone()

    if existing_user:
        connection.close()
        flash("Username already exists", "error")
        return redirect("/register")
    
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    connection.commit()
    connection.close()
    flash("You have created an account!", "success")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/character/<character_name>")
def character(character_name):
    if "username" not in session:
        return redirect("/")
    
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM characters WHERE name = ?",
        (character_name,)
    )

    character = cursor.fetchone()

    cursor.execute("SELECT * FROM builds WHERE character = ?",
    (character_name,)
    )
    builds = cursor.fetchall()

    print("builds:", builds)
    connection.close()

    return render_template("character.html", character=character, builds=builds)

@app.route("/create_build")
def create_build():
    if "username" not in session:
        return redirect("/")

    return render_template("create_build.html")
@app.route("/create_build", methods=["POST"])
def save_build():
    build_name = request.form["build_name"]
    description = request.form["description"]
    character = request.form["character"]
    username = session["username"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO builds
        (username, character, build_name, description)
        VALUES (?, ?, ?, ?)
    """, (
        username,
        character,
        build_name,
        description
    ))

    connection.commit()
    connection.close()

    return redirect("/main")
@app.route("/edit_build/<int:build_id>")
def edit_build(build_id):
    if "username" not in session:
        return redirect("/")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM builds WHERE id = ?",
        (build_id,)
    )

    build = cursor.fetchone()

    connection.close()

    return render_template("edit_build.html", build=build)
@app.route("/edit_build/<int:build_id>", methods=["POST"])
def save_edit(build_id):
    build_name = request.form["build_name"]
    description = request.form["description"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE builds
        SET build_name = ?, description = ?
        WHERE id = ?
    """, (
        build_name,
        description,
        build_id
    ))

    connection.commit()
    connection.close()

    return redirect("/main")
@app.route("/delete-build/<int:build_id>", methods=["POST"])
def delete_build(build_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM builds WHERE id = ?",
        (build_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/main")
app.run(debug=True)
    