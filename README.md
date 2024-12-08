# ptrs
Pothole Tracking and Repair System (PTRS) project for COSC319 at IUP.

## Setup and Run
1. Start by setting up a Python virtual environment on your machine. Make sure your Python version is 3.12 or higher.
2. Clone and change into the repository directory to your machine.
3. Activate your virtual environment. Run `pip install -e .` to install the required dependencies specified in `pyproject.toml`. This will also make an editable install of the `ptrs` package.
4. Create a .env file in the repository directory to store environment variables. You can create an in-memory SQLite database by adding `DATABASE=':memory:'` and ` DATABASE_SCHEMA='database/schema.sql'` to your .env file.
5. Change to the `src/ptrs/app` directory, then launch `app.py`. If you don't have a proper WSGI server, you can use the default Flask one by simply running `python app.py`. For a production WSGI server (e.g. gunicorn), you'll need to point it to the `app.py` module. `PTRS` leverages `Flask`, so see the [related documentation](https://flask.palletsprojects.com/en/stable/deploying/) for launching the app with other WSGI servers.

## About
A basic implementation of the MVC design pattern in the context of a Flask app for tracking potholes. Features a simple REST API and a clean UI for performing basic CRUD operations on potholes and work orders.
