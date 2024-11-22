# ptrs
Pothole Tracking and Repair System (PTRS) project for COSC319 at IUP.

## Setup and Run
1. Start by installing the [pixi package manager](https://pixi.sh/latest/) on your machine.
2. Clone and change into the repository to your machine.
3. Run `pixi install` to install necessary dependencies.
4. Activate the pixi virtual environment. You can do this by either setting your Python interpreter path to `.pixi/envs/default/bin/python` or activating the pixi shell via `pixi shell`.
5. Change to the `src/ptrs/app` directory, then launch `app.py`. If you don't have a proper WSGI server, you can use the default Flask one by simply running `python app.py`. For a production WSGI server (e.g. gunicorn), you'll need to point it to the `app.py` module. `PTRS` leverages `Flask`, so see the [related documentation](https://flask.palletsprojects.com/en/stable/deploying/) for launching the app with other WSGI servers.
