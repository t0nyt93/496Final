from flask import Flask
import time, datetime
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    var = time.time() 
    t = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d %H:%M:%S')	

    """Return a friendly HTTP greeting."""
    return t 

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
