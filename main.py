from flask import Flask
import time, datetime

import json
import webapp2
import os
from google.appengine.ext import ndb


# RESTful permissions
PERMISSION_ANYONE = 'anyone'
PERMISSION_LOGGED_IN_USER = 'logged_in_user'
PERMISSION_OWNER_USER = 'owner_user'
PERMISSION_ADMIN = 'admin'

customer_keys = []
book_keys = []
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
        #Ok so let's just parse the book_id and then figure out what to return?
        url = book_id.split("/")

        #/books/authors/:name
        if (url[0] == 'author' ) and (len(url) == 2):
            #Get all of the books where the authors name is url[1]
            self.response.write("Viewing books by author, desired %s" % url[1])
        #/books/genre/:type
        elif (url[0] == 'genre') and (len(url) == 2):
            # Get all of the books where the authors name is url[1]
            self.response.write("Viewing books by genre, desired %s" % url[1])
        #/books/
        elif (url[0] == "") and (len(url) == 1):
            #Get all of the books
            self.response.write("Viewing all books ")
        #/books/:id
        elif (url[0].isdigit() ) and (len(url) == 1):
            #Lookup the books ID and return the json.
            #/books/:id
            self.response.write('Book id is %s' % book_id)
"""
    def put(self, arg):
        #Put to /books/
        if arg == "":

        #PUT to /books/id
        elif arg.isDigit():
            #Get the book with the right ID and change it's values

    def delete(self, arg):
        # Put to /books/
        if arg == "":

        # PUT to /books/id
        elif arg.isDigit():

    # Get the book with the right ID and change it's values
    def post(self):
        #Create a new record with the given body

    def patch(self,arg):
        # Put to /books/
        if arg == "":

        # Update the book with the corresponding ID
        elif arg.isDigit():"""
"""
Customer Handler

Provides a REST api for creating, updating, and deleting Customer objects
"""

class CustomerHandler(webapp2.RequestHandler):
    c = customerModel.query()
    next_id = len(c) + 1

    def get(self, customer_id):
        if customer_id.isDigit():
            desired_customer = customerModel.query(customerModel.id == int(customer_id))
            if desired_customer:
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write( json.dumps(desired_customer.to_dict()))
            else:
                self.response.write("Could not find a customer with the ID %s, have you created one yet?" % customer_id)

        else:
            self.response.write('Customer ID\'s consist of solely digits!')


    def post(self):
        new_customer = customerModel()
        new_customer.id = self.next_id
        new_customer.name = self.request.get('name', "John Doe")
        new_customer.balance = self.request.get('balance', "0")
        new_customer.checked_out = self.request.get_all('checked_out', "")
        cust_key = new_customer.put()
        customer_keys.append(cust_key)


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

app.router.add((r'/books/(.*)', BookHandler))
app.router.add((r'/customers/(.*)', CustomerHandler))







def main():
    app.run()

if __name__ == '__main__':
    main()

