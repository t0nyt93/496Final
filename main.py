from flask import Flask
import time, datetime
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


class CustomerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, Customer Handler!')


def handle_404(request, response, exception):
    response.write(' The URL you requested isn\'t valid in this site!')
    response.set_status(404)


def handle_500(request, response, exception):
    response.write(exception)
    response.set_status(500)


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

app.router.add((r'/books', BookHandler))
app.router.add((r'/customer', CustomerHandler))




def main():
    app.run()

if __name__ == '__main__':
    main()

