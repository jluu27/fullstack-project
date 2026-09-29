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


users = cursor.fetchall()

print(users)
connection.commit()

connection.close()


from flask import Flask, render_template, request, redirect, session
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
        return redirect("/main")
    else:
        return "incorrect user or pass"

@app.route("/main")
def main():
    if "username" not in session:
        return redirect("/")
    
    return render_template("main.html")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/register", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/rem")
def character_view():
    return render_template("rem.html")
@app.route("/vindicta")
def character_view2():
    return render_template("vindicta.html")
#MAKE THIS A CLASS LATER ON 

app.run(debug=True)
    