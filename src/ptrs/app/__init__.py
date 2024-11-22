from flask import Flask, render_template, request

"""
When you import the ptrs.app package,
all code in this module will be run automatically.
"""

NEWPOTHOLEINFO = {
    "address": "",
    "lattitude": 0,
    "longitude": 0,
    "size": 0,
    "location": "",
    "other": "",
}


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    @app.route("/about")
    def about():
        return "Pothole Tracking and Repair System (PTRS)"

    @app.route("/pothole", methods=["GET", "POST"])
    def pothole():
        if request.method == "POST":
            NEWPOTHOLEINFO["size"] = float(request.form.get("size")) / 10
            NEWPOTHOLEINFO["location"] = request.form.get("location")
            NEWPOTHOLEINFO["other"] = request.form.get("other")
        return render_template("pothole.html")

    @app.route("/addressUpdate", methods=["POST"])
    def process_data():
        NEWPOTHOLEINFO["address"] = request.json["address"]
        NEWPOTHOLEINFO["lattitude"] = request.json["lattitude"]
        NEWPOTHOLEINFO["longitude"] = request.json["longitude"]
        return "success"

    return app
