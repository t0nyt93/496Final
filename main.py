from flask import Flask
import time, datetime
import logging
import webapp2
#app = Flask(__name__)

#app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.respone.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to the Home URL of my CS496 Website. !')

class BookHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, Book Handler!')
    def post(self):
        self.response.write('Hello, Book Handler!')
    def delete(self):
        self.response.write('Hello, Book Handler!')
    def put(self):
        self.response.write('Hello, Book Handler!')
    def patch(self):
        self.response.write('Hello, Book Handler!')

class CustomerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, Customer Handler!')

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write( ' The URL you requested isn\'t valid in this site!' )
    response.set_status(404)


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
], debug=True)

app.router.add( (r'/books',BooksHandler) )
app.router.add( (r'/books',CustomerHandler) )

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
