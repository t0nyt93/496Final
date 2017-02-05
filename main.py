import json
import webapp2
import os
import cgi
from google.appengine.ext import ndb
from cStringIO import StringIO

# RESTful permissions
PERMISSION_ANYONE = 'anyone'
PERMISSION_LOGGED_IN_USER = 'logged_in_user'
PERMISSION_OWNER_USER = 'owner_user'
PERMISSION_ADMIN = 'admin'

#So my limited understanding leads me to belive that these keys are solely available
#in the context of the Process Memory. Therefore if we've restarted the server, we
#lost all of the keys that we'd previously created, granted we can the objects with query...
#
#HALLELUJAH
#If you're interested the server could have a startup task that got all entities, and then just did
# for entity in books:
#   book_keys.append(entity.key())
#I feel like you've already got the overhead of the Query though, so maybe you're just saving on process
#memory at that point..
customer_keys = []
book_keys = []
objects = []
"""
Create Database Models
"""


class bookModel(ndb.Model):
    id = ndb.IntegerProperty()
    title = ndb.StringProperty()
    isbn = ndb.StringProperty()
    genre = ndb.StringProperty(repeated=True)
    author = ndb.StringProperty()
    checkedIn = ndb.BooleanProperty()

class customerModel(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    balance = ndb.StringProperty()
    checked_out = ndb.StringProperty(repeated=True)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, CS496!')

    def delete(self):
        b = bookModel.query()
        c = customerModel.query()

        for book in b:
            book.key.delete()
        for customer in c:
            customer.key.delete()
        self.response.write("Successfully deleted all books and customers.")

"""
Customer Handler

Provides a REST api for creating, updating, and deleting book objects
"""


class BookListHandler(webapp2.RequestHandler):
    b = bookModel.query()

    """
    RESTful GET @ /books/
    """
    def get(self, args):
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        output = []

        #/books
        if args == "" or args == "/":
            self.response.headers['Content-Type'] = 'application/json'
            if self.request.get("checkedIn"):
                flag = self.request.get("checkedIn").capitalize()
                if flag == "True":
                    books = self.b.filter(bookModel.checkedIn == True)
                else:
                    books = self.b.filter(bookModel.checkedIn == False)

                for book in books:
                    output.append(json.dumps(book.to_dict()))


            else:
                for book in self.b:
                    output.append(json.dumps(book.to_dict()))

        elif path_len == 2 and path[1].isdigit():
            desired_book = self.b.filter(bookModel.id == int(path[1])).get()
            self.response.headers['Content-Type'] = 'application/json'
            output.append(json.dumps(desired_book.to_dict()))
        self.response.write( ",".join(output).join(("[", "]")))

    def post(self, args):
        if args == "" or args == "/":
            output = []
            try:
                checked_flag = False
                if self.request.get('checkedIn') == ("True" or "true"):
                    checked_flag = True

                new_book = bookModel(
                    id = 0,
                    title=self.request.get('title'),
                    isbn=self.request.get('isbn'),
                    genre=self.request.get_all('genre'),
                    author=self.request.get('author'),
                    checkedIn=checked_flag
                )
                book_key = new_book.put()
                new_book.id = book_key.id()

                #Send the new entry to the Datastore
                new_book.put()
                self.response.status = 201
                self.response.write(json.dumps(new_book.to_dict()))


            except Exception as e:
                self.response.write(output)
        else:
            self.response.write(output)

    def delete(self, args):
        path_info = parse_url( args )
        path_len = path_info[0]
        path = path_info[1]
        #Lets delete a customer by id
        if path_len == 2 and path[1].isdigit():
            book_by_id = self.b.filter(bookModel.id == int(path[1]))
            for x in book_by_id:
                x.key.delete()

        elif args == "" or args == "/":
            for book in self.b:
                book.key.delete()

        self.response.write("")

    def put(self, args):
        output = []
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]

        #Lets delete a customer by id
        if path_len == 2 and path[1].isdigit():
            book_by_id = self.b.filter(bookModel.id == int(path[1]))
            for x in book_by_id:
                #Replace the books contents
                if self.request.get('title'):
                    x.title = self.request.get('title')
                else:
                    x.title = ""
                if self.request.get('author'):
                    x.author = self.request.get('author')
                else:
                    x.author = ""
                if self.request.get('isbn'):
                    x.isbn = self.request.get('isbn')
                else:
                    x.isbn = ""
                if self.request.get('genre'):
                    x.genre = self.request.get_all('genre')
                else:
                    x.genre = []
                if self.request.get('id'):
                    x.id = int(self.request.get('id'))
                if self.request.get('checkedIn'):
                    x.checkedIn = bool(self.request.get('checkedIn'))
                else:
                    x.checkedIn = True
                x.put()
                self.response.status = 201
                output.append(json.dumps(x.to_dict()))
        self.response.write( ",".join(output).join(("[", "]")))

    def patch(self, args):
        output = []
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        filepointer = StringIO(self.request.body)
        form = cgi.FieldStorage(
            fp = filepointer,
            headers = self.request.headers,
            environ= { 'REQUEST_METHOD' : 'PATCH',
                       'CONTENT_TYPE' : self.request.headers['content-type']
                    }
            )
        title = form.getfirst("title","")
        author = form.getfirst("author","")
        isbn = form.getfirst('isbn', "")
        genres = form.getlist('genre')
        bookId = form.getfirst('id', "")
        checkFlag = form.getfirst('checkedIn', "")

        #Lets delete a customer by id
        if path_len == 2 and path[1].isdigit():
            book = self.b.filter(bookModel.id == int(path[1])).get()
            #Replace the books contents
            if title:
                book.title = title
            if author:
                book.author = author
            if isbn:
                book.isbn = isbn
            if genres:
                book.genre = genres
            if bookId:
                book.id = bookId
            if checkFlag:
                book.checkedIn = bool(checkFlag)
            book.put()
            self.response.status = 201
            output.append(json.dumps(book.to_dict()))
            self.response.write(",".join(output).join(("[", "]")))


