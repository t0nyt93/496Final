from flask import Flask
import time, datetime
import webapp2
#app = Flask(__name__)

#app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
], debug=True)

def main():
    app.run()

if __name__ == '__main__':
    main()
'''
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
'''
