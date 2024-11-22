import ptrs.app

'''
This module creates a Flask instance, 
effectively launching the app.

If you run this module directly (e.g. python app.py),
the default Flask WSGI server will be used.
This WSGI server is incredibly basic and meant for
development only - do not use it in a producting setting.

If you run this module through a proper WSGI server (e.g. gunicorn),
that WSGI server will be used instead of Flask's default one.
'''

if __name__ == '__main__':
    # executed when running module directly
    # this will use the basic (insecure) Flask WSGI server
    app = ptrs.app.create_app()
    app.run()
else:
    # executed when not running module directly
    # e.g. through a proper third-party WSGI server
    app = ptrs.app.create_app()