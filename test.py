#!/opt/local/bin/python2.7

# To run this you may need to install requests. Do this by running
# sudo python -m pip install requests

import requests as r
import json as j
from time import sleep

url="https://lasthope-155502.appspot.com"

# This controls how much we wait for things to become consistent.
# It is measured in seconds.
WAIT=2

b1 = {
	"title": "The Hitchhikers guide to the galaxy",
	"author": "Douglas Adams",
	"isbn": "0345391802" ,
	"genre": ["sci-fi", "humor"],
	"checkedIn": False
}

b2 = {
	"title": "The Name of the Rose",
	"author": "Umberto Eco",
	"isbn": "0343215043",
	"genre": ["mistery"],
	"checkedIn": True
}

c1 = {
	'name': 'John Smith',
	'balance': 0.0,
	'checked_out': []
}

knownBooks = []
customers = []

# Getting the books in the library
resp = r.get(url + '/books')
assert resp.status_code == 200

# Delete everything
resp = r.delete(url + '/')
assert resp.status_code == 200 or resp.status_code == 204

sleep(WAIT) # waiting for the changes to propagate

# Now the library should be empty
resp = r.get(url + '/books')
assert resp.status_code == 200
assert resp.text == "[]"

# Adding two books
resp = r.post(url + '/books', json=b1)
print resp.status_code
assert resp.status_code == 201
knownBooks.append(j.loads(resp.text)['id'])

resp = r.post(url + '/books', json=b2)
assert resp.status_code == 201
knownBooks.append(j.loads(resp.text)['id'])

sleep(WAIT) # waiting for the changes to propagate

# Checking that they exist
resp = r.get(url + '/books')
assert resp.status_code == 200
assert len(j.loads(resp.text)) == 2

# Deleting one book
resp = r.delete(url + '/books/' + str(knownBooks[0]))
assert resp.status_code == 200 or resp.status_code == 204

sleep(WAIT) # waiting for the changes to propagate

#We should have only one book
resp = r.get(url + '/books')
assert resp.status_code == 200
assert len(j.loads(resp.text)) == 1

# Checking the customers url
resp = r.get(url + '/customers')
assert resp.status_code == 200
assert len(j.loads(resp.text)) == 0

# Adding a customer
resp = r.post(url + '/customers', json=c1)
assert resp.status_code == 201
customers.append(j.loads(resp.text)['id'])

# Querying the customer
resp = r.get(url + '/customers/' + str(customers[0]))
assert resp.status_code == 200

# Checkout a book
resp = r.put(url + "/customers/" + str(customers[0]) + "/books/" + str(knownBooks[1]))
assert resp.status_code == 201

# Check that the book is checked out
resp = r.get(url + "/customers/" + str(customers[0]) + "/books/" + str(knownBooks[1]))
assert resp.status_code == 200
assert j.loads(resp.text)['id'] == knownBooks[1]

# Get a list of checked out books
resp = r.get(url + "/books?checkedIn=false")
assert resp.status_code == 200
assert len(j.loads(resp.text)) == 1

# Check in a book
resp = r.delete(url + "/customers/" + str(customers[0]) + "/books/" + str(knownBooks[1]))
assert resp.status_code == 200

sleep(WAIT) # waiting for the changes to propagate

# No books should be checked out
resp = r.get(url + "/books?checkedIn=false")
assert resp.status_code == 200
assert len(j.loads(resp.text)) == 0

print "====SUCCESS===="
