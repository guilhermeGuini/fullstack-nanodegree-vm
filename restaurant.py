from http.server import BaseHTTPRequestHandler

from db.database_setup import Restaurant
from db.connect import Connection

import cgi

conn = Connection()

class restaurantHandler():

    def add(handler: BaseHTTPRequestHandler):
        ctype, pdict = cgi.parse_header(handler.headers.get('Content-Type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(handler.rfile, pdict)
            name = fields.get('name')[0]

        restaurant = Restaurant(name = name)
        session = conn.connect()
        session.add(restaurant)
        session.commit()

        print("Restaurant %s created" % name)
        handler.send_response(303)
        handler.send_header('Location', '/restaurants')
        handler.end_headers()
        return


    def update(handler: BaseHTTPRequestHandler):
        ctype, pdict = cgi.parse_header(handler.headers.get('Content-Type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(handler.rfile, pdict)
            name = fields.get('name')[0]

        indexId = 2
        restaurantId = handler.path.split('/')[indexId]

        session = conn.connect()
        restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()

        restaurant.name = name
        session.add(restaurant)
        session.commit()

        print("Restaurant with id {} has updated name to {}".format(restaurant.id, name))

        handler.send_response(303)
        handler.send_header('Location', '/restaurants')
        handler.end_headers()
        return

    def delete(handler: BaseHTTPRequestHandler):
        indexId = 2
        restaurantId = handler.path.split('/')[indexId]

        session = conn.connect()
        restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()

        session.delete(restaurant)
        session.commit()

        print("Restaurant with id %s was removed" % restaurant.id)

        handler.send_response(303)
        handler.send_header('Location', '/restaurants')
        handler.end_headers()
        return
