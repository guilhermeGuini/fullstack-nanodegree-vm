from http.server import BaseHTTPRequestHandler

from db.database_setup import Restaurant
from db.connect import Connection

conn = Connection()

class restaurantUI():

    def doGet(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()

        session = conn.connect()
        restaurants = session.query(Restaurant).all()

        output = ""
        output += "<html><body>"
        output += "<h1>Restaurants</h1>"

        for restaurant in restaurants:
            output += "<div>%s</div>" % restaurant.name
            output += "<div><a href='/restaurants/%s/edit'>Edit</a></div>" % restaurant.id
            output += "<div><a href='/restaurants/%s/delete'>Delete</a></div>" % restaurant.id
            output += "<br/>"
        
        output += "<a href='/restaurants/new'>Create new restaurant</a>"
        
        output += "</body></html>"
        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return

    def newPage(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        
        output = "<html><body>"
        output += "<h1>Edit Restaurant</h1>"
        output += "<form enctype='multipart/form-data' action='/restaurants/new' method='POST'>"
        output += "<div><label>Name: </label><input type='text' name='name' /></div>"
        output += "<br/><input type='submit' value='Submit'>"
        output += "</form>"
        output += "</body></html>"


        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return

    def editPage(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        
        indexId = 2
        restaurantId = handler.path.split('/')[indexId]

        session = conn.connect()
        restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()

        output = "<html><body>"
        output += "<h1>Edit Restaurant</h1>"
        output += "<form enctype='multipart/form-data' action='/restaurants/%s/doEdit' method='POST'>" % restaurant.id
        output += "<div><label>Id: %s</label>" % restaurant.id
        output += "<div><label>Name: </label><input type='text' name='name' value='%s'/></div>" % restaurant.name
        output += "<br/><input type='submit' value='Submit'>"
        output += "</form>"
        output += "</body></html>"


        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return


    def deletePage(handler: BaseHTTPRequestHandler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        
        indexId = 2
        restaurantId = handler.path.split('/')[indexId]

        session = conn.connect()
        restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()

        output = "<html><body>"
        output += "<h1>Confirm delete for:</h1>"
        output += "<form enctype='multipart/form-data' action='/restaurants/%s/delete' method='POST'>" % restaurant.id
        output += "<div><label>Id: %s</label>" % restaurant.id
        output += "<div><label>Name: %s</label></div>" % restaurant.name
        output += "<br/><input type='submit' value='Yes'>"
        output += "</form>"
        output += "<a href='/restaurants' >No</a>"
        output += "</body></html>"


        handler.wfile.write(output.encode('utf-8'))
        print(output)
        return