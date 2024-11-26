# ptrs
Pothole Tracking and Repair System (PTRS) project for COSC319 at IUP.

## Setup and Run
1. Start by installing the [pixi package manager](https://pixi.sh/latest/) on your machine.
2. Clone and change into the repository to your machine.
3. Run `pixi install` to install necessary dependencies.
4. Create a .env file in the `app` package to store environment variables. You can create an in-memory SQLite database by adding `DATABASE=':memory:'` and ` DATABASE_SCHEMA='database/schema.sql'` to your .env file.
5. Activate the pixi virtual environment. You can do this by either setting your Python interpreter path to `.pixi/envs/default/bin/python` or activating the pixi shell via `pixi shell`.
6. Change to the `src/ptrs/app` directory, then launch `app.py`. If you don't have a proper WSGI server, you can use the default Flask one by simply running `python app.py`. For a production WSGI server (e.g. gunicorn), you'll need to point it to the `app.py` module. `PTRS` leverages `Flask`, so see the [related documentation](https://flask.palletsprojects.com/en/stable/deploying/) for launching the app with other WSGI servers.

## About
A basic implementation of the MVC design pattern in the context of a Flask app for tracking potholes.

This is intended to serve as a basic example. As such, the API and UI are very limited and crude. The REST API exposes 2 endpoints: One for tracking a new pothole, and one for getting info about a previously tracked pothole. From the base components and work flows defined in this example, a more complete app can be designed and created.
