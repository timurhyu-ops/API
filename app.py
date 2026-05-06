from flask import Flask, render_template, request, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "vinyl_key_99"

@app.route("/", methods=["GET", "POST"])
def index():
    tracks = []
    advice = ""
    if request.method == "POST":
        query = request.form.get("query")
        try:
            res = requests.get(f"https://itunes.apple.com/search?term={query}&entity=song&limit=6")
            tracks = res.json().get("results", [])
            
            adv_res = requests.get("https://api.adviceslip.com/advice")
            advice = adv_res.json().get("slip", {}).get("advice")
        except:
            return "API Error", 500
            
    return render_template("index.html", tracks=tracks, advice=advice)

@app.route("/add", methods=["POST"])
def add():
    if "lib" not in session: session["lib"] = []
    track = {
        "name": request.form.get("name"),
        "artist": request.form.get("artist"),
        "img": request.form.get("img")
    }
    if track not in session["lib"]:
        session["lib"].append(track)
        session.modified = True
    return redirect(url_for("library"))

@app.route("/library")
def library():
    return render_template("library.html", songs=session.get("lib", []))

@app.route("/clear")
def clear():
    session.pop("lib", None)
    return redirect(url_for("library"))

if __name__ == "__main__":
    app.run(debug=True)