"""
Customer Handler

Provides a REST api for creating, updating, and deleting Customer objects
"""
class CustomerListHandler(webapp2.RequestHandler):
    c = customerModel.query()

    def get(self, args):
        output = []
        #Checking a book in
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        #Get all of the customers
        if args == "" or args == "/":
            for customer in self.c:
                output.append(json.dumps(customer.to_dict()))
                self.response.headers['Content-Type'] = 'application/json'
            self.response.write(",".join(output).join(("[", "]")))

        elif path_len == 2 and path[1].isdigit():
            cust_by_id = self.c.filter(customerModel.id == int(path[1])).get()
            self.response.headers['Content-Type'] = 'application/json'
            output.append(json.dumps(cust_by_id.to_dict()))
            self.response.write(",".join(output).join(("[", "]")))

        elif path_len == 4 and path[1].isdigit() and path[2] == "books":
            cust_by_id = self.c.filter(customerModel.id == int(path[1])).get()
            for x in cust_by_id.checked_out:
                if x:
                    b_id = x.split("/")
                    if int(b_id[2]) == int(path[3]):
                        self.response.headers['Content-Type'] = 'application/json'
                        book = bookModel.query(bookModel.id == int(path[3])).get()
                        self.response.write(json.dumps(book.to_dict()))

        elif path_len == 3 and path[1].isdigit() and path[2] == "books":
            cust_by_id = self.c.filter(customerModel.id == int(path[1])).get()
            for x in cust_by_id.checked_out:
                if x:
                    b_id = x.split("/")
                    if b_id[2].isdigit():
                        self.response.headers['Content-Type'] = 'application/json'
                        book = bookModel.query(bookModel.id == int(b_id[2])).get()
                        output.append(json.dumps(book.to_dict()))
            self.response.write(",".join(output).join(("[", "]")))

    def post(self, args):
        output = []
        if args == "" or args == "/":
            try:
                new_customer = customerModel(
                    id = 0,
                    name=self.request.get('name'),
                    balance=self.request.get('balance'),
                    checked_out=self.request.get_all('checked_out')
                )
                customer_key = new_customer.put()
                new_customer.id = customer_key.integer_id()
                new_customer.put()
                self.response.headers['Content-Type'] = 'application/json'
                self.response.status = 201
                self.response.write(json.dumps(new_customer.to_dict()))

            except Exception as e:
                self.response.write(output)

        else:
            self.response.write(output)

    def delete(self, args):
        #Checking a book in
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        if path_len == 2 and path[1].isdigit():
            cust_by_id = self.c.filter(customerModel.id == int(path[1]))
            for x in cust_by_id:
                x.key.delete()

        # Check In a book
        if path_len == 4 and path[1].isdigit() and path[3].isdigit() and path[2] == "books":
            c_id = path[1]
            b_id = path[3]

            cust_by_id = self.c.filter(customerModel.id == int(c_id)).get()
            book_by_id = bookModel.query(bookModel.id == int(b_id)).get()
            cust_by_id.checked_out.remove("/books/" + b_id)
            book_by_id.checkedIn = True
            book_by_id.put()
            cust_by_id.put()
        if args == "" or args == "/":
            for cust in self.c:
                cust.key.delete()

    def put(self, args):
        output = []
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        # Lets delete a customer by id
        if path_len == 4 and path[1].isdigit() and path[3].isdigit() and path[2] == "books":
            c_id = path[1]
            b_id = path[3]

            cust_by_id = self.c.filter(customerModel.id == int(c_id)).get()
            book_by_id = bookModel.query(bookModel.id == int(b_id)).get()
            cust_by_id.checked_out.append("/books/" + b_id)
            book_by_id.checkedIn = False

            book_by_id.put()
            cust_by_id.put()

            self.response.headers['Content-Type'] = 'application/json'
            self.response.status = 201
            output.append(json.dumps(cust_by_id.to_dict()))

        #Lets update a customer by id
        if path_len == 2 and path[1].isdigit():
            cust_by_id = self.c.filter(customerModel.id == int(path[1]))
            for x in cust_by_id:
                #Replace the books contents
                if self.request.get('name'):
                    x.name = self.request.get('name')
                else:
                    x.name = ""
                if self.request.get('balance'):
                    x.balance = self.request.get('balance')
                else:
                    x.balance = ""
                if self.request.get('checked_out'):
                    x.checked_out = self.request.get_all('checked_out')
                else:
                    x.checked_out = []
                if self.request.get('id'):
                    x.id = int(self.request.get('id'))

                x.put()
                self.response.status = 201
                output.append(json.dumps(x.to_dict()))
        self.response.write( ",".join(output).join(("[", "]")))

    def patch(self, args):
        output = []
        path_info = parse_url(args)
        path_len = path_info[0]
        path = path_info[1]
        filepointer = StringIO(self.request.body)
        form = cgi.FieldStorage(
            fp = filepointer,
            headers = self.request.headers,
            environ= { 'REQUEST_METHOD' : 'PATCH',
                       'CONTENT_TYPE' : self.request.headers['content-type']
                    }
            )
        name = form.getfirst("name","")
        balance = form.getfirst("balance","")
        cId = form.getfirst('id', "")
        checkOut = form.getlist('checked_out')

        #Lets delete a customer by id
        if path_len == 2 and path[1].isdigit():
            cust = self.c.filter(customerModel.id == int(path[1])).get()
            #Replace the books contents
            if name:
                cust.name = name
            if balance:
                cust.balance = balance
            if cId:
                cust.id = cId
            if checkOut:
                cust.checked_out = checkOut

            cust.put()
            self.response.status = 201
            output.append(json.dumps(cust.to_dict()))
            self.response.write(",".join(output).join(("[", "]")))


def handle_404(request, response, exception):
    response.write(' The URL you requested isn\'t valid in this site!')
    response.set_status(404)


def handle_500(request, response, exception):
    response.write(exception)
    response.set_status(500)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

app.router.add((r'/books(.*)', BookListHandler))
app.router.add((r'/customers(.*)', CustomerListHandler))

def parse_url( url ):
    x = url.split("/")
    return len(x),x


def main():
    app.run()

if __name__ == '__main__':
    main()



