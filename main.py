from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")  # User data sent through jinja

@app.route("/")
def null():
    return render_template("home.html")
    #return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)