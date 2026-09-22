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
    if username == "man27" and password == "password123":
        return redirect("/main")
    else:
        return "incorrect user or pass"

@app.route("/main")
def main():
    return render_template("main.html")

app.run(debug=True)
    