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
        "latitude": 40.61784839360533,
        "longitude": -79.14349968544316,
        "address": "310 Locust St, Indiana, PA 15701",
        "size": 5,
        "location": "Turning lane",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "11:39AM on October 26th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "latitude": 40.78190387919964,
        "longitude": -79.05321749721166,
        "address": "9819 Rte 119 Hwy N, Marion Center, PA 0",
        "size": 8,
        "location": "By parking",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "7:23PM on October 26th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "latitude": 40.62053120537463,
        "longitude": -78.91648685182243,
        "address": "6424 PA-403, Homer City, PA 15748",
        "size": 2,
        "location": "",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "12:05AM on October 27th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "latitude": 40.53661477640323,
        "longitude": -79.06485400700325,
        "address": "5533 Rte 422 Hwy W, Indiana, PA 15701",
        "size": 7,
        "location": "",
        "other": "",
        "repairStatus": "Not Repaired",
        "reportDate": "5:17PM on October 27th 2024",
        "expectedCompletion": "October 28th 2024",
    },
    {
        "latitude": 40.66118746305543,
        "longitude": -79.0205031224644,
        "address": "1385 Dixon Rd, Clymer, PA 15728",
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
