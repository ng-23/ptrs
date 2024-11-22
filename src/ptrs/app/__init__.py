from flask import Flask

'''
When you import the ptrs.app package,
all code in this module will be run automatically.
'''

def create_app():
    app = Flask(__name__)

    @app.route('/about')
    def about():
        return 'Pothole Tracking and Repair System (PTRS)'
    
    return app