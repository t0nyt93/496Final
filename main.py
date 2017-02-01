from flask import Flask
import time, datetime


import webapp2
import os
from google.appengine.ext import ndb


# RESTful permissions
PERMISSION_ANYONE = 'anyone'
PERMISSION_LOGGED_IN_USER = 'logged_in_user'
PERMISSION_OWNER_USER = 'owner_user'
PERMISSION_ADMIN = 'admin'

"""
Create Database Models
"""


class customerModel(ndb.Model):
    id = ndb.IntegerProperty
    title = ndb.StringProperty
    isbn = ndb.IntegerProperty
    genre = [ ndb.StringProperty() ]
    author = ndb.StringProperty


class bookModel(ndb.Model):
    id = ndb.IntegerProperty
    name = ndb.StringProperty
    balance = ndb.IntegerProperty
    checked_out = [ ndb.StringProperty ]


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, CS496!')

"""
Customer Handler

Provides a REST api for creating, updating, and deleting book objects
"""

class BookHandler(webapp2.RequestHandler):
    def get(self, book_id):
        self.response.write('Book id is %s' % book_id)


"""
Customer Handler

Provides a REST api for creating, updating, and deleting Customer objects
"""

class CustomerHandler(webapp2.RequestHandler):
    def get(self, customer_id):
        self.response.write('Customer id is %s' % customer_id)
        #Potentially use ID as lookup then do an object_key.get()
        #and write out the json structure.


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

app.router.add((r'/books/(\d+)', BookHandler))
app.router.add((r'/customers/(\d+)', CustomerHandler))







def main():
    app.run()

if __name__ == '__main__':
    main()

