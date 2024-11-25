from flask import Flask, render_template, request

"""
When you import the ptrs.app package,
all code in this module will be run automatically.
"""

NEWPOTHOLEINFO = {
    "longitude": 0,
    "latitude": 0,
    "address": "",
    "size": 0,
    "location": "",
    "other": "",
}

POTHOLES = [
    {
        "longitude": -79.14330656640881,
        "latitude": 40.61788300526618,
        "address": "East Locust Street, Indiana, PA 15701",
        "size": 5,
        "location": "Turning lane",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "11:39AM on October 26th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "longitude": -79.15567480668099,
        "latitude": 40.616057738540064,
        "address": "849 Grant Street, Indiana, PA 15701",
        "size": 8,
        "location": "By parking",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "7:23PM on October 26th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "longitude": -79.16833557394808,
        "latitude": 40.62060286129906,
        "address": "202 South 14th Street, Indiana, PA 15701",
        "size": 2,
        "location": "",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "12:05AM on October 27th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "longitude": -79.16043114570603,
        "latitude": 40.625764114281935,
        "address": "1096 Oak Street, Indiana, PA 15701",
        "size": 7,
        "location": "",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "5:17PM on October 27th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "latitude": 40.61988757212833,
        "longitude": -79.15554698944091,
        "address": "290 Pratt Dr, Indiana, PA 15705",
        "size": 1,
        "location": "",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "8:21PM on October 27th 2024",
        "expectedCompletion": "October 28th 2024",
    },
]


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

    @app.route("/data", methods=["GET", "POST"])
    def process_data():
        if request.method == "POST":
            NEWPOTHOLEINFO["longitude"] = request.json["longitude"]
            NEWPOTHOLEINFO["latitude"] = request.json["latitude"]
            NEWPOTHOLEINFO["address"] = request.json["address"]
            return "success"
        elif request.method == "GET":
            return POTHOLES

    return app
