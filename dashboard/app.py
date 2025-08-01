from flask import Flask, render_template, jsonify
import json
from config import RESULTS_FILE

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    with open(RESULTS_FILE) as f:
        results = json.load(f)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
