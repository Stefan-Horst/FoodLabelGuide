from flask import Flask, render_template
import json

with open("resources/label_dict.json", "r", encoding="utf-8") as f:
    label_dict = json.load(f)

app = Flask(__name__)


@app.route("/")
def index():
    detected_labels = ["bio_hexagon", "eco_stars"]
    accordion_data = [label_dict[key] for key in detected_labels]

    return render_template("index.html", data=accordion_data)


if __name__ == "__main__":
    app.run(debug=True)
