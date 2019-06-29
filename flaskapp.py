from flask import Flask
from flask import Response
flask_app = Flask('flaskapp')


@flask_app.route('/hello')
def hello_world():
    return Response(
        '''<center><h1>Hello world from Flask!\n</h1>
        <h3>Running on a Python WSGI Server.</h3>
        <h4>A platform Independent Server</h4></center>'''
    )

app = flask_app.wsgi_app
