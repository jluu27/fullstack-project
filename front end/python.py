import sqlite3  
connection =  sqlite3.connect("database.db")

connection.close()


from flask import Flask, render_template, request, redirect
app = Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")
def home():
    return render_template('main.html')
@app.route("/login", methods=["POST"])
def check_login():
    username = request.form.get("username")
    password = request.form.get("password")
    username = username.lower() 
    password = password.lower()
    if username == "a" and password == "b":
        return redirect("/main")
    else:
        return "incorrect user or pass"

@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/rem")
def character_view():
    return render_template("rem.html")
@app.route("/vindicta")
def character_view2():
    return render_template("vindicta.html")
#MAKE THIS A CLASS LATER ON 

app.run(debug=True)
